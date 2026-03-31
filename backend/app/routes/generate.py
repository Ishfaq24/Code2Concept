from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from app.schemas.request import Query

# 🔥 CORE SYSTEM
from app.services.llm_service import (
    generate_teaching_script,
    generate_manim_from_script
)

from app.services.manim_service import save_code, render_video
from app.utils.clean_code import clean_code

router = APIRouter()


@router.post("/generate")
async def generate(q: Query):
    try:
        print(f"\n🚀 Generating video for: {q.topic}\n")

        # =========================
        # 🔹 STEP 1: SCRIPT (BRAIN)
        # =========================
        script = generate_teaching_script(q.topic)
        print("✅ Script generated:", script)

        # =========================
        # 🔹 STEP 2: MANIM CODE
        # =========================
        raw_code = generate_manim_from_script(script)
        print("✅ Manim code generated")

        # =========================
        # 🔹 CLEAN CODE
        # =========================
        code = clean_code(raw_code)

        print("\n===== FINAL CODE =====\n")
        print(code)
        print("\n======================\n")

        # =========================
        # 🔹 SAVE + RENDER
        # =========================
        save_code(code)
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