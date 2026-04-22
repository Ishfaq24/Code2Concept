"""
Main API routes for video generation pipeline.
Simplified pipeline: Script → Manim Code → Render → Video
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

from app.schemas.request import Query
from app.services.llm_service import (
    generate_teaching_script,
    generate_manim_from_script
)
from app.services.refine_service import refine_code, get_refinement_feedback
from app.services.manim_service import (
    save_code,
    render_video,
    get_video_path,
    video_exists
)
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
    """
    Generate educational video from a topic query.
    
    Pipeline:
    1. Generate teaching script using LLM
    2. Generate Manim code from script
    3. Clean and validate code
    4. Save code to file
    5. Render video using Manim CLI
    
    Args:
        q: Query object with topic field
        
    Returns:
        dict: Success/error message and metadata
    """
    try:
        print(f"\n🚀 Generating video for: {q.topic}\n")
        
        # STEP 1: Generate teaching script
        print("📝 Step 1: Generating teaching script...")
        script = generate_teaching_script(q.topic)
        print(f"✅ Script generated: {script.get('title')}")
        
        # STEP 2: Generate Manim code
        print("\n🎨 Step 2: Generating Manim code...")
        raw_code = generate_manim_from_script(script)
        print("✅ Manim code generated")
        
        # STEP 3: Clean and validate code
        print("\n🧹 Step 3: Cleaning and validating code...")
        code = clean_code(raw_code)
        print("✅ Code cleaned and validated")
        
        # STEP 4: Save code
        print("\n💾 Step 4: Saving code to file...")
        save_code(code)
        print("✅ Code saved successfully")
        
        # STEP 5: Render video
        print("\n🎬 Step 5: Rendering video...")
        success = render_video(quality="low_quality", fps=15)
        
        if not success or not video_exists():
            raise Exception("Video rendering failed - check Manim output above")
        
        # Store for user feedback
        current_generation["topic"] = q.topic
        current_generation["code"] = code
        current_generation["script"] = script
        
        print("\n✅ Video generation completed!\n")
        
        return {
            "message": "Video generated successfully",
            "topic": q.topic,
            "title": script.get("title"),
            "duration_seconds": script.get("duration_seconds", 120),
            "status": "completed"
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error: {error_msg}\n")
        return {
            "error": error_msg,
            "message": "Video generation failed. Please try again.",
            "status": "failed"
        }


@router.post("/refine")
async def refine_video(feedback: dict):
    """
    Apply user feedback to refine the generated video.
    
    Modifications applied:
    - timing: slower, faster, longer, shorter
    - appearance: dark, bright, larger, smaller
    - pacing: speed, pace
    
    Args:
        feedback: dict with "feedback" key containing user request
        
    Returns:
        dict: Success/error message
    """
    try:
        if not current_generation["code"]:
            raise Exception("No video to refine. Generate one first using /generate endpoint.")
        
        user_feedback = feedback.get("feedback", "").strip()
        if not user_feedback:
            raise Exception("Please provide feedback for refinement in 'feedback' field")
        
        print(f"\n🔄 Applying user feedback: {user_feedback}\n")
        
        # Apply feedback modifications
        refined_code = get_refinement_feedback(
            current_generation["code"],
            user_feedback
        )
        
        # Clean and save
        code = clean_code(refined_code)
        save_code(code)
        
        # Render updated video
        success = render_video(quality="low_quality", fps=15)
        
        if not success or not video_exists():
            raise Exception("Video re-rendering failed")
        
        # Update stored code
        current_generation["code"] = code
        
        print("\n✅ Video refined successfully!\n")
        
        return {
            "message": "Video refined successfully",
            "feedback_applied": user_feedback,
            "status": "refined"
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error: {error_msg}\n")
        return {
            "error": error_msg,
            "status": "failed"
        }


@router.get("/video")
def get_video():
    """
    Serve the most recently generated video file.
    
    Returns:
        FileResponse: MP4 video file or 404 error
    """
    video_path = get_video_path()
    
    if not os.path.exists(video_path):
        raise HTTPException(
            status_code=404,
            detail="Video not found. Generate a video first using /generate endpoint."
        )
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        headers={"Content-Disposition": "inline; filename=generated_video.mp4"}
    )


@router.get("/status")
def get_status():
    """
    Get current generation status and metadata.
    
    Returns:
        dict: Status information
    """
    return {
        "has_video": video_exists(),
        "current_topic": current_generation["topic"],
        "video_path": get_video_path() if video_exists() else None,
        "status": "ready" if video_exists() else "no_video"
    }


@router.post("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "video-generation-api"}