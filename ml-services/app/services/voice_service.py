import os
import shutil
import subprocess
from typing import Optional

from dotenv import load_dotenv
from gtts import gTTS


load_dotenv()

AUDIO_DIR = os.path.join("media", "audio")


def generate_narration_audio(text: str, filename: str = "DemoScene_narration.mp3") -> str:
    """Generate an MP3 narration file from the given text.

    Args:
        text: Narration script text.
        filename: Output audio filename inside media/audio.

    Returns:
        Absolute or relative path to the generated audio file.
    """

    if not text or not text.strip():
        raise ValueError("Narration text is empty")

    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_path = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang="en")
    tts.save(audio_path)

    print(f"✅ Narration audio saved to {audio_path}")
    return audio_path


def merge_audio_with_video(
    video_path: str,
    audio_path: str,
    output_path: Optional[str] = None,
) -> Optional[str]:
    """Merge the given audio file with a video using ffmpeg.

    Video stream is copied, audio is encoded as AAC. Returns the
    output path on success, or None on failure.
    """

    if not os.path.exists(video_path):
        print(f"❌ Video file not found for merge: {video_path}")
        return None
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found for merge: {audio_path}")
        return None

    if output_path is None:
        base, ext = os.path.splitext(video_path)
        output_path = f"{base}_voiced{ext}"

    # Ensure target directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Resolve ffmpeg path: prefer FFMPEG_PATH from env, else fall back to PATH
    ffmpeg_cmd = os.getenv("FFMPEG_PATH") or "ffmpeg"

    # On Windows, give a clear message if ffmpeg is not found
    if shutil.which(ffmpeg_cmd) is None:
        print("❌ ffmpeg not found. Set FFMPEG_PATH in backend/.env or add ffmpeg to PATH.")
        print("   Example: FFMPEG_PATH=C:/ffmpeg/bin/ffmpeg.exe")
        return None

    cmd = [
        ffmpeg_cmd,
        "-y",  # overwrite without asking
        "-i",
        video_path,
        "-i",
        audio_path,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        output_path,
    ]

    print("🎧 Merging audio and video with ffmpeg:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ ffmpeg merge failed")
        print(result.stderr[:1000])
        return None

    print(f"✅ Voiced video created at {output_path}")
    return output_path
