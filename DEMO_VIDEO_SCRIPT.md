# Team Brahmand — 2-Minute Demo Video Script

**Total Duration:** 2 minutes (~270 words)

---

## [0:00-0:15] — HOOK (15 seconds)

"AI video generators like Sora, Runway, and Grok can create amazing videos... but they often have physics problems. Objects floating in the air. People moving through walls. Impossible physics."

*[Show demo.ipynb title slide]*

"What if you could automatically detect and fix these violations?"

---

## [0:15-0:45] — THE PROBLEM (30 seconds)

"Here's the challenge: We have 3,397 AI-generated videos across 7 different generators. How do we automatically evaluate whether they follow physical laws?"

*[Show Section 1-6 of notebook - metrics, distributions]*

"Our team used **NVIDIA Cosmos-Reason2-8B** — a foundation model trained for physical reasoning — to score all 3,397 videos on a 5-point scale."

**Key Result:** We detected **117 physics violations** (3.4% of videos).

---

## [0:45-1:20] — THE SOLUTION (35 seconds)

"But here's our innovation — instead of just reporting violations as text, we visually tagged the frames."

*[Show Section 10: Visual Frame Gallery]*

"See these frames? Red borders mark where physics is wrong. We extracted annotated frames from violation videos so you can instantly see what's broken."

*[Show Section 11: Model Reasoning]*

"And look at what the model is thinking. These are real explanations from Cosmos-Reason2:

- 'The car is floating without support... violates gravity'
- 'The person is in mid-air... defies physical laws'

The model understands the physics violations!"

---

## [1:20-1:50] — THE PIPELINE (30 seconds)

"Here's where it gets powerful. We built a **video cleaning pipeline** that automatically removes violation segments."

*[Show Section 12: Video Cleaning Pipeline]*

"The pipeline:
1. **Splits** videos into segments
2. **Scores** each segment with Cosmos-Reason2
3. **Removes** segments with physics violations
4. **Reassembles** clean segments into training-ready video"

**Example:** A 6-second video with violations becomes 4 seconds of clean content — perfect for training data.

---

## [1:50-2:00] — IMPACT & CALL TO ACTION (10 seconds)

"**Our Results:**
- 3,397 videos analyzed
- 117 violations detected
- 35.4% model accuracy
- Visual frame tagging (our innovation!)

This solution enables quality control for synthetic media, better training data, and safety evaluation of AI-generated content."

*[Show GitHub repo]*

"All code is open-source on GitHub. Ready to improve AI-generated video quality? Check out our repository!"

---

## 🎬 FILMING TIPS

1. **Pacing:** Read slowly and naturally (not rushed)
2. **Screen Recording:** Use OBS Studio or similar to record screen + audio
3. **Visuals:** Pause at key sections to let viewers see the data
4. **Audio:** Use a microphone for clarity
5. **Background:** Keep simple (blank wall or professional setting)

---

## 📹 RECORDING COMMAND (Optional - using FFmpeg)

```bash
# Record screen + audio simultaneously
ffmpeg -f x11grab -video_size 1920x1080 -i :0 \
  -f pulse -i default \
  -pix_fmt yuv420p \
  -c:v libx264 -preset ultrafast \
  demo_video.mp4
```

Or use:
- **OBS Studio** (free, recommended)
- **ScreenFlow** (Mac)
- **Camtasia** (Windows/Mac)

---

## 📊 SCRIPT BREAKDOWN

| Section | Duration | Content |
|---------|----------|---------|
| Hook | 15s | Problem statement |
| Problem | 30s | Scale + metrics |
| Solution | 35s | Visual innovation |
| Pipeline | 30s | Cleaning mechanism |
| Impact | 10s | Results + CTA |
| **Total** | **2:00** | **270 words** |

---

## ✅ CHECKLIST BEFORE RECORDING

- [ ] Jupyter notebook open with demo.ipynb ready
- [ ] Microphone tested and working
- [ ] Screen at 1920x1080 resolution
- [ ] Quiet room (no background noise)
- [ ] Script printed or displayed on second monitor
- [ ] Recording software configured
- [ ] Run through script 1-2 times before recording
- [ ] Do a test 10-second recording first

---

**Good luck! You've got this! 🎬**
