from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from app.schemas.request import Query
from app.services.llm_service import generate_manim_code
from app.services.manim_service import save_code, render_video
from app.utils.clean_code import clean_code

router = APIRouter()  # ✅ THIS WAS MISSING

@router.post("/generate")
async def generate(q: Query):
    try:
        raw_code = generate_manim_code(q.topic)
        code = clean_code(raw_code)

        print("Generated Code:\n", code)

        save_code(code)
        render_video()

        video_path = "media/videos/scene/480p15/DemoScene.mp4"

        if not os.path.exists(video_path):
            return {"error": "Video not generated"}

        return {"message": "Video generated"}

    except Exception as e:
        return {"error": str(e)}


@router.get("/video")
def get_video():
    return FileResponse(
        "media/videos/scene/480p15/DemoScene.mp4",  # ✅ FIXED PATH
        media_type="video/mp4"
    )