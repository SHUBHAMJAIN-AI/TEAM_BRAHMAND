#!/usr/bin/env python3
"""
Extract frames from physics violation videos and annotate them.
This script:
1. Loads JSON results with violation scores
2. For videos with score ≤ 2, downloads the video
3. Extracts key frames
4. Annotates with violation info
5. Generates an enhanced HTML report with embedded frames
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error
from PIL import Image, ImageDraw, ImageFont
import base64
import time


class FrameExtractor:
    def __init__(self, output_dir: str = "/home/team/physics_demo_output"):
        self.output_dir = Path(output_dir)
        self.frames_dir = self.output_dir / "violation_frames"
        self.frames_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = tempfile.mkdtemp()

    def load_results(self, results_file: str) -> List[Dict]:
        """Load JSON results file."""
        with open(results_file) as f:
            return json.load(f)

    def download_video(self, url: str, output_path: str, timeout: int = 30) -> bool:
        """Download a video from URL."""
        try:
            print(f"  ⬇️  Downloading {Path(url).name[-30:]}...")
            # urlretrieve with proper timeout handling
            import socket
            socket.setdefaulttimeout(timeout)
            urllib.request.urlretrieve(url, output_path)
            socket.setdefaulttimeout(None)
            return True
        except Exception as e:
            print(f"  ⚠️  Download failed: {e}")
            return False

    def get_video_duration(self, video_path: str) -> Optional[float]:
        """Get video duration using ffprobe."""
        try:
            result = subprocess.run(
                [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1:norow=1",
                    video_path,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return float(result.stdout.strip())
        except:
            return None

    def extract_frame_at_time(
        self,
        video_path: str,
        timestamp: float,
        output_path: str,
    ) -> bool:
        """Extract a single frame at a specific timestamp."""
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-ss", str(timestamp),
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

    def annotate_frame(
        self,
        frame_path: str,
        score: float,
        explanation: str,
    ) -> str:
        """Annotate a frame with violation info and return annotated path."""
        try:
            img = Image.open(frame_path)
            img = img.convert("RGB")
            draw = ImageDraw.Draw(img, "RGBA")

            width, height = img.size

            # Try to load a good font, fallback to default
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            except:
                title_font = text_font = ImageFont.load_default()

            # Add dark overlay at top for title
            draw.rectangle([(0, 0), (width, 60)], fill=(200, 0, 0, 200))
            draw.text((10, 8), f"⚠  Physics Violation  •  Score: {score:.1f}/5",
                     fill=(255, 255, 255), font=title_font)

            # Add explanation box at bottom
            explanation = explanation.strip()
            if len(explanation) > 120:
                explanation = explanation[:120] + "..."

            draw.rectangle([(0, height - 80), (width, height)], fill=(0, 0, 0, 200))
            draw.text((10, height - 70), explanation,
                     fill=(255, 255, 255), font=text_font)

            # Add red border
            draw.rectangle([(0, 0), (width - 1, height - 1)], outline=(255, 0, 0), width=6)

            # Save
            annotated_path = str(frame_path).replace(".jpg", "_annotated.jpg")
            img.save(annotated_path, quality=95)
            return annotated_path

        except Exception as e:
            print(f"    Annotation error: {e}")
            return frame_path

    def process_violations(self, results_file: str, max_videos: int = 10) -> Dict[str, List[str]]:
        """
        Process violation videos: download, extract frames, annotate.
        Returns dict of {video_url: [frame_paths]}
        """
        results = self.load_results(results_file)

        # Filter violations and sort by score
        violations = [r for r in results if r.get("pred_score", 3) <= 2]
        violations = sorted(violations, key=lambda x: x.get("pred_score", 3))

        print(f"\n🎯 Found {len(violations)} physics violations")
        print(f"📸 Processing first {min(max_videos, len(violations))} violations...\n")

        frame_map = {}
        processed = 0

        for violation in violations[:max_videos]:
            if processed >= max_videos:
                break

            url = violation.get("video_url")
            score = violation.get("pred_score", 3.0)
            explanation = violation.get("output_text", "Physics violation detected")

            # Extract summary from explanation (first meaningful line after score)
            exp_lines = explanation.split('\n')[1:3]
            summary = " ".join(exp_lines).strip()[:100]

            print(f"[{processed + 1}/{max_videos}] Score: {score:.1f}/5")

            # Download video
            video_filename = f"violation_{processed:03d}.mp4"
            video_path = os.path.join(self.temp_dir, video_filename)

            if not self.download_video(url, video_path, timeout=30):
                print(f"  ❌ Skipped")
                continue

            # Get duration
            duration = self.get_video_duration(video_path)
            if not duration:
                print(f"  ❌ Could not get duration")
                continue

            # Extract frames at 3 points: start, middle, end
            frame_times = [0.5, duration / 2, max(0.5, duration - 1)]
            frame_paths = []

            for i, t in enumerate(frame_times):
                frame_file = self.frames_dir / f"violation_{processed:03d}_frame_{i}.jpg"

                if self.extract_frame_at_time(video_path, t, str(frame_file)):
                    # Annotate frame
                    annotated = self.annotate_frame(str(frame_file), score, summary)
                    frame_paths.append(annotated)
                    print(f"  ✅ Extracted frame {i + 1}/3")
                else:
                    print(f"  ⚠️  Frame {i + 1} extraction failed")

            if frame_paths:
                frame_map[url] = frame_paths
                processed += 1

            # Clean up video
            try:
                os.remove(video_path)
            except:
                pass

        return frame_map

    def image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 data URI."""
        try:
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except:
            return ""

    def generate_html_with_frames(self, frame_map: Dict[str, List[str]]) -> str:
        """Generate enhanced HTML report with embedded annotated frames."""

        html_parts = ["""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Physics Violations — Frame Analysis</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #d32f2f 0%, #f57c00 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.95; }
        .content { padding: 40px; }
        .violation-group {
            background: #f8f9fa;
            border: 2px solid #ffebee;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .violation-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #d32f2f;
            margin-bottom: 15px;
        }
        .frames-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        .frame-container {
            background: white;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .frame-image {
            width: 100%;
            display: block;
            border-bottom: 1px solid #eee;
        }
        .frame-info {
            padding: 10px;
            font-size: 0.9em;
            color: #666;
        }
        footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 0.9em;
        }
        .stat {
            display: inline-block;
            background: white;
            padding: 15px 25px;
            border-radius: 6px;
            margin: 10px 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 1.8em;
            font-weight: bold;
            color: #d32f2f;
        }
        .stat-label {
            font-size: 0.85em;
            color: #999;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Physics Violations — Frame Analysis</h1>
            <p>AI Video Physics Detection with NVIDIA Cosmos-Reason2</p>
        </div>

        <div class="content">
            <div style="text-align: center; margin-bottom: 30px;">
                <div class="stat">
                    <div class="stat-number">"""]

        html_parts.append(str(len(frame_map)))
        html_parts.append("""</div>
                    <div class="stat-label">Violations with Frames</div>
                </div>
            </div>
""")

        # Add violation groups
        for i, (url, frames) in enumerate(frame_map.items(), 1):
            html_parts.append(f"""
            <div class="violation-group">
                <div class="violation-title">Violation #{i}: Detected Physics Anomaly</div>
                <div class="frames-grid">
""")

            for j, frame_path in enumerate(frames):
                frame_basename = Path(frame_path).name
                try:
                    # Try to embed as data URI for self-contained HTML
                    with open(frame_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        html_parts.append(f"""
                    <div class="frame-container">
                        <img src="data:image/jpeg;base64,{b64}" class="frame-image" alt="Violation frame {j+1}">
                        <div class="frame-info">Frame {j+1} — Violation visible</div>
                    </div>
""")
                except:
                    # Fallback: reference local file
                    html_parts.append(f"""
                    <div class="frame-container">
                        <img src="violation_frames/{frame_basename}" class="frame-image" alt="Violation frame {j+1}">
                        <div class="frame-info">Frame {j+1} — Violation visible</div>
                    </div>
""")

            html_parts.append("""
                </div>
            </div>
""")

        html_parts.append("""
        </div>

        <footer>
            <p>Physics Violation Detection using NVIDIA Cosmos-Reason2-8B</p>
            <p style="margin-top: 5px; font-size: 0.85em;">
                VideoPhy-2 Dataset • Hackathon Demo
            </p>
        </footer>
    </div>
</body>
</html>
""")

        return "".join(html_parts)


def main():
    print("=" * 60)
    print("Physics Violation Frame Extractor")
    print("=" * 60)

    extractor = FrameExtractor()

    # Process violations from the combined results
    results_file = "/home/team/physics_demo_output/results/results_combined.json"

    if not os.path.exists(results_file):
        print(f"❌ Results file not found: {results_file}")
        print("   Run physics_demo.py first to generate results")
        return

    # Extract frames from violation videos
    frame_map = extractor.process_violations(results_file, max_videos=5)

    if not frame_map:
        print("\n❌ No frames extracted")
        return

    # Generate HTML with embedded frames
    print("\n📝 Generating HTML report with embedded frames...")
    html_content = extractor.generate_html_with_frames(frame_map)

    output_file = extractor.output_dir / "violation_frames_demo.html"
    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"\n✅ Report generated: {output_file}")
    print(f"   Violations with frames: {len(frame_map)}")
    print(f"   Total frames extracted: {sum(len(f) for f in frame_map.values())}")


if __name__ == "__main__":
    main()
