#!/usr/bin/env python3
"""
Verify Physics Violation Demo is ready for hackathon submission.
Run this script to ensure all files are in place and data is correct.
"""

import json
import os
from pathlib import Path


def check_file(path, desc):
    """Check if a file exists and report size."""
    p = Path(path)
    if p.exists():
        size = p.stat().st_size
        if size > 1024 * 1024:
            size_str = f"{size / (1024**2):.1f} MB"
        elif size > 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size} B"
        print(f"  ✅ {desc:40s} {size_str:>10s}")
        return True
    else:
        print(f"  ❌ {desc:40s} NOT FOUND")
        return False


def main():
    print("=" * 80)
    print("  🎬 PHYSICS VIOLATION DEMO - VERIFICATION SCRIPT")
    print("=" * 80)

    all_ok = True

    # Check main scripts
    print("\n📁 Demo Scripts")
    print("-" * 80)
    all_ok &= check_file("physics_demo.py", "Main inference script")
    all_ok &= check_file("demo.ipynb", "Jupyter notebook")
    all_ok &= check_file("extract_violation_frames.py", "Frame extractor")

    # Check documentation
    print("\n📖 Documentation")
    print("-" * 80)
    all_ok &= check_file("HACKATHON_DEMO_README.md", "Full documentation")
    all_ok &= check_file("DEMO_QUICK_START.txt", "Quick start guide")

    # Check output reports
    print("\n📊 Generated Reports")
    print("-" * 80)
    all_ok &= check_file("physics_demo_output/demo.html", "Main HTML report")

    # Check results
    print("\n📝 Results & Metrics")
    print("-" * 80)
    all_ok &= check_file("physics_demo_output/results/results_combined.json", "Combined results")
    all_ok &= check_file("physics_demo_output/results/summary.json", "Metrics summary")

    # Load and verify results
    print("\n🔍 Data Integrity Checks")
    print("-" * 80)

    try:
        results_file = Path("physics_demo_output/results/results_combined.json")
        with open(results_file) as f:
            results = json.load(f)

        print(f"  ✅ Results JSON loads correctly")
        print(f"    • Total entries: {len(results):,}")

        # Check violation count
        violations = sum(1 for r in results if r.get("pred_score", 3) <= 2)
        print(f"    • Physics violations (score ≤ 2): {violations}")

        # Check score distribution
        scores = {}
        for r in results:
            s = int(r.get("pred_score", 3))
            scores[s] = scores.get(s, 0) + 1

        print(f"    • Score distribution:")
        for score in sorted(scores.keys()):
            pct = 100 * scores[score] / len(results)
            print(f"      - Score {score}: {scores[score]:4d} videos ({pct:5.1f}%)")

        if len(results) == 3397 and violations == 117:
            print(f"  ✅ Data matches expected values (3,397 results, 117 violations)")
        else:
            print(f"  ⚠️  Unexpected data counts")
            all_ok = False

    except Exception as e:
        print(f"  ❌ Error loading results: {e}")
        all_ok = False

    # Load and verify metrics
    try:
        metrics_file = Path("cookbook/cosmos-reason2/results/videophy2_test/summary.json")
        with open(metrics_file) as f:
            metrics = json.load(f)

        print(f"\n  ✅ Metrics loaded successfully")
        print(f"    • Accuracy: {metrics['accuracy']:.1%}")
        print(f"    • Pearson Correlation: {metrics['pearson_correlation']:.4f}")
        print(f"    • Samples: {metrics['num_samples']:,}")

        if metrics['accuracy'] > 0.35 and metrics['pearson_correlation'] > 0.3:
            print(f"  ✅ Metrics are reasonable")
        else:
            print(f"  ⚠️  Metrics seem low")

    except Exception as e:
        print(f"  ❌ Error loading metrics: {e}")
        all_ok = False

    # Check local videos
    print("\n🎥 Local Video Assets")
    print("-" * 80)

    grok_dir = Path("Sakib/syntheticVideos")
    if grok_dir.exists():
        grok_videos = list(grok_dir.glob("*.mp4"))
        print(f"  ✅ Found {len(grok_videos)} Grok videos")
        total_size = sum(v.stat().st_size for v in grok_videos)
        print(f"    • Total size: {total_size / (1024**2):.1f} MB")
    else:
        print(f"  ❌ Grok videos directory not found")
        all_ok = False

    # Check pre-computed results
    print("\n📦 Pre-computed VideoPhy-2 Results")
    print("-" * 80)

    results_dir = Path("cookbook/cosmos-reason2/results/videophy2_test")
    if results_dir.exists():
        json_files = list(results_dir.glob("*.json"))
        # Exclude summary.json
        json_files = [f for f in json_files if f.name != "summary.json"]
        print(f"  ✅ Found {len(json_files)} pre-computed results")
        total_size = sum(f.stat().st_size for f in json_files)
        print(f"    • Total size: {total_size / (1024**2):.1f} MB")
    else:
        print(f"  ❌ Pre-computed results directory not found")
        all_ok = False

    # Summary
    print("\n" + "=" * 80)
    if all_ok:
        print("  ✅ ALL CHECKS PASSED - DEMO IS READY FOR SUBMISSION!")
        print("=" * 80)
        print("\n  Next steps:")
        print("  1. Open demo.html in browser: /home/team/physics_demo_output/demo.html")
        print("  2. Run Jupyter notebook: jupyter notebook /home/team/demo.ipynb")
        print("  3. Review documentation: cat /home/team/DEMO_QUICK_START.txt")
        return 0
    else:
        print("  ❌ SOME CHECKS FAILED - PLEASE FIX ISSUES ABOVE")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    exit(main())
