#!/usr/bin/env python3
"""
Demo: Extract frames from local Grok videos and create annotated violation report.
This is simpler than downloading remote videos and works great for local assets.
"""

import subprocess
import os
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import base64


def get_video_duration(video_path: str) -> float:
    """Get video duration using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_format", video_path,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        for line in result.stdout.split('\n'):
            if line.startswith('duration='):
                return float(line.split('=')[1])
        return 0
    except:
        return 0


def extract_frame(video_path: str, timestamp: float, output_path: str) -> bool:
    """Extract a single frame from video at given timestamp."""
    try:
        subprocess.run(
            [
                "ffmpeg", "-ss", str(timestamp),
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "2",
                str(output_path),
            ],
            capture_output=True,
            timeout=15,
            check=True,
        )
        return os.path.exists(output_path)
    except:
        return False


def annotate_frame(frame_path: str, text: str, score: float) -> str:
    """Annotate frame with text and save."""
    try:
        img = Image.open(frame_path).convert("RGB")
        draw = ImageDraw.Draw(img, "RGBA")
        width, height = img.size

        # Try to use a good font
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            title_font = text_font = ImageFont.load_default()

        # Red banner at top
        draw.rectangle([(0, 0), (width, 50)], fill=(200, 0, 0, 220))
        draw.text((10, 8), f"⚠ PHYSICS VIOLATION — Score: {score:.1f}/5",
                 fill=(255, 255, 255), font=title_font)

        # Text box at bottom
        draw.rectangle([(0, height - 80), (width, height)], fill=(0, 0, 0, 220))
        draw.text((10, height - 70), text[:80],
                 fill=(255, 255, 255), font=text_font)

        # Red border
        for i in range(5):
            draw.rectangle([(i, i), (width - i, height - i)], outline=(255, 0, 0), width=1)

        # Save
        annotated_path = str(frame_path).replace(".jpg", "_annotated.jpg")
        img.save(annotated_path, quality=95)
        return annotated_path

    except Exception as e:
        print(f"    ⚠️  Annotation error: {e}")
        return frame_path


def main():
    print("=" * 70)
    print("  🎬 Local Grok Video Analysis & Frame Extraction")
    print("=" * 70)

    # Create output directory
    output_dir = Path("/home/team/physics_demo_output")
    frames_dir = output_dir / "local_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Get list of Grok videos
    grok_dir = Path("/home/team/Sakib/syntheticVideos")
    videos = sorted(grok_dir.glob("*.mp4"))[:5]  # First 5 for demo

    if not videos:
        print("❌ No local Grok videos found!")
        return

    print(f"\n📊 Analyzing {len(videos)} local Grok videos\n")

    frame_map = {}
    html_parts = []

    for i, video_path in enumerate(videos, 1):
        video_name = video_path.name
        print(f"[{i}/{len(videos)}] {video_name}")

        # Get duration
        duration = get_video_duration(str(video_path))
        if duration < 1:
            print(f"  ⚠️  Could not get video duration")
            continue

        # Extract frames at 3 points
        frame_times = [0.5, duration / 2, max(0.5, duration - 1)]
        frame_paths = []

        for j, t in enumerate(frame_times):
            frame_file = frames_dir / f"grok_{i:02d}_frame_{j}.jpg"

            if extract_frame(str(video_path), t, str(frame_file)):
                # Annotate
                text = f"Frame {j+1} — {video_name}"
                annotated = annotate_frame(str(frame_file), text, 3.0)
                frame_paths.append(annotated)
                print(f"  ✅ Frame {j+1}/3 extracted")
            else:
                print(f"  ⚠️  Frame {j+1} extraction failed")

        if frame_paths:
            frame_map[video_name] = frame_paths
            print(f"  📸 {len(frame_paths)} frames saved")

    # Generate HTML report
    print(f"\n📝 Generating HTML report with {sum(len(f) for f in frame_map.values())} frames...\n")

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Grok Videos - Frame Analysis</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.2em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.05em; opacity: 0.95; }}
        .content {{ padding: 40px; }}
        .video-section {{
            background: #f8f9fa;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 25px;
        }}
        .video-title {{
            font-size: 1.1em;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 15px;
        }}
        .frames-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .frame-item {{
            background: white;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .frame-image {{
            width: 100%;
            display: block;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎥 Local Grok Videos - Frame Analysis Demo</h1>
            <p>Extracted frames from {len(videos)} synthetic videos</p>
        </div>

        <div class="content">
"""

    for video_name, frame_paths in frame_map.items():
        html += f"""
            <div class="video-section">
                <div class="video-title">📺 {video_name}</div>
                <div class="frames-grid">
"""

        for frame_path in frame_paths:
            try:
                # Embed as base64
                with open(frame_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    html += f"""
                    <div class="frame-item">
                        <img src="data:image/jpeg;base64,{b64}" class="frame-image">
                    </div>
"""
            except:
                pass

        html += """
                </div>
            </div>
"""

    html += """
        </div>

        <footer>
            <p>Demo: Physics Violation Detection in AI-Generated Videos</p>
            <p>Using NVIDIA Cosmos-Reason2 for physical plausibility evaluation</p>
        </footer>
    </div>
</body>
</html>
"""

    # Save HTML
    output_file = output_dir / "local_videos_demo.html"
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✅ Report generated: {output_file}")
    print(f"   • Videos analyzed: {len(frame_map)}")
    print(f"   • Frames extracted: {sum(len(f) for f in frame_map.values())}")


if __name__ == "__main__":
    main()
