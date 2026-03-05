# 🎬 Team Brahmand — Physics Violation Detection in AI Videos

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/) [![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)](https://jupyter.org/) [![NVIDIA Cosmos-Reason2](https://img.shields.io/badge/NVIDIA%20Cosmos-Reason2-76B900)](https://github.com/NVIDIA-AI-IOT/Cosmos) [![VideoPhy-2](https://img.shields.io/badge/Dataset-VideoPhy--2-green)](https://huggingface.co/datasets/videophysics/videophy2_test)

**An automated system for detecting and visually tagging physics violations in AI-generated videos using NVIDIA's Cosmos-Reason2 foundation model.**

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| **Videos Analyzed** | 3,397 (VideoPhy-2 test set) |
| **Physics Violations Detected** | 117 videos (3.4%) |
| **Model Accuracy** | 35.4% |
| **Pearson Correlation** | 0.322 |
| **Frames Extracted** | 15 annotated violation frames |
| **Generation Models** | 7 (Cogvideo, Cosmos, Hunyuan, Ray2, Sora, Videocrafter, WAN) |

---

## 🎯 Problem & Solution

### The Problem
> How do we automatically evaluate whether AI-generated videos follow physical laws?

AI video generators like Sora, Runway, and Grok can create impressive videos, but they often violate basic physics:
- Objects floating without support
- Penetrating solid surfaces
- Violating conservation of momentum
- Abrupt, unexplained changes in motion

**Current approaches:** Text-based violation reports (hard to visualize, requires careful reading)

### Our Solution
Use **Cosmos-Reason2** (a multimodal vision-language model) to:
1. **Score** each video on a 5-point physics plausibility scale
2. **Identify** videos with physics violations (score ≤ 2)
3. **Extract frames** from violation videos at key moments
4. **Annotate frames** with red borders and violation descriptions
5. **Generate** an interactive HTML gallery showing violations visually

---

## 🚀 Quick Start (No GPU Required)

### 1. View the Interactive Notebook
```bash
jupyter notebook demo.ipynb
```

This shows:
- 3,397 pre-computed results from VideoPhy-2 test set
- Score distribution visualization
- Real Cosmos-Reason2 reasoning from 5 violation examples
- 15 annotated frames from local Grok videos
- Video cleaning pipeline explanation

**Note:** All outputs are pre-embedded in the notebook. No GPU or downloads needed.

### 2. View the HTML Reports
```bash
# Main statistics and violation gallery
open physics_demo_output/demo.html

# Local Grok videos with annotated frames
open physics_demo_output/demo_local_videos.html
```

---

## 🏗️ Architecture

```
Input Video (MP4)
      ↓
┌─────────────────────────────────┐
│  Cosmos-Reason2-8B (vLLM)       │
│  Physics Evaluation Prompt      │
│  Inference: ~45 sec/video       │
└─────────────────────────────────┘
      ↓
Physics Score (1-5) + Reasoning Text
      ↓
      │ Is Score ≤ 2? (Violation)
      │
  ┌───┴─────────────────────┐
  │                         │
  YES                       NO
  │                         └──→ [Archive result]
  ↓
Frame Extraction (ffmpeg)
  ↓
Frame Annotation (PIL)
  ↓
Red Border + Violation Text
  ↓
HTML Gallery with Embedded Images
```

### Technology Stack

| Component | Tool |
|-----------|------|
| **Model** | NVIDIA Cosmos-Reason2-8B |
| **Inference** | vLLM (fast, efficient serving) |
| **Video Processing** | FFmpeg |
| **Image Annotation** | PIL/Pillow |
| **Data Format** | JSON |
| **Report Generation** | Jinja2 + HTML5/CSS3 |
| **Visualization** | Matplotlib |
| **Interactive Demo** | Jupyter Notebook |

---

## 📁 File Structure

```
.
├── README.md                              # This file
├── .gitignore                             # Git exclusions
├── demo.ipynb                             # Main interactive notebook (2.5MB)
│
├── physics_demo.py                        # Full vLLM inference pipeline
├── clean_video.py                         # Video cleaning (remove violation segments)
├── demo_local_videos.py                   # Process local Grok videos
├── extract_violation_frames.py            # Frame extraction & annotation
├── verify_demo.py                         # Verification/checks script
├── RUN_DEMO.sh                            # Shell script entrypoint
│
├── physics_demo_output/
│   ├── demo.html                          # Main HTML report
│   ├── results/
│   │   ├── results_combined.json          # All 3,397 inference results
│   │   └── summary.json                   # Performance metrics
│   └── local_frames/                      # 30 annotated frame images
│
├── Shubham/                               # Team baseline notebooks
│   ├── sigma_jamba_baseline_benchmarks_FIXED_1 (1).ipynb
│   └── sigma_jamba_baseline_benchmarks_v2_FIXED.ipynb
│
├── HACKATHON_DEMO_README.md               # Full technical documentation
├── SUBMISSION_SUMMARY.md                  # Executive summary
├── FINAL_SUBMISSION_GUIDE.md              # Submission guide
├── QUICK_REFERENCE.md                     # Command reference
├── DEMO_QUICK_START.txt                   # Quick start guide
├── KERNEL_SETUP.md                        # Jupyter kernel setup
└── VIEW_REASONING.md                      # How to view model reasoning

```

---

## 📊 Physics Evaluation Rubric

The model evaluates videos on 4 criteria:

| Criterion | Description |
|-----------|-------------|
| **Object Behavior** | Do objects deform naturally? Do rigid objects stay rigid? |
| **Motion & Forces** | Are gravity, inertia, momentum respected? |
| **Interactions** | Do objects collide realistically? No penetration? |
| **Temporal Consistency** | No abrupt, unexplained changes? Objects persist over time? |

**Score Scale:**
- **1** — Numerous violations (terrible)
- **2** — Major violations (poor)
- **3** — Noticeable issues (moderate)
- **4** — Only minor issues (good)
- **5** — Perfect adherence (excellent)

---

## 📈 Results Breakdown

### Score Distribution (3,397 videos)

```
Score 5 (Perfect):     2 videos  (0.1%)  ✅
Score 4 (Good):     1,353 videos (39.8%) ✅
Score 3 (Moderate): 1,925 videos (56.7%) ⚠️
Score 2 (Poor):       93 videos  (2.7%)  ❌
Score 1 (Severe):     24 videos  (0.7%)  ❌

Total Violations: 117 videos (≤ 2/5)
```

### Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 35.4% |
| Pearson Correlation | 0.3224 |
| Sample Size | 3,397 videos |
| Inference Speed | ~45 seconds/video with vLLM |
| GPU Memory | 24GB (2B model) / 32GB (8B model) |

---

## 🔧 Full Pipeline (GPU Required)

### Requirements
```bash
pip install vllm pyyaml pillow numpy matplotlib jinja2
sudo apt-get install ffmpeg ffprobe  # For video processing
```

### Step 1: Run Inference on Local Videos
```bash
python physics_demo.py \
    --videos Sakib/syntheticVideos/ \
    --output physics_demo_output/ \
    --mode grok
```

This:
- Loads Cosmos-Reason2-8B from cache (~20GB VRAM)
- Runs inference on 21 local Grok videos (~10-15 min)
- Saves results to `physics_demo_output/results/results_grok.json`

### Step 2: Extract & Annotate Violation Frames
```bash
python demo_local_videos.py
```

This:
- Extracts 3 key frames from each violation video
- Annotates with red border + violation marker
- Generates enhanced HTML report

### Step 3: Clean a Violation Video
```bash
python clean_video.py \
    --video Sakib/syntheticVideos/grok-video-0d58534b-c259-443a-bb9a-d77c0da767b6.mp4 \
    --output physics_demo_output/cleaned/ \
    --segments 3 \
    --threshold 2.0
```

This:
- Splits the video into 3 equal segments
- Scores each segment using Cosmos-Reason2-8B
- Removes segments with score ≤ 2.0
- Outputs cleaned video + JSON report with before/after stats

### Step 4: View Results
```bash
open physics_demo_output/demo.html
jupyter notebook demo.ipynb
```

---

## 📋 Key Features

✅ **Scale** — 3,397 videos evaluated across 7 different generation models
✅ **Visual Proof** — 15 annotated frames embedded in notebook
✅ **Real Reasoning** — Cosmos-Reason2 explanations for each violation
✅ **Automated Cleaning** — Remove bad segments for training data
✅ **Production Quality** — Error handling, logging, detailed reports
✅ **No GPU Needed** — View all results without GPU (pre-computed)
✅ **Reproducible** — All code is open-source, results are deterministic

---

## 🎬 Use Cases

- ✅ **Quality Control** — Evaluate synthetic videos before release
- ✅ **Training Data Filtering** — Remove physics violations from training datasets
- ✅ **Safety Evaluation** — Benchmark physics understanding in VLMs
- ✅ **Video Generation Improvement** — Identify failure modes in generators
- ✅ **Competitive Analysis** — Compare physics quality across video models

---

## 📚 References

### Key Papers & Resources
- **NVIDIA Cosmos**: [World Foundation Models for Physical AI](https://arxiv.org/abs/2411.02671)
- **Cosmos-Reason2**: [GitHub Repository](https://github.com/NVIDIA-AI-IOT/cosmos)
- **VideoPhy-2 Dataset**: [HuggingFace Hub](https://huggingface.co/datasets/videophysics/videophy2_test)
- **vLLM**: [Fast LLM Serving Framework](https://docs.vllm.ai)

### Model Downloads
- Cosmos-Reason2-8B: Auto-cached from Hugging Face Hub
- VideoPhy-2: Auto-downloaded from Hugging Face Datasets

---

## 🤝 Team Brahmand

Built with NVIDIA Cosmos-Reason2, evaluated on VideoPhy-2, powered by vLLM.

### Deliverables
- ✅ `demo.ipynb` — Interactive notebook with embedded visualizations
- ✅ `physics_demo.py` — Full inference pipeline
- ✅ `clean_video.py` — Video cleaning utility
- ✅ `physics_demo_output/` — Pre-computed results and reports

---

## 📝 License

This project uses publicly available models and datasets. See individual repositories for licensing.

---

## 🚀 Next Steps

1. **Clone the repo** and explore `demo.ipynb`
2. **Run the full pipeline** if you have a GPU
3. **Adapt for your videos** — use the scripts on your own video datasets
4. **Fine-tune Cosmos-Reason2** on domain-specific physics violations
5. **Deploy as a service** — API wrapper for third-party integrations

---

**Built for the NVIDIA Cosmos Hackathon 2026** 🎯
