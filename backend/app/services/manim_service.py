"""
Manim rendering service.
Handles saving Manim scene code and rendering videos with Manim CLI.
"""

import subprocess
import os
import sys


def save_code(code: str, scene_name: str = "DemoScene") -> bool:
    """
    Save Manim scene code to file.
    
    Args:
        code: The Manim Python scene code
        scene_name: Name of the scene class (default: DemoScene)
        
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        file_path = "generated/scene.py"
        
        # Ensure directory exists
        os.makedirs("generated", exist_ok=True)
        
        # Write code to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        # Verify file was written
        if not os.path.exists(file_path):
            print(f"❌ Failed to create {file_path}")
            return False
        
        file_size = os.path.getsize(file_path)
        print(f"✅ Code saved to {file_path} ({file_size} bytes)")
        return True
        
    except Exception as e:
        print(f"❌ Error saving code: {e}")
        return False


def render_video(
    quality: str = "low_quality",
    fps: int = 15,
    timeout: int = 300
) -> bool:
    """
    Render video using Manim CLI.
    
    Args:
        quality: Video quality (low_quality, medium_quality, high_quality)
        fps: Frames per second (default 15)
        timeout: Timeout in seconds (default 300 = 5 minutes)
        
    Returns:
        bool: True if rendering succeeded, False otherwise
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
        print(f"   Timeout: {timeout}s")
        
        # Run Manim command
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
            timeout=timeout
        )
        
        if result.returncode == 0:
            print("✅ Video rendered successfully")
            return True
        else:
            print(f"❌ Rendering failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error output:\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Rendering timeout (exceeded {timeout}s)")
        return False
    except Exception as e:
        print(f"❌ Rendering error: {e}")
        return False


def get_video_path() -> str:
    """
    Get the path to the rendered video file.
    
    Returns:
        str: Path to DemoScene.mp4
    """
    return "media/videos/scene/480p15/DemoScene.mp4"


def video_exists() -> bool:
    """
    Check if a video file has been successfully rendered.
    
    Returns:
        bool: True if video exists, False otherwise
    """
    path = get_video_path()
    exists = os.path.exists(path)
    
    if exists:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"   📹 Video found: {path} ({size_mb:.2f} MB)")
    
    return exists


def cleanup_old_renders(keep_latest: int = 3) -> None:
    """
    Clean up old render artifacts to save disk space.
    
    Args:
        keep_latest: Number of latest renders to keep
    """
    
    try:
        media_dir = "media/videos/scene/480p15/partial_movie_files/DemoScene"
        
        if not os.path.exists(media_dir):
            return
        
        # Get all files sorted by modification time
        files = sorted(
            [f for f in os.listdir(media_dir) if f.endswith('.mp4')],
            key=lambda f: os.path.getctime(os.path.join(media_dir, f)),
            reverse=True
        )
        
        # Remove old files
        for old_file in files[keep_latest:]:
            try:
                os.remove(os.path.join(media_dir, old_file))
                print(f"   🗑️ Cleaned up old file: {old_file}")
            except Exception as e:
                print(f"   ⚠️ Failed to remove {old_file}: {e}")
                
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")