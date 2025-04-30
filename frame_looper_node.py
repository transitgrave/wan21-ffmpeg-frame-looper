import os
import subprocess
from PIL import Image
from pathlib import Path
import numpy as np
import comfy.utils
import folder_paths

class ExtractVideoFrame:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"multiline": False}),
                "frame_type": (["first", "last"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("frame_image",)
    FUNCTION = "extract_frame"
    CATEGORY = "WAN2.1 Tools"

    def extract_frame(self, video_path, frame_type):
        video_path = Path(video_path.strip('"'))

        # Determine the frame extraction command
        temp_output = Path(folder_paths.get_temp_directory()) / "temp_frame.png"
        if frame_type == "first":
            cmd = [
                "ffmpeg", "-y", "-i", str(video_path),
                "-vf", "select=eq(n\\,0)",
                "-vframes", "1", str(temp_output)
            ]
        elif frame_type == "last":
            cmd = [
                "ffmpeg", "-y", "-sseof", "-1", "-i", str(video_path),
                "-vframes", "1", str(temp_output)
            ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Load the frame image into PIL and convert for ComfyUI
        image = Image.open(temp_output).convert("RGB")
        image_np = np.array(image).astype(np.float32) / 255.0
        image_np = np.expand_dims(image_np, axis=0)

        return (image_np,)

NODE_CLASS_MAPPINGS = {
    "ExtractVideoFrame": ExtractVideoFrame,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExtractVideoFrame": "WAN2.1 FFmpeg Frame Extractor",
}
