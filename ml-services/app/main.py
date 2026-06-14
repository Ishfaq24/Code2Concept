import os
import re
import json
import shutil
import hashlib
import sqlite3
import subprocess
import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.llm_service import get_llm_service
from app.services.voice_service import generate_narration_audio, merge_audio_with_video
from app.utils.clean_code import clean_code

app = FastAPI()

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "hi": "Hindi",
}

CURRENT_VIDEO_PATH = None
CURRENT_VIDEO_TOKEN = None
CURRENT_PDF_PATH = None
CURRENT_STUDY_GUIDE = None
CURRENT_TOPIC = None
CURRENT_LANGUAGE_NAME = None
CURRENT_LANGUAGE_CODE = None
CURRENT_CACHE_KEY = None

CACHE_DB_PATH = "generated/topic_cache.db"
CACHE_VIDEO_DIR = "generated/cache/videos"
CACHE_PDF_DIR = "generated/cache/pdfs"

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str
    language: str = "en"
    generate_pdf: bool = False


def _ensure_cache_storage() -> None:
    os.makedirs("generated", exist_ok=True)
    os.makedirs(CACHE_VIDEO_DIR, exist_ok=True)
    os.makedirs(CACHE_PDF_DIR, exist_ok=True)


def _cache_connection() -> sqlite3.Connection:
    _ensure_cache_storage()
    conn = sqlite3.connect(CACHE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_cache_db() -> None:
    with _cache_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS topic_cache (
                cache_key TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                normalized_topic TEXT NOT NULL,
                language_code TEXT NOT NULL,
                language_name TEXT NOT NULL,
                narration_text TEXT,
                study_guide_json TEXT,
                video_path TEXT NOT NULL,
                pdf_path TEXT,
                voice_enabled INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                hit_count INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_topic_cache_lookup
            ON topic_cache (normalized_topic, language_code)
            """
        )


def _normalize_topic(topic: str) -> str:
    return re.sub(r"\s+", " ", topic.strip().lower())


def _cache_key(topic: str, language_code: str) -> str:
    raw = f"{_normalize_topic(topic)}|{language_code.strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _safe_load_json(raw: str):
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _copy_to_cache(source_path: str, destination_path: str) -> str:
    if not source_path or not os.path.exists(source_path):
        return None
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.copy2(source_path, destination_path)
    return destination_path


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_cached_entry(topic: str, language_code: str):
    key = _cache_key(topic, language_code)
    with _cache_connection() as conn:
        row = conn.execute(
            "SELECT * FROM topic_cache WHERE cache_key = ?",
            (key,),
        ).fetchone()

        if not row:
            return None

        video_path = row["video_path"]
        if not video_path or not os.path.exists(video_path):
            conn.execute("DELETE FROM topic_cache WHERE cache_key = ?", (key,))
            return None

        conn.execute(
            "UPDATE topic_cache SET hit_count = hit_count + 1, updated_at = datetime('now') WHERE cache_key = ?",
            (key,),
        )

        return dict(row)


def _save_cache_entry(
    topic: str,
    language_code: str,
    language_name: str,
    narration_text: str,
    study_guide,
    source_video_path: str,
    voice_enabled: bool,
    source_pdf_path: str = None,
):
    key = _cache_key(topic, language_code)
    cached_video_path = _copy_to_cache(
        source_video_path,
        os.path.join(CACHE_VIDEO_DIR, f"{key}.mp4"),
    )
    if not cached_video_path:
        return None

    cached_pdf_path = None
    if source_pdf_path:
        cached_pdf_path = _copy_to_cache(
            source_pdf_path,
            os.path.join(CACHE_PDF_DIR, f"{key}.pdf"),
        )

    now = _now_utc_iso()
    study_guide_json = json.dumps(study_guide) if study_guide else None

    with _cache_connection() as conn:
        conn.execute(
            """
            INSERT INTO topic_cache (
                cache_key, topic, normalized_topic, language_code, language_name,
                narration_text, study_guide_json, video_path, pdf_path, voice_enabled,
                created_at, updated_at, hit_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            ON CONFLICT(cache_key) DO UPDATE SET
                topic = excluded.topic,
                language_name = excluded.language_name,
                narration_text = excluded.narration_text,
                study_guide_json = COALESCE(excluded.study_guide_json, topic_cache.study_guide_json),
                video_path = excluded.video_path,
                pdf_path = COALESCE(excluded.pdf_path, topic_cache.pdf_path),
                voice_enabled = excluded.voice_enabled,
                updated_at = excluded.updated_at
            """,
            (
                key,
                topic,
                _normalize_topic(topic),
                language_code,
                language_name,
                narration_text,
                study_guide_json,
                cached_video_path,
                cached_pdf_path,
                int(bool(voice_enabled)),
                now,
                now,
            ),
        )
    return key


def _list_cached_topics(limit: int = 50):
    safe_limit = max(1, min(limit, 200))
    with _cache_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                topic,
                language_code,
                language_name,
                voice_enabled,
                CASE WHEN pdf_path IS NOT NULL THEN 1 ELSE 0 END AS has_pdf,
                hit_count,
                updated_at
            FROM topic_cache
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def _cache_totals():
    with _cache_connection() as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*) AS total_topics,
                COALESCE(SUM(hit_count), 0) AS total_hits,
                COALESCE(SUM(CASE WHEN pdf_path IS NOT NULL THEN 1 ELSE 0 END), 0) AS topics_with_pdf
            FROM topic_cache
            """
        ).fetchone()
    return dict(row)


def _update_cache_pdf(cache_key: str, pdf_source_path: str):
    if not cache_key or not pdf_source_path or not os.path.exists(pdf_source_path):
        return None

    cached_pdf_path = _copy_to_cache(
        pdf_source_path,
        os.path.join(CACHE_PDF_DIR, f"{cache_key}.pdf"),
    )
    if not cached_pdf_path:
        return None

    with _cache_connection() as conn:
        conn.execute(
            "UPDATE topic_cache SET pdf_path = ?, updated_at = datetime('now') WHERE cache_key = ?",
            (cached_pdf_path, cache_key),
        )

    return cached_pdf_path


def _upgrade_cached_voice(
    cached: dict,
    topic: str,
    language_name: str,
    language_code: str,
    cached_pdf_path: str = None,
) -> dict:
    """Try to rebuild a voiced cached video when the stored cache is silent."""

    if not cached or cached.get("voice_enabled"):
        return cached

    narration_text = (cached.get("narration_text") or "").strip()
    video_path = cached.get("video_path")
    if not narration_text or not video_path or not os.path.exists(video_path):
        return cached

    try:
        print("🎙️ Cache hit is silent; rebuilding voiced video...")
        audio_filename = f"{cached['cache_key']}_narration_{language_code}.mp3"
        audio_path = generate_narration_audio(
            narration_text,
            filename=audio_filename,
            language=language_code,
        )

        merged_path = merge_audio_with_video(video_path, audio_path)
        if not merged_path:
            print("⚠️ Could not rebuild voiced cache entry; keeping silent video")
            return cached

        _save_cache_entry(
            topic=topic,
            language_code=language_code,
            language_name=language_name,
            narration_text=narration_text,
            study_guide=_safe_load_json(cached.get("study_guide_json")),
            source_video_path=merged_path,
            voice_enabled=True,
            source_pdf_path=cached_pdf_path,
        )

        updated_cached = dict(cached)
        updated_cached["video_path"] = os.path.join(CACHE_VIDEO_DIR, f"{cached['cache_key']}.mp4")
        updated_cached["voice_enabled"] = 1
        return updated_cached

    except Exception as voice_error:
        print(f"⚠️ Failed to rebuild voiced cache entry: {voice_error}")
        return cached


_init_cache_db()


@app.get("/")
async def root():
    return {"message": "Video Generation API running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/cache/topics")
async def cached_topics(limit: int = 50):
    """List recent cached topics shared across all users."""
    topics = _list_cached_topics(limit=limit)
    return {
        "status": "success",
        "shared_cache": True,
        "count": len(topics),
        "topics": topics,
    }


@app.get("/cache/stats")
async def cache_stats():
    """High-level stats for the shared topic cache."""
    return {
        "status": "success",
        "shared_cache": True,
        **_cache_totals(),
    }


@app.post("/generate")
async def generate_video(request: GenerateRequest):
    """Generate video from topic - ONE STEP process"""
    global CURRENT_VIDEO_PATH, CURRENT_VIDEO_TOKEN, CURRENT_PDF_PATH
    global CURRENT_STUDY_GUIDE, CURRENT_TOPIC, CURRENT_LANGUAGE_NAME, CURRENT_LANGUAGE_CODE, CURRENT_CACHE_KEY
    
    topic = request.topic.strip()
    language_code = request.language.lower().strip()
    language_name = SUPPORTED_LANGUAGES.get(language_code)
    
    if not topic:
        return {"error": "Topic is required"}

    if not language_name:
        return {
            "status": "error",
            "error": "Unsupported language",
            "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
        }

    cached = _get_cached_entry(topic, language_code)
    if cached:
        print(f"\n⚡ Cache hit for topic: {topic} ({language_name})\n")

        study_guide = _safe_load_json(cached.get("study_guide_json"))
        cached_pdf_path = cached.get("pdf_path")
        if cached_pdf_path and not os.path.exists(cached_pdf_path):
            cached_pdf_path = None

        if request.generate_pdf and not cached_pdf_path and study_guide:
            try:
                generated_pdf_path = _build_study_guide_pdf(
                    study_guide=study_guide,
                    topic=topic,
                    language_name=language_name,
                    language_code=language_code,
                    token="cached",
                )
                cached_pdf_path = _update_cache_pdf(cached["cache_key"], generated_pdf_path)
            except Exception as pdf_build_error:
                print(f"⚠️ Could not build PDF from cache: {pdf_build_error}")

        cached = _upgrade_cached_voice(
            cached=cached,
            topic=topic,
            language_name=language_name,
            language_code=language_code,
            cached_pdf_path=cached_pdf_path,
        )

        CURRENT_VIDEO_TOKEN = uuid.uuid4().hex
        CURRENT_VIDEO_PATH = cached["video_path"]
        CURRENT_PDF_PATH = cached_pdf_path if request.generate_pdf else None
        CURRENT_STUDY_GUIDE = study_guide
        CURRENT_TOPIC = topic
        CURRENT_LANGUAGE_NAME = language_name
        CURRENT_LANGUAGE_CODE = language_code
        CURRENT_CACHE_KEY = cached["cache_key"]

        return {
            "status": "success",
            "message": "Video loaded from cache",
            "topic": topic,
            "video_path": CURRENT_VIDEO_PATH,
            "pdf_path": CURRENT_PDF_PATH,
            "pdf_available": bool(CURRENT_PDF_PATH),
            "pdf_error": None,
            "pdf_requested": bool(request.generate_pdf),
            "language": language_code,
            "voice_enabled": bool(cached.get("voice_enabled")),
            "narration_text": cached.get("narration_text"),
            "video_token": CURRENT_VIDEO_TOKEN,
            "cached": True,
        }
    
    print(f"\n🚀 Generating video for: {topic} ({language_name})\n")
    
    try:
        # STEP 1: Generate code
        print("📝 Step 1: Generating Manim code...")
        llm_service = get_llm_service()
        manim_code = llm_service.generate_manim_video_code(topic)

        # Also generate narration script for voice-over
        print("🗣️ Generating narration script...")
        narration_text = llm_service.generate_narration_text(
            topic,
            language_name,
            language_code,
        )

        study_guide = None
        if request.generate_pdf:
            study_guide = llm_service.generate_study_guide(
                topic,
                "English",
                "en",
            )

        # STEP 2: Clean, prepare and save code
        print("🧹 Step 2: Cleaning and saving code to file...")
        manim_code = clean_code(manim_code)
        os.makedirs("generated", exist_ok=True)
        
        # Ensure import is first
        if "from manim import" not in manim_code:
            manim_code = "from manim import *\n\n" + manim_code
        
        # Ensure class name is DemoScene
        manim_code = re.sub(r'class \w+Scene\(Scene\):', 'class DemoScene(Scene):', manim_code)
        
        # Print what we're saving
        print("\n" + "="*80)
        print("📄 SAVING TO FILE (first 15 lines):")
        print("="*80)
        lines = manim_code.split('\n')[:15]
        for i, line in enumerate(lines, 1):
            print(f"{i}: {line}")
        print("="*80 + "\n")
        
        with open("generated/scene.py", "w", encoding="utf-8") as f:
            f.write(manim_code)
        
        print("✅ Code saved successfully\n")
        
        # STEP 3: Render video (higher quality)
        print("🎬 Step 3: Rendering video in high quality (this may take a few minutes)...")
        # NOTE: With the Click-based Manim CLI, options must come
        # *before* the first non-option argument (the script path).
        # If flags like -pqh or --frame_rate are placed after the
        # script path, Manim treats them as scene names and Click
        # raises "no such option" errors, causing rendering to fail.
        result = subprocess.run(
            [
                "manim",
                "-pqh",              # preview, high quality
                "--frame_rate=30",   # 30 FPS so path is 1080p30
                "generated/scene.py",
                "DemoScene",
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        
        if result.returncode == 0:
            print("✅ Video rendered successfully!\n")

            base_video_path = "media/videos/scene/1080p30/DemoScene.mp4"
            voiced_video_path = None
            voice_enabled = False

            # STEP 4: Generate narration audio and merge with video
            try:
                print(f"🎙️ Generating narration audio ({language_code})...")
                audio_filename = f"DemoScene_narration_{language_code}.mp3"
                audio_path = generate_narration_audio(
                    narration_text,
                    filename=audio_filename,
                    language=language_code,
                )

                print("🎧 Merging audio with video...")
                merged_output_path = f"media/videos/scene/1080p30/DemoScene_voiced_{language_code}.mp4"
                merged_path = merge_audio_with_video(
                    base_video_path,
                    audio_path,
                    output_path=merged_output_path,
                )

                if merged_path:
                    voiced_video_path = merged_path
                    voice_enabled = True
                else:
                    print("⚠️ Falling back to silent video (merge failed)")
            except Exception as ve:
                print(f"⚠️ Voice generation failed, using silent video. Error: {ve}")

            final_video_path = voiced_video_path or base_video_path
            CURRENT_VIDEO_TOKEN = uuid.uuid4().hex
            CURRENT_VIDEO_PATH = final_video_path
            CURRENT_PDF_PATH = None
            CURRENT_STUDY_GUIDE = study_guide
            CURRENT_TOPIC = topic
            CURRENT_LANGUAGE_NAME = language_name
            CURRENT_LANGUAGE_CODE = language_code
            pdf_error = None

            if request.generate_pdf and study_guide:
                try:
                    CURRENT_PDF_PATH = _build_study_guide_pdf(
                        study_guide=study_guide,
                        topic=topic,
                        language_name=language_name,
                        language_code=language_code,
                        token=CURRENT_VIDEO_TOKEN,
                    )
                except Exception as pdf_error:
                    pdf_error = str(pdf_error)
                    print(f"⚠️ PDF generation failed, continuing with video only. Error: {pdf_error}")

            CURRENT_CACHE_KEY = _save_cache_entry(
                topic=topic,
                language_code=language_code,
                language_name=language_name,
                narration_text=narration_text,
                study_guide=study_guide,
                source_video_path=final_video_path,
                voice_enabled=voice_enabled,
                source_pdf_path=CURRENT_PDF_PATH,
            )

            return {
                "status": "success",
                "message": "Video generated successfully",
                "topic": topic,
                "video_path": final_video_path,
                "pdf_path": CURRENT_PDF_PATH,
                "pdf_available": bool(CURRENT_PDF_PATH),
                "pdf_error": pdf_error,
                "pdf_requested": bool(request.generate_pdf),
                "language": language_code,
                "voice_enabled": voice_enabled,
                "narration_text": narration_text,
                "video_token": CURRENT_VIDEO_TOKEN,
                "cached": False,
            }
        else:
            error_msg = result.stderr[:1000] if result.stderr else result.stdout[:1000]
            print(f"❌ Rendering failed:\n{error_msg}\n")
            return {
                "status": "error",
                "message": f"Video rendering failed",
                "error_details": error_msg
            }
            
    except subprocess.TimeoutExpired:
        print("❌ Rendering timeout\n")
        return {"status": "error", "message": "Video rendering timed out (exceeded 5 minutes)"}
    except Exception as e:
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


def _build_study_guide_pdf(study_guide, topic: str, language_name: str, language_code: str, token: str) -> str:
    """Render the generated study guide into a downloadable PDF."""

    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer
        from xml.sax.saxutils import escape
    except ImportError as exc:
        raise RuntimeError(
            "reportlab is required to generate PDFs. Install ml-services dependencies first."
        ) from exc

    os.makedirs("media/pdfs", exist_ok=True)

    def sanitize_filename(value: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
        cleaned = re.sub(r"_+", "_", cleaned).strip("._-")
        return cleaned or "study_guide"

    pdf_file_name = f"{sanitize_filename(topic)}.pdf"
    pdf_path = os.path.join("media/pdfs", pdf_file_name)

    def safe_text(value: str) -> str:
        text = value or ""
        try:
            text.encode("latin-1")
            return text
        except UnicodeEncodeError:
            # Keep PDF generation resilient with default fonts.
            return text.encode("latin-1", "replace").decode("latin-1")

    def paragraph_text(value: str) -> str:
        return escape(safe_text(value)).replace("\n", "<br/>")

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "GuideTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10,
    )
    subtitle_style = ParagraphStyle(
        "GuideSubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=16,
    )
    heading_style = ParagraphStyle(
        "GuideHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f766e"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "GuideBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#111827"),
        spaceAfter=8,
    )
    bullet_style = ParagraphStyle(
        "GuideBullet",
        parent=body_style,
        leftIndent=12,
        bulletIndent=0,
    )

    document = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        title=study_guide.get("title") or f"Study Guide: {topic}",
        author="Video Generation App",
    )

    story = []
    story.append(Paragraph(paragraph_text(study_guide.get("title") or f"Study Guide: {topic}"), title_style))
    story.append(Paragraph(paragraph_text(study_guide.get("subtitle") or f"A detailed revision guide in {language_name}"), subtitle_style))
    story.append(Paragraph(paragraph_text(f"Topic: {topic} | Language: {language_name} | Version: {language_code.upper()}"), subtitle_style))

    def add_section(title: str, content: str):
        if not content:
            return
        story.append(Paragraph(paragraph_text(title), heading_style))
        story.append(Paragraph(paragraph_text(content), body_style))

    def add_bullets(title: str, items):
        if not items:
            return
        story.append(Paragraph(paragraph_text(title), heading_style))
        bullets = []
        for item in items:
            bullets.append(ListItem(Paragraph(paragraph_text(str(item)), bullet_style)))
        story.append(ListFlowable(bullets, bulletType="bullet", leftIndent=16))

    add_section("Overview", study_guide.get("overview", ""))

    core_concepts = study_guide.get("core_concepts", []) or []
    if core_concepts:
        story.append(Paragraph(paragraph_text("Core Concepts"), heading_style))
        for concept in core_concepts:
            heading = concept.get("heading") if isinstance(concept, dict) else "Concept"
            content = concept.get("content") if isinstance(concept, dict) else str(concept)
            story.append(Paragraph(paragraph_text(str(heading)), body_style))
            story.append(Paragraph(paragraph_text(str(content)), body_style))

    add_section("Worked Example", study_guide.get("worked_example", ""))
    add_bullets("Real-World Applications", study_guide.get("real_world_applications", []))
    add_bullets("Common Misconceptions", study_guide.get("common_misconceptions", []))
    add_section("Quick Recap", study_guide.get("quick_recap", ""))
    add_bullets("Practice Questions", study_guide.get("practice_questions", []))
    add_bullets("Further Learning", study_guide.get("further_learning", []))

    document.build(story)
    return pdf_path


@app.get("/video")
async def get_video(token: str, t: str = None):
    """Get the latest rendered video"""
    if not CURRENT_VIDEO_TOKEN or token != CURRENT_VIDEO_TOKEN:
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        # Prefer high quality if available, otherwise fall back
        candidates = [
            CURRENT_VIDEO_PATH,
            "media/videos/scene/1080p30/DemoScene_voiced_en.mp4",
            "media/videos/scene/1080p30/DemoScene.mp4",
            "media/videos/scene/720p30/DemoScene.mp4",
            "media/videos/scene/480p15/DemoScene.mp4",
        ]
        video_path = next((p for p in candidates if p and os.path.exists(p)), None)
        if video_path:
            from fastapi.responses import FileResponse
            return FileResponse(
                video_path,
                media_type="video/mp4",
                headers={
                    "Content-Disposition": "inline",
                    "Cache-Control": "no-store, no-cache, must-revalidate, private",
                    "Pragma": "no-cache",
                    "Expires": "0",
                    "X-Content-Type-Options": "nosniff",
                },
            )
        return {"error": "Video not found"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/pdf")
async def get_pdf(token: str, t: str = None):
    """Get the latest generated study guide as a PDF"""
    if not CURRENT_VIDEO_TOKEN or token != CURRENT_VIDEO_TOKEN:
        raise HTTPException(status_code=403, detail="Access denied")

    pdf_candidates = [
        CURRENT_PDF_PATH,
        "media/pdfs/generated_study_guide.pdf",
    ]
    pdf_path = next((p for p in pdf_candidates if p and os.path.exists(p)), None)

    if not pdf_path:
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path),
        headers={
            "Content-Disposition": f'attachment; filename="{os.path.basename(pdf_path)}"',
            "Cache-Control": "no-store, no-cache, must-revalidate, private",
            "Pragma": "no-cache",
            "Expires": "0",
            "X-Content-Type-Options": "nosniff",
        },
    )


@app.post("/regenerate-pdf")
async def regenerate_pdf(token: str):
    """Retry generating the PDF without re-rendering the video."""
    global CURRENT_PDF_PATH, CURRENT_CACHE_KEY

    if not CURRENT_VIDEO_TOKEN or token != CURRENT_VIDEO_TOKEN:
        raise HTTPException(status_code=403, detail="Access denied")

    if not CURRENT_STUDY_GUIDE or not CURRENT_TOPIC:
        raise HTTPException(status_code=404, detail="No study guide available. Generate a video first.")

    try:
        CURRENT_PDF_PATH = _build_study_guide_pdf(
            study_guide=CURRENT_STUDY_GUIDE,
            topic=CURRENT_TOPIC,
            language_name=CURRENT_LANGUAGE_NAME or "English",
            language_code=CURRENT_LANGUAGE_CODE or "en",
            token=CURRENT_VIDEO_TOKEN,
        )

        if CURRENT_CACHE_KEY:
            cached_pdf = _update_cache_pdf(CURRENT_CACHE_KEY, CURRENT_PDF_PATH)
            if cached_pdf:
                CURRENT_PDF_PATH = cached_pdf

        return {
            "status": "success",
            "pdf_available": True,
            "pdf_path": CURRENT_PDF_PATH,
        }
    except Exception as e:
        return {
            "status": "error",
            "pdf_available": False,
            "error": str(e),
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)