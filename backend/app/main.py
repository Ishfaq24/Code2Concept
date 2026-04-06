import os
import re
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.services.llm_service import get_llm_service
from app.utils.clean_code import clean_code

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
if os.path.exists("media"):
    app.mount("/media", StaticFiles(directory="media"), name="media")


class GenerateRequest(BaseModel):
    topic: str


@app.get("/")
async def root():
    return {"message": "Video Generation API running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def generate_video(request: GenerateRequest):
    """Generate video from topic - ONE STEP process"""
    
    topic = request.topic.strip()
    
    if not topic:
        return {"error": "Topic is required"}
    
    print(f"\n🚀 Generating video for: {topic}\n")
    
    try:
        # STEP 1: Generate code
        print("📝 Step 1: Generating Manim code...")
        llm_service = get_llm_service()
        manim_code = llm_service.generate_manim_video_code(topic)

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
            return {
                "status": "success",
                "message": "Video generated successfully",
                "topic": topic,
                "video_path": "media/videos/scene/1080p30/DemoScene.mp4"
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
async def get_video(t: str = None):
    """Get the latest rendered video"""
    try:
        # Prefer high quality if available, otherwise fall back
        candidates = [
            "media/videos/scene/1080p30/DemoScene.mp4",
            "media/videos/scene/720p30/DemoScene.mp4",
            "media/videos/scene/480p15/DemoScene.mp4",
        ]
        video_path = next((p for p in candidates if os.path.exists(p)), None)
        if video_path:
            from fastapi.responses import FileResponse
            return FileResponse(video_path, media_type="video/mp4")
        return {"error": "Video not found"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)