import os
import re
import subprocess
import uuid
from fastapi import FastAPI, HTTPException
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


@app.get("/")
async def root():
    return {"message": "Video Generation API running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def generate_video(request: GenerateRequest):
    """Generate video from topic - ONE STEP process"""
    global CURRENT_VIDEO_PATH, CURRENT_VIDEO_TOKEN
    
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
    
    print(f"\n🚀 Generating video for: {topic} ({language_name})\n")
    
    try:
        # STEP 1: Generate code
        print("📝 Step 1: Generating Manim code...")
        llm_service = get_llm_service()
        manim_code = llm_service.generate_manim_video_code(topic)

        # Also generate narration script for voice-over
        print("🗣️ Generating narration script...")
        narration_text = llm_service.generate_narration_text(topic, language_name)

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
            CURRENT_VIDEO_PATH = final_video_path
            CURRENT_VIDEO_TOKEN = uuid.uuid4().hex

            return {
                "status": "success",
                "message": "Video generated successfully",
                "topic": topic,
                "video_path": final_video_path,
                "language": language_code,
                "voice_enabled": voice_enabled,
                "narration_text": narration_text,
                "video_token": CURRENT_VIDEO_TOKEN,
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)