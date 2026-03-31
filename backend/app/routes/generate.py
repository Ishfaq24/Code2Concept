from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

from app.schemas.request import Query
from app.services.llm_service import (
    generate_teaching_script,
    generate_manim_from_script
)
from app.services.research_service import generate_research
from app.services.refine_service import refine_code, get_refinement_feedback
from app.services.manim_service import save_code, render_video, get_video_path, video_exists
from app.utils.clean_code import clean_code

router = APIRouter()

# Store current generation state for user feedback
current_generation = {
    "topic": None,
    "code": None,
    "script": None
}


@router.post("/generate")
async def generate(q: Query):
    """Generate video from topic"""
    try:
        print(f"\n🚀 Generating video for: {q.topic}\n")
        
        # STEP 1: Generate teaching script
        print("📝 Step 1: Generating teaching script...")
        script = generate_teaching_script(q.topic)
        print(f"✅ Script generated: {script.get('title')}")
        
        # STEP 2: Generate Manim code
        print("🎨 Step 2: Generating Manim code...")
        raw_code = generate_manim_from_script(script)
        print("✅ Manim code generated")
        
        # STEP 3: Refine code
        print("🔧 Step 3: Refining code...")
        try:
            final_code = refine_code(raw_code)
        except Exception as e:
            print(f"⚠️ Refinement failed: {e}, using raw code")
            final_code = raw_code
        
        # STEP 4: Clean code
        print("🧹 Step 4: Cleaning code...")
        code = clean_code(final_code)
        
        # STEP 5: Save code
        print("💾 Step 5: Saving code...")
        save_code(code)
        
        # STEP 6: Render video
        print("🎬 Step 6: Rendering video...")
        success = render_video(quality="low_quality", fps=15)
        
        if not success or not video_exists():
            raise Exception("Video rendering failed")
        
        # Store for user feedback
        current_generation["topic"] = q.topic
        current_generation["code"] = code
        current_generation["script"] = script
        
        print("\n✅ Video generation completed!\n")
        
        return {
            "message": "Video generated successfully",
            "topic": q.topic,
            "duration_seconds": script.get("duration_seconds", 90)
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "error": str(e),
            "message": "Video generation failed. Please try again."
        }


@router.post("/refine")
async def refine_video(feedback: dict):
    """
    Apply user feedback to refine the video
    
    Expected body:
    {
        "feedback": "Make it faster, add more colors, etc"
    }
    """
    try:
        if not current_generation["code"]:
            raise Exception("No video to refine. Generate one first.")
        
        user_feedback = feedback.get("feedback", "")
        if not user_feedback:
            raise Exception("Please provide feedback for refinement")
        
        print(f"\n🔄 Applying user feedback: {user_feedback}\n")
        
        # Apply feedback
        refined_code = get_refinement_feedback(current_generation["code"], user_feedback)
        
        # Clean and save
        code = clean_code(refined_code)
        save_code(code)
        
        # Render
        success = render_video(quality="low_quality", fps=15)
        
        if not success or not video_exists():
            raise Exception("Video re-rendering failed")
        
        current_generation["code"] = code
        
        print("✅ Video refined successfully!\n")
        
        return {
            "message": "Video refined successfully",
            "feedback_applied": user_feedback
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"error": str(e)}


@router.get("/video")
def get_video():
    """Serve the rendered video"""
    video_path = get_video_path()
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(video_path, media_type="video/mp4")


@router.get("/status")
def get_status():
    """Get current generation status"""
    return {
        "has_video": video_exists(),
        "current_topic": current_generation["topic"],
        "video_path": get_video_path() if video_exists() else None
    }