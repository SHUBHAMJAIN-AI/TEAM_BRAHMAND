# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 📋 Project Overview

**Team Brahmand — Physics Violation Detection in AI Videos**

An automated system for detecting and visually tagging physics violations in AI-generated videos using NVIDIA's Cosmos-Reason2 foundation model. The project analyzes 3,397 AI-generated videos, detects 117 physics violations (3.4%), extracts annotated frames as visual evidence, and provides a video cleaning pipeline to remove violation segments for training data improvement.

### Key Achievement
- ✅ 3,397 videos analyzed across 7 generation models (Cogvideo, Cosmos, Hunyuan, Ray2, Sora, Videocrafter, WAN)
- ✅ 117 physics violations detected (score ≤ 2/5)
- ✅ 15 demo frames extracted and annotated with violation markers
- ✅ 35.4% accuracy on physics scoring, 0.322 Pearson correlation
- ✅ Video cleaning pipeline to remove bad segments

---

## 🏗️ Architecture Overview

### Core Pipeline
```
Input Video (MP4)
    ↓
[Cosmos-Reason2-8B via vLLM] — Physics Scoring (1-5) + Reasoning
    ↓
Filter: Score ≤ 2? (Violation Detected)
    ├─ YES → Frame Extraction (ffmpeg) → Frame Annotation (PIL) → HTML Gallery
    └─ NO  → Archive result
```

### Technology Stack
| Component | Tool | Purpose |
|-----------|------|---------|
| **Model** | NVIDIA Cosmos-Reason2-8B | Multimodal VLM for physics reasoning |
| **Inference** | vLLM | Fast, efficient GPU model serving |
| **Video Processing** | ffmpeg | Frame extraction, video splitting, concatenation |
| **Image Annotation** | PIL/Pillow | Add red borders and text to frames |
| **Data Processing** | NumPy, JSON | Results handling and metrics |
| **Visualization** | Matplotlib, Jinja2 | Score distributions and HTML reports |
| **Interactive Demo** | Jupyter Notebook | Self-contained submission with embedded outputs |

### Two-Part Solution
1. **Part 1: Detect & Visualize**
   - Score each video on 5-point physics plausibility scale
   - Identify violations (score ≤ 2)
   - Extract frames from violation videos
   - Annotate frames with red borders + violation descriptions
   - Generate interactive HTML gallery

2. **Part 2: Clean & Improve**
   - Split violation videos into segments
   - Score each segment independently
   - Remove bad segments (score ≤ 2.0)
   - Reassemble good segments
   - Output training-ready video without physics violations

---

## 📁 File Structure & Key Files

### Main Submission File
```
demo.ipynb (2.5 MB)
├── Sections 1-9: Data loading, analysis, metrics, evaluation methodology
├── Section 10: Inline frame gallery — 15 annotated violation frames from Grok videos
├── Section 11: Model reasoning — 5 real Cosmos-Reason2 physics violation explanations
├── Section 12: Video cleaning pipeline concept explanation
└── All outputs embedded as base64 for standalone viewing (no GPU required)
```

**Key: This is a self-contained notebook. All images and reasoning are embedded in the .ipynb file itself. Submit this single file.**

### Core Scripts
- **physics_demo.py** (21.5 KB)
  - Main inference pipeline using vLLM
  - Loads Cosmos-Reason2-8B model
  - Runs batch inference on video datasets
  - Outputs physics scores and reasoning text to `physics_demo_output/results/results_combined.json`
  - Usage: `python physics_demo.py --videos <dir> --output <dir> --mode grok`

- **clean_video.py** (14 KB)
  - End-to-end video cleaning pipeline
  - Splits video into N segments, scores each with Cosmos-Reason2, removes violations, reassembles
  - Generates before/after metrics in JSON report
  - Usage: `python clean_video.py --video <path> --output <dir> --segments 3 --threshold 2.0`

- **demo_local_videos.py** (7.2 KB)
  - Processes local Grok videos
  - Extracts 3 key frames per violation video
  - Annotates frames with red borders and descriptions
  - Generates enhanced HTML report with embedded frames

- **extract_violation_frames.py** (13.8 KB)
  - Advanced frame tagging tool
  - Can download violation videos from VideoPhy-2 dataset
  - Extracts frames and creates annotation gallery

### Data & Results
```
physics_demo_output/
├── demo.html (12.9 KB)
│   └── Pre-computed report: 3,397 videos, 117 violations, metrics
├── local_videos_demo.html (2.4 MB)
│   └── Local Grok videos with extracted annotated frames
├── results/
│   ├── results_combined.json (2.8 MB) — All 3,397 inference results with reasoning
│   └── summary.json — Metrics: accuracy, Pearson correlation, violation counts
└── local_frames/ — 15 extracted annotated JPG images from Grok videos
```

### Local Video Assets
```
Sakib/syntheticVideos/
└── 21 Grok-generated MP4 files (63.7 MB total)
```

### Documentation
- **README.md** — GitHub project overview with problem/solution, quick start, full pipeline
- **HACKATHON_DEMO_README.md** — Technical documentation for hackathon reviewers
- **SUBMISSION_SUMMARY.md** — Executive summary with key results and talking points
- **DEMO_VIDEO_SCRIPT.md** — 2-minute video script with talking points and recording tips
- **DEMO_QUICK_START.txt** — Quick reference for common commands
- **.gitignore** — Excludes videos, venv, credentials, external repos, system files

---

## 🚀 Common Development Tasks

### View Pre-computed Results (No GPU Required)
```bash
# View the main HTML report
open physics_demo_output/demo.html

# View local Grok videos with extracted frames
open physics_demo_output/local_videos_demo.html

# Run interactive notebook
jupyter notebook demo.ipynb
```

### Run Inference on Local Videos (GPU Required)
```bash
# Install dependencies first
pip install vllm pyyaml pillow numpy matplotlib jinja2
sudo apt-get install ffmpeg ffprobe

# Run inference on 21 local Grok videos (~10-15 min on H100)
python physics_demo.py \
    --videos Sakib/syntheticVideos/ \
    --output physics_demo_output/ \
    --mode grok

# Extract frames from violations
python demo_local_videos.py

# View enhanced results
open physics_demo_output/demo.html
```

### Clean a Violation Video (GPU Required)
```bash
python clean_video.py \
    --video Sakib/syntheticVideos/grok-video-XXX.mp4 \
    --output physics_demo_output/cleaned/ \
    --segments 3 \
    --threshold 2.0
```

### Update the Notebook with New Results
After running `physics_demo.py`:
```bash
# Re-execute notebook to embed new outputs
jupyter nbconvert --to notebook --execute --inplace demo.ipynb
```

### Prepare for Submission/Presentation
1. Ensure `demo.ipynb` has all outputs embedded (run cells if needed)
2. Verify all images show in Section 10 (15 annotated frames)
3. Verify reasoning text displays in Section 11 (5 violation examples)
4. Check `physics_demo_output/results/results_combined.json` has 3,397 entries
5. Run `verify_demo.py` to confirm all assets are in place

---

## 🔑 Physics Evaluation Rubric

The model scores videos 1-5 based on 4 criteria:

| Criterion | Description |
|-----------|-------------|
| **Object Behavior** | Do objects deform naturally? Rigid objects stay rigid? |
| **Motion & Forces** | Are gravity, inertia, momentum respected? |
| **Interactions** | Do objects collide realistically? No penetration? |
| **Consistency** | No abrupt, unexplained changes? Objects persist? |

**Score Scale:**
- **1** — Numerous violations (terrible)
- **2** — Major violations (poor)
- **3** — Noticeable issues (moderate)
- **4** — Only minor issues (good)
- **5** — Perfect adherence (excellent)

**Detection Threshold:** Score ≤ 2 = Physics Violation

---

## 💾 Data & Results Format

### results_combined.json Structure
```json
{
  "video_id": "grok-video-0d58534b-c259-443a-bb9a-d77c0da767b6",
  "pred_score": 1.5,
  "output_text": "1\nThe ball penetrates through the wall without deforming...",
  "generation_model": "grok",
  "violation": true
}
```

### Summary Metrics
```json
{
  "total_videos": 3397,
  "violations_detected": 117,
  "accuracy": 0.354,
  "pearson_correlation": 0.322,
  "score_distribution": {
    "score_5": 2,
    "score_4": 1353,
    "score_3": 1925,
    "score_2": 93,
    "score_1": 24
  }
}
```

---

## 🔧 GPU & Hardware Requirements

### Minimum
- **GPU Memory:** 24 GB (Cosmos-Reason2-2B) or 32 GB (Cosmos-Reason2-8B)
- **Model:** A100/H100 recommended
- **Inference Speed:** ~30-60 seconds per video

### Environment
- Python 3.8+
- vLLM 0.5.0+
- FFmpeg/FFprobe
- CUDA 11.8+ (for GPU inference)

### Model Caching
- Cosmos-Reason2-8B auto-downloads from Hugging Face Hub (~16 GB)
- Cached at `~/.cache/huggingface/hub/models--nvidia--Cosmos-Reason2-8B/`
- VideoPhy-2 videos auto-cached from Hugging Face Datasets

---

## 🎯 Hackathon Presentation Guide

### Quick Demo (30 seconds)
```bash
open physics_demo_output/demo.html      # Show summary + violations
open physics_demo_output/local_videos_demo.html  # Show annotated frames
```
Shows: 3,397 videos → 117 violations detected → Visual frame evidence

### Interactive Walkthrough (2-3 minutes)
```bash
jupyter notebook demo.ipynb
# Walk through Sections 1-12, highlighting:
# - Data scale and metrics
# - Score distribution visualization
# - Violation examples with real Cosmos-Reason2 reasoning
# - Annotated frames with red violation markers
# - Video cleaning pipeline concept
```

### Full Pipeline Demo (10-15 minutes)
```bash
# Run inference on local Grok videos (if GPU available)
python physics_demo.py --videos Sakib/syntheticVideos/ --mode grok

# Extract and annotate frames
python demo_local_videos.py

# Show the results
open physics_demo_output/demo.html
```

### Key Talking Points
- ✅ **Scale & Rigor:** 3,397 videos, multiple models, quantitative metrics with ground truth
- ✅ **Innovation:** Visual frame tagging instead of text-only reports
- ✅ **Practical Value:** Quality control for video generators, training data filtering, safety evaluation
- ✅ **Technical Excellence:** Production-ready code, error handling, modular design
- ✅ **Presentation Ready:** Beautiful HTML reports, interactive notebook, pre-computed demo

---

## 📝 Important Notes

### Submission Strategy
- **Single File Submission:** `demo.ipynb` contains everything needed (images, reasoning, results)
- **No GPU Required:** All outputs are pre-embedded; judges can view without running
- **Standalone:** Works offline; no external API calls or downloads needed during presentation

### Git Workflow
- Repository: https://github.com/SHUBHAMJAIN-AI/TEAM_BRAHMAND
- Commits tracked in full history
- Large files excluded: videos (*.mp4), venv, credentials
- Shubham baseline notebooks removed (not part of main project)

### Common Issues & Fixes

**Issue:** Section 11 reasoning not displaying
- **Fix:** Use `print()` instead of `display(HTML())` for text output visibility

**Issue:** FFprobe duration detection failing
- **Fix:** Use `-show_format` parameter and parse `duration=` field directly

**Issue:** GitHub push blocked by token detection
- **Fix:** Remove HuggingFace tokens before committing, use environment variables instead

---

## 🔗 References

- **NVIDIA Cosmos:** [Paper](https://arxiv.org/abs/2411.02671) | [GitHub](https://github.com/nvidia-cosmos/cosmos-reason2)
- **VideoPhy-2 Dataset:** [HuggingFace Hub](https://huggingface.co/datasets/videophysics/videophy2_test)
- **vLLM:** [Documentation](https://docs.vllm.ai)
- **FFmpeg:** [Official Docs](https://ffmpeg.org/documentation.html)

---

## 📊 Project Status

✅ **COMPLETE** — Ready for hackathon submission

- [x] Data collection & analysis (3,397 videos)
- [x] Inference pipeline (Cosmos-Reason2-8B via vLLM)
- [x] Violation detection & frame extraction
- [x] Visual annotation of violation frames
- [x] Interactive Jupyter notebook with embedded outputs
- [x] Video cleaning pipeline implementation
- [x] Comprehensive HTML reporting
- [x] GitHub repository organization
- [x] Documentation for judges and future developers
- [x] 2-minute demo video script

