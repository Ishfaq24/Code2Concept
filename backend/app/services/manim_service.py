import subprocess
import os
import sys

def save_code(code: str, request_id: str = "default"):
    """
    Save Manim code to file
    
    Args:
        code: The Manim scene code
        request_id: Unique request identifier (for potential future multi-request support)
    """
    file_path = "generated/scene.py"
    
    # Ensure directory exists
    os.makedirs("generated", exist_ok=True)
    
    # Write code
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    print(f"✅ Code saved to {file_path}")


def render_video(quality: str = "low_quality", fps: int = 15):
    """
    Render video using Manim CLI
    
    Args:
        quality: low_quality, medium_quality, or high_quality
        fps: Frames per second (default 15)
    """
    
    try:
        # Map quality to Manim flags
        quality_flag_map = {
            "low_quality": "-pql",
            "medium_quality": "-pqm",
            "high_quality": "-pqh"
        }
        
        flag = quality_flag_map.get(quality, "-pql")
        
        print(f"🎬 Rendering video ({quality}, {fps} fps)...")
        
        result = subprocess.run(
            [
                "manim",
                "generated/scene.py",
                "DemoScene",
                flag,
                f"--frame_rate={fps}"
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ Video rendered successfully")
            return True
        else:
            print(f"❌ Rendering failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Rendering timeout (exceeded 5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Rendering error: {e}")
        return False


def get_video_path() -> str:
    """Get path to the rendered video"""
    return "media/videos/scene/480p15/DemoScene.mp4"


def video_exists() -> bool:
    """Check if video file exists"""
    path = get_video_path()
    return os.path.exists(path)