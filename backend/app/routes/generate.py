from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from app.schemas.request import Query

# 🔥 CORE (CONTROLLED SYSTEM)
from app.services.llm_service import (
    generate_teaching_script,
    generate_manim_from_script
)

# 🔥 OPTIONAL AI ENHANCEMENT
from app.services.research_service import generate_research
from app.services.refine_service import refine_code

from app.services.manim_service import save_code, render_video
from app.utils.clean_code import clean_code

router = APIRouter()


@router.post("/generate")
async def generate(q: Query):
    try:
        print(f"\n🚀 Generating video for: {q.topic}\n")

        # =========================
        # 🔹 STEP 1: BASE SCRIPT (ALWAYS WORKS)
        # =========================
        script = generate_teaching_script(q.topic)
        print("✅ Base script generated")

        # =========================
        # 🔹 STEP 2: OPTIONAL RESEARCH (ENHANCE)
        # =========================
        try:
            research = generate_research(q.topic)
            print("✅ Research added")

            # (Optional: later you can merge research into script)
        except Exception as e:
            print("⚠️ Research failed:", e)

        # =========================
        # 🔹 STEP 3: GENERATE MANIM CODE
        # =========================
        raw_code = generate_manim_from_script(script)
        print("✅ Manim code generated")

        # =========================
        # 🔹 STEP 4: REFINE CODE (OPTIONAL)
        # =========================
        try:
            final_code = refine_code(raw_code)
            print("✅ Code refined")
        except Exception as e:
            print("⚠️ Refinement failed:", e)
            final_code = raw_code

        # =========================
        # 🔹 CLEAN + SAVE
        # =========================
        code = clean_code(final_code)

        print("\n===== FINAL CODE =====\n")
        print(code)
        print("\n======================\n")

        save_code(code)

        # =========================
        # 🔹 RENDER VIDEO
        # =========================
        render_video()

        video_path = "media/videos/scene/480p15/DemoScene.mp4"

        if not os.path.exists(video_path):
            return {"error": "Video not generated"}

        return {
            "message": "Video generated successfully",
            "topic": q.topic
        }

    except Exception as e:
        return {"error": str(e)}


@router.get("/video")
def get_video():
    video_path = "media/videos/scene/480p15/DemoScene.mp4"

    if not os.path.exists(video_path):
        return {"error": "Video not found"}

    return FileResponse(video_path, media_type="video/mp4")