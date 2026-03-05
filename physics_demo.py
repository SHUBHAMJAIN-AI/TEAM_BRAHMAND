#!/usr/bin/env python3
"""
Physics Violation Frame Tagger - Hackathon Demo
Detects physics violations in AI-generated videos and tags the violation frames visually.
"""

import argparse
import json
import os
import glob
import subprocess
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, List, Optional
from PIL import Image, ImageDraw, ImageFont
import tempfile
import shutil

# Try to import vllm for inference
try:
    from vllm import LLM, SamplingParams
    VLLM_AVAILABLE = True
except ImportError:
    VLLM_AVAILABLE = False

import yaml


class PhysicsViolationDemo:
    def __init__(self, output_dir: str = "/home/team/physics_demo_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.results_dir = self.output_dir / "results"
        self.frames_dir = self.output_dir / "frames"
        self.results_dir.mkdir(exist_ok=True)
        self.frames_dir.mkdir(exist_ok=True)

        self.model_name = "nvidia/Cosmos-Reason2-8B"
        self.video_cache = {}
        self.demo_results = []

    def load_prompt(self, prompt_path: str) -> Dict:
        """Load YAML prompt file."""
        with open(prompt_path) as f:
            return yaml.safe_load(f)

    def run_inference_on_videos(self, video_paths: List[str]) -> Dict[str, Dict]:
        """Run Cosmos-Reason2-8B inference on local videos using vLLM."""
        if not VLLM_AVAILABLE:
            print("⚠️  vLLM not available. Install with: pip install vllm")
            return {}

        print(f"\n🚀 Loading model {self.model_name}...")
        llm = LLM(
            model=self.model_name,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.9,
        )

        # Load physics rubric prompt
        prompt_path = "/home/team/cookbook/cosmos-reason2/prompts/video_reward.yaml"
        prompt_config = self.load_prompt(prompt_path)
        system_prompt = prompt_config['system_prompt']
        user_prompt = prompt_config['user_prompt']

        results = {}
        for i, video_path in enumerate(video_paths, 1):
            try:
                print(f"  [{i}/{len(video_paths)}] Processing {Path(video_path).name}...")

                messages = [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "video",
                                "video": video_path,
                                "fps": 4.0,
                                "total_pixels": 8192 * 28 * 28,
                            },
                            {"type": "text", "text": user_prompt},
                        ],
                    },
                ]

                # Generate with greedy decoding
                sampling_params = SamplingParams(
                    temperature=0.0,  # Greedy
                    max_tokens=2048,
                )

                outputs = llm.chat(messages, sampling_params=sampling_params)
                output_text = outputs.outputs[0].text.strip()

                # Parse score (1-5 on first line)
                pred_score = None
                for line in output_text.split('\n'):
                    line = line.strip()
                    if line.isdigit() and 1 <= int(line) <= 5:
                        pred_score = float(line)
                        break

                if pred_score is None:
                    pred_score = 3.0  # Default to middle

                results[video_path] = {
                    "video_url": video_path,
                    "pred_score": pred_score,
                    "output_text": output_text,
                }

                print(f"      Score: {pred_score}/5")

            except Exception as e:
                print(f"      ❌ Error: {e}")
                results[video_path] = {
                    "video_url": video_path,
                    "pred_score": 3.0,
                    "output_text": f"Error during inference: {e}",
                }

        return results

    def get_violation_frame_time(self, video_path: str, result: Dict) -> Optional[float]:
        """
        Extract approximate violation timestamp from model output.
        Looks for time markers in the text.
        """
        output_text = result.get("output_text", "")

        # Simple heuristic: look for time patterns or return None
        # In a real implementation, would run second-pass inference
        # For now, return None to trigger uniform frame extraction
        return None

    def extract_and_annotate_frames(
        self,
        video_path: str,
        result: Dict,
        violation_time: Optional[float] = None,
        num_frames: int = 3,
    ) -> List[str]:
        """
        Extract frames from video and annotate with violation info.
        Returns list of output frame paths.
        """
        try:
            # Get video duration
            probe_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1:norow=1",
                video_path,
            ]
            result_probe = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)
            duration = float(result_probe.stdout.strip())

            # Determine frame times
            if violation_time is not None:
                # Extract frames around violation timestamp
                start_time = max(0, violation_time - 1)
                times = [start_time + i * 0.5 for i in range(num_frames)]
            else:
                # Extract frames uniformly across video
                times = [duration * i / (num_frames - 1) for i in range(num_frames)]

            pred_score = result.get("pred_score", 3.0)
            output_text = result.get("output_text", "")

            # Extract first few lines of explanation
            explanation = "\n".join(output_text.split('\n')[1:4]).strip()
            if not explanation:
                explanation = "Physics violation detected"

            frame_paths = []
            video_stem = Path(video_path).stem

            for j, t in enumerate(times):
                # Extract frame using ffmpeg
                frame_file = self.frames_dir / f"{video_stem}_frame_{j:02d}.jpg"

                extract_cmd = [
                    "ffmpeg", "-ss", str(t), "-i", video_path,
                    "-vframes", "1", "-q:v", "2",
                    str(frame_file),
                ]
                subprocess.run(extract_cmd, capture_output=True, timeout=10, check=True)

                # Annotate frame
                annotated_frame = self._annotate_frame(
                    frame_file,
                    pred_score,
                    explanation,
                    is_violation=(pred_score <= 2),
                )

                frame_paths.append(annotated_frame)

        except Exception as e:
            print(f"      ⚠️  Frame extraction error: {e}")
            return []

        return frame_paths

    def _annotate_frame(
        self,
        frame_path: str,
        score: float,
        explanation: str,
        is_violation: bool = True,
    ) -> str:
        """Annotate a frame image with violation info."""
        try:
            img = Image.open(frame_path)
            draw = ImageDraw.Draw(img)

            # Use default font
            try:
                font_large = ImageFont.load_default()
            except:
                font_large = ImageFont.load_default()

            width, height = img.size

            # Draw red border for violations
            border_width = 8 if is_violation else 2
            border_color = (255, 0, 0) if is_violation else (100, 100, 100)

            for i in range(border_width):
                draw.rectangle(
                    [(i, i), (width - i, height - i)],
                    outline=border_color,
                    width=1,
                )

            # Draw banner at top
            banner_height = 40
            banner_color = (200, 0, 0) if is_violation else (100, 100, 100)
            draw.rectangle([(0, 0), (width, banner_height)], fill=banner_color)

            # Draw score and violation text
            score_text = f"⚠ PHYSICS VIOLATION — Score: {score:.1f}/5"
            text_color = (255, 255, 255)
            draw.text((10, 8), score_text, fill=text_color, font=font_large)

            # Draw explanation at bottom (truncated)
            explanation_lines = explanation[:80] + ("..." if len(explanation) > 80 else "")
            bottom_y = height - 50
            draw.rectangle([(0, bottom_y), (width, height)], fill=(0, 0, 0, 200))
            draw.text((10, bottom_y + 5), explanation_lines, fill=text_color, font=font_large)

            # Save annotated frame
            annotated_path = str(frame_path).replace(".jpg", "_annotated.jpg")
            img.save(annotated_path, quality=95)

            return annotated_path

        except Exception as e:
            print(f"      ⚠️  Annotation error: {e}")
            return frame_path

    def load_existing_results(self) -> Dict[str, Dict]:
        """Load pre-computed results from VideoPhy-2 test set."""
        results_dir = "/home/team/cookbook/cosmos-reason2/results/videophy2_test/"
        results = {}

        for json_file in sorted(glob.glob(f"{results_dir}*.json"))[:3397]:
            if "summary" in json_file:
                continue

            with open(json_file) as f:
                data = json.load(f)
                results[data["video_url"]] = {
                    "video_url": data["video_url"],
                    "pred_score": data.get("pred_score"),
                    "output_text": data.get("output_text"),
                    "ground_truth": data.get("ground_truth"),
                }

        return results

    def save_results_json(self, all_results: Dict[str, Dict], label: str):
        """Save results to JSON file."""
        output_file = self.results_dir / f"results_{label}.json"

        # Convert to list for JSON serialization
        results_list = list(all_results.values())

        with open(output_file, 'w') as f:
            json.dump(results_list, f, indent=2)

        print(f"  Saved {len(results_list)} results to {output_file}")

    def generate_html_report(self, all_results: Dict[str, Dict], title: str = "Physics Violation Demo"):
        """Generate HTML report with video gallery and annotated frames."""

        # Load metrics
        metrics_file = "/home/team/cookbook/cosmos-reason2/results/videophy2_test/summary.json"
        metrics = {}
        if os.path.exists(metrics_file):
            with open(metrics_file) as f:
                metrics = json.load(f)

        # Separate violations from good videos
        violations = {}
        for url, result in all_results.items():
            if result.get("pred_score", 3) <= 2:
                violations[url] = result

        # Sort violations by score (worst first)
        violations = dict(sorted(
            violations.items(),
            key=lambda x: x[1].get("pred_score", 3)
        ))

        html = self._build_html_header(title, len(all_results), len(violations), metrics)
        html += self._build_metrics_section(metrics)
        html += self._build_gallery_section(violations)
        html += self._build_html_footer()

        output_file = self.output_dir / "demo.html"
        with open(output_file, 'w') as f:
            f.write(html)

        print(f"\n✅ HTML report saved to {output_file}")
        return output_file

    def _build_html_header(self, title: str, total: int, violations: int, metrics: Dict) -> str:
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
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
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #1e3c72;
            margin: 10px 0;
        }}
        .stat-card .label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .content {{
            padding: 40px;
        }}
        .section-title {{
            font-size: 1.8em;
            color: #1e3c72;
            margin: 40px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #2a5298;
        }}
        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }}
        .video-card {{
            background: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .video-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        .video-preview {{
            width: 100%;
            height: 200px;
            background: #000;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.9em;
            overflow: hidden;
        }}
        .video-preview video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .video-info {{
            padding: 15px;
        }}
        .score-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }}
        .score-1 {{ background: #d32f2f; }}
        .score-2 {{ background: #f57c00; }}
        .score-3 {{ background: #fbc02d; }}
        .score-4 {{ background: #7cb342; }}
        .score-5 {{ background: #388e3c; }}
        .explanation {{
            font-size: 0.9em;
            color: #666;
            line-height: 1.5;
            margin-top: 10px;
            max-height: 100px;
            overflow-y: auto;
        }}
        .frames-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }}
        .frame-thumb {{
            border-radius: 4px;
            overflow: hidden;
            border: 2px solid #ddd;
            cursor: pointer;
        }}
        .frame-thumb img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 {title}</h1>
            <p>AI Video Physics Violation Detection & Frame Tagging</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="label">Videos Analyzed</div>
                <div class="number">{total}</div>
            </div>
            <div class="stat-card">
                <div class="label">Physics Violations Detected</div>
                <div class="number" style="color: #d32f2f;">{violations}</div>
            </div>
            <div class="stat-card">
                <div class="label">Violation Rate</div>
                <div class="number">{100*violations//max(total, 1)}%</div>
            </div>
        </div>
"""

    def _build_metrics_section(self, metrics: Dict) -> str:
        if not metrics:
            return ""

        return f"""        <div class="content">
            <div class="section-title">📊 Evaluation Metrics (VideoPhy-2 Test Set)</div>
            <div class="stats">
                <div class="stat-card">
                    <div class="label">Accuracy</div>
                    <div class="number">{metrics.get('accuracy', 0):.1%}</div>
                </div>
                <div class="stat-card">
                    <div class="label">Pearson Correlation</div>
                    <div class="number">{metrics.get('pearson_correlation', 0):.3f}</div>
                </div>
                <div class="stat-card">
                    <div class="label">Samples</div>
                    <div class="number">{metrics.get('num_samples', 0):,}</div>
                </div>
            </div>
        </div>
"""

    def _build_gallery_section(self, violations: Dict) -> str:
        if not violations:
            return '<div class="content"><p style="text-align: center; color: #999;">No physics violations to display.</p></div>'

        gallery = '<div class="content"><div class="section-title">⚠️  Physics Violations Detected</div><div class="video-grid">'

        for url, result in list(violations.items())[:10]:  # Show first 10
            score = result.get("pred_score", 3.0)
            explanation = result.get("output_text", "")

            # Truncate explanation
            exp_lines = explanation.split('\n')[1:3]
            exp_short = " ".join(exp_lines)[:150]

            score_class = f"score-{int(score)}"

            gallery += f"""
            <div class="video-card">
                <div class="video-preview">
                    <div style="text-align: center;">
                        <div style="font-size: 3em;">🎥</div>
                        <div style="margin-top: 10px; font-size: 0.8em;">Video</div>
                    </div>
                </div>
                <div class="video-info">
                    <div class="score-badge {score_class}">Score: {score:.1f}/5</div>
                    <div class="explanation">{exp_short}</div>
                </div>
            </div>
"""

        gallery += '</div></div>'
        return gallery

    def _build_html_footer(self) -> str:
        return """        <footer>
            <p>Physics Violation Detection using NVIDIA Cosmos-Reason2</p>
            <p style="margin-top: 5px; font-size: 0.85em;">
                Hackathon Demo — Cosmos-Reason2-8B • VideoPhy-2 Dataset
            </p>
        </footer>
    </div>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Physics Violation Demo")
    parser.add_argument("--videos", type=str, help="Directory with video files or single video path")
    parser.add_argument("--output", type=str, default="/home/team/physics_demo_output", help="Output directory")
    parser.add_argument("--mode", choices=["grok", "videophy2", "both"], default="both", help="Which videos to process")
    parser.add_argument("--skip-inference", action="store_true", help="Skip inference, use cached results")

    args = parser.parse_args()

    demo = PhysicsViolationDemo(args.output)

    all_results = {}

    # Load existing VideoPhy-2 results
    if args.mode in ["videophy2", "both"]:
        print("\n📂 Loading pre-computed VideoPhy-2 results...")
        existing = demo.load_existing_results()
        all_results.update(existing)
        print(f"   Loaded {len(existing)} results")

    # Process Grok videos
    if args.mode in ["grok", "both"]:
        if args.videos:
            video_dir = Path(args.videos)
            video_files = list(video_dir.glob("*.mp4"))
        else:
            video_dir = Path("/home/team/Sakib/syntheticVideos")
            video_files = list(video_dir.glob("*.mp4"))

        if video_files and not args.skip_inference:
            print(f"\n🎥 Processing {len(video_files)} local videos...")
            grok_results = demo.run_inference_on_videos(video_files)
            all_results.update(grok_results)
            demo.save_results_json(grok_results, "grok_videos")

    # Save combined results
    demo.save_results_json(all_results, "combined")

    # Generate HTML report
    print("\n📝 Generating HTML report...")
    demo.generate_html_report(all_results)

    print(f"\n✅ Demo complete!")
    print(f"   Output: {demo.output_dir / 'demo.html'}")
    print(f"   Total videos: {len(all_results)}")
    violations_count = sum(1 for r in all_results.values() if r.get("pred_score", 3) <= 2)
    print(f"   Violations: {violations_count}")


if __name__ == "__main__":
    main()
