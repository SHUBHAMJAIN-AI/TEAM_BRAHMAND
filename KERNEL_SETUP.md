# 🎯 Jupyter Kernel Setup - Physics Violation Demo

## ✅ Kernel Created Successfully!

A **Python 3** Jupyter kernel has been created and registered on your system.

### Kernel Details
```
Name:        python3
Location:    /home/team/.local/share/jupyter/kernels/python3
Display:     Python 3
Status:      ✅ READY TO USE
```

---

## 🚀 How to Run the Demo

### Option 1: Simple Command (Recommended)
```bash
bash /home/team/RUN_DEMO.sh
```
This will start Jupyter and open the demo notebook automatically.

### Option 2: Command Line
```bash
jupyter notebook /home/team/demo.ipynb
```
Then open `http://localhost:8888` in your browser.

### Option 3: Jupyter Lab (Advanced)
```bash
jupyter lab /home/team/demo.ipynb
```

### Option 4: VSCode
1. Open VSCode
2. Open `/home/team/demo.ipynb`
3. Select kernel → Choose **Python 3**
4. Click cells to run them or use **Run All**

---

## 📋 What Gets Executed

The notebook includes these analysis cells:

1. **Load Pre-computed Results** (3,397 videos from VideoPhy-2)
2. **Analyze Physics Violations** (117 videos with score ≤ 2)
3. **Visualize Score Distribution** (histograms and pie charts)
4. **Show Violation Examples** (detailed explanations)
5. **List Local Grok Videos** (21 videos available for inference)
6. **Display Summary Statistics** (accuracy, correlation, breakdown)

---

## ✨ Features

✅ **No GPU Required** — Uses pre-computed results
✅ **Full Analysis** — All 3,397 videos analyzed
✅ **Interactive Visualizations** — Matplotlib charts
✅ **Example Violations** — See what physics is wrong
✅ **Next Steps** — Instructions for running full pipeline

---

## 🔧 Kernel Troubleshooting

### Problem: Kernel not found
**Solution**: Reinstall the kernel
```bash
python3 -m ipykernel install --user --name python3 --display-name "Python 3"
```

### Problem: Jupyter says "kernel not found"
**Solution**: Make sure you're using the right kernel name
```bash
jupyter kernelspec list  # Should show python3
```

### Problem: Missing packages
**Solution**: Install dependencies
```bash
pip install matplotlib pyyaml pillow numpy
```

### Problem: Port 8888 already in use
**Solution**: Use a different port
```bash
jupyter notebook --port 8889 /home/team/demo.ipynb
```

---

## 📊 What You'll See

When you run the notebook, you'll get:

```
📊 Cosmos-Reason2-2B Performance on VideoPhy-2 Test Set (3,397 videos)
   Accuracy: 35.4%
   Pearson Correlation: 0.3224
   Samples: 3,397

📈 Physics Score Distribution:
   Score 1:   24 videos (  0.7%) █
   Score 2:   93 videos (  2.7%) ██
   Score 3: 1925 videos ( 56.7%) ████████████████████████████
   Score 4: 1353 videos ( 39.8%) ███████████████████

⚠️  Physics Violations (score ≤ 2): 117 videos
```

Plus interactive charts and detailed violation examples.

---

## 🎬 Quick Demo Flow

1. **Run the script**
   ```bash
   bash /home/team/RUN_DEMO.sh
   ```

2. **Jupyter opens in browser**
   - Kernel: Python 3 (automatically selected)
   - File: demo.ipynb

3. **Click "Run All" or run cells individually**
   - Each cell takes 1-10 seconds
   - Full notebook: ~2 minutes

4. **See results**
   - Analysis of 3,397 videos
   - Visualizations
   - Violation examples

---

## 📝 Notebook Structure

| Cell | Duration | What It Does |
|------|----------|--------------|
| 1-2 | 5 sec | Load metrics and analyze data |
| 3-4 | 30 sec | Create visualizations (histograms, pie charts) |
| 5-6 | 10 sec | Show violation examples |
| 7-8 | 5 sec | List local Grok videos |
| 9-10 | 15 sec | Display summary statistics |
| 11-12 | 5 sec | Show output files |
| 13-14 | 5 sec | Explain methodology |

**Total**: ~2-3 minutes to run everything

---

## 🎯 Next Steps After Demo

### If you want to run full inference (requires GPU):
```bash
# 1. Install vLLM
pip install vllm

# 2. Run on Grok videos
python /home/team/physics_demo.py --videos /home/team/Sakib/syntheticVideos/ --mode grok

# 3. View updated results
open /home/team/physics_demo_output/demo.html
```

### If you want to extract frames:
```bash
python /home/team/demo_local_videos.py
open /home/team/physics_demo_output/local_videos_demo.html
```

---

## ✅ Verification

Check kernel status:
```bash
jupyter kernelspec list
python3 -c "import jupyter; print('✅ Jupyter working')"
```

Test basic functionality:
```bash
python3 -c "import matplotlib; import numpy; print('✅ All imports OK')"
```

---

**You're all set!** 🚀 Run the demo with:
```bash
bash /home/team/RUN_DEMO.sh
```
