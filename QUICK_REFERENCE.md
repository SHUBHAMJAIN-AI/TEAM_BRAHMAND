# 🎯 Quick Reference Card

## Submission Checklist

```bash
# 1. Run notebook to embed images (ONE TIME, before submitting)
jupyter notebook /home/team/demo.ipynb
# → Press Ctrl+Home, then "Kernel" → "Restart & Run All"
# → Wait for completion (~2-3 minutes)
# → Close browser when done

# 2. Verify images are embedded
python3 /home/team/verify_demo.py  # Should show all ✅

# 3. Submit /home/team/demo.ipynb
# That's it! File is self-contained with all images baked in
```

---

## What's in the Notebook Now

| Section | What It Shows |
|---------|---------------|
| 1-9 | Original analysis (metrics, visualizations, examples) |
| **10** | **📸 15 annotated violation frames (NEW)** |
| **11** | **🧠 Real Cosmos reasoning with HTML boxes (NEW)** |
| **12** | **🎬 Video cleaning pipeline explanation (NEW)** |

---

## Video Cleaning Script

```bash
# Basic usage (demo mode, no GPU needed)
python /home/team/clean_video.py \
    --video /home/team/Sakib/syntheticVideos/grok-video-0d58534b-c259-443a-bb9a-d77c0da767b6.mp4 \
    --output /home/team/physics_demo_output/cleaned/

# Full GPU mode (with Cosmos-Reason2-8B)
python /home/team/clean_video.py \
    --video <video_path> \
    --output <output_dir> \
    --segments 3 \
    --threshold 2.0

# Show help
python /home/team/clean_video.py --help
```

**Outputs**:
- `cleaned_<video_name>.mp4` — Cleaned video (violations removed)
- `cleaning_report_<video_name>.json` — Before/after statistics

---

## Demo Scripts (3 Ways to Present)

### 30 Seconds: Quick Visual Demo
```bash
jupyter notebook /home/team/demo.ipynb
# → Skip to Section 10 (Show 5 annotated frames)
# → Done!
```

### 5 Minutes: Full Story
```bash
jupyter notebook /home/team/demo.ipynb
# → Run all cells (full walkthrough)
# → Judges see: stats → metrics → images → reasoning → cleaning concept
```

### 10 Minutes: Technical Deep Dive
```bash
# 1. Open notebook, run all
jupyter notebook /home/team/demo.ipynb

# 2. Show cleaning in action
python /home/team/clean_video.py \
    --video /home/team/Sakib/syntheticVideos/grok-video-xxx.mp4 \
    --output /tmp/cleaned/

# 3. Show the report
cat /tmp/cleaned/cleaning_report_grok-video-xxx.json
```

---

## Files Ready to Submit

| File | Purpose | Size |
|------|---------|------|
| `/home/team/demo.ipynb` | **Main submission** (26 cells, images embedded) | ~5 MB |
| `/home/team/clean_video.py` | Video cleaning script (bonus) | 14 KB |
| `/home/team/FINAL_SUBMISSION_GUIDE.md` | Complete guide | 12 KB |

---

## Key Numbers to Mention

- **3,397** videos evaluated across 7 AI generators
- **117** physics violations identified (3.4%)
- **35.4%** accuracy on physics scoring
- **0.322** Pearson correlation
- **15** frames extracted and visually tagged
- **26** cells in final notebook
- **3** new sections with visual + reasoning content

---

## Common Questions

**Q: Do I need to run the notebook before submitting?**
A: Yes, once. Running it embeds all images into the `.ipynb` file. Then judges can view it without running it.

**Q: Can judges run the notebook themselves?**
A: Yes, but they don't need to. All outputs (images, reasoning) are already computed and embedded.

**Q: Does the cleaning script need GPU?**
A: No. It runs in "demo mode" with heuristic scoring if GPU isn't available. With GPU, it runs real Cosmos-Reason2-8B inference.

**Q: Which file do I actually submit?**
A: Just `/home/team/demo.ipynb`. It's completely self-contained. Optionally also include `clean_video.py` as bonus implementation.

**Q: How long will the notebook take to run?**
A: ~2-3 minutes for full execution (computing 3,397 results analysis + rendering 15 images).

---

## Execution Checklist

- [ ] Run: `jupyter notebook /home/team/demo.ipynb`
- [ ] "Kernel" → "Restart & Run All"
- [ ] Wait for completion
- [ ] Close notebook
- [ ] Verify: `python3 /home/team/verify_demo.py` ← all ✅
- [ ] Submit: `/home/team/demo.ipynb`
- [ ] Done! 🎉

---

**That's all you need!** The notebook is self-contained and ready for judges. ✨
