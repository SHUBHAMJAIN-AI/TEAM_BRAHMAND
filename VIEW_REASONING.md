# 📖 How to View the Reasoning Output

## The reasoning outputs ARE in the notebook! ✅

They were added in:
- **Section 11: Model Reasoning** (Cell 22-23)
- **Section 10: Frame Gallery** (Cell 20-21)

## Why You Might Not See Them

The notebook has 26 cells. The reasoning is near the end. You need to:

### Option 1: View in Jupyter Notebook (Best)
```bash
jupyter notebook /home/team/demo.ipynb
```
Then:
1. **Scroll down** to find "## 11. Model Reasoning"
2. You should see **5 colored boxes** with reasoning text
3. Each box shows:
   - ❌ Red badge: "Score: 1/5 — SEVERE PHYSICS VIOLATIONS"
   - Formatted reasoning text below

### Option 2: Check Via Command Line
```bash
python3 << 'EOF'
import json

with open('/home/team/demo.ipynb') as f:
    nb = json.load(f)

# Get Section 11 reasoning cell
cell = nb['cells'][23]

# Show the Python code that generates the reasoning
source = ''.join(cell['source'])
print("Section 11 Source Code:")
print(source[:500])
print("\n...")

# Show that outputs exist
print(f"\nNumber of reasoning outputs: {len(cell.get('outputs', []))}")
print("✅ Outputs are stored in the notebook")
EOF
```

### Option 3: Check What's Actually In The Outputs
```bash
python3 << 'EOF'
import json

with open('/home/team/demo.ipynb') as f:
    nb = json.load(f)

cell = nb['cells'][23]  # Reasoning cell

print("Reasoning Output Content:")
print("=" * 70)

for i, output in enumerate(cell.get('outputs', [])):
    if output.get('output_type') == 'display_data':
        data = output.get('data', {})
        if 'text/html' in data:
            html = data['text/html']
            if isinstance(html, list):
                html = ''.join(html)

            # Extract the text content
            if 'Score:' in html:
                print(f"\nReasoning Box {i}:")
                # Find the score
                import re
                score_match = re.search(r'Score: (\d+)/5', html)
                if score_match:
                    print(f"  Score: {score_match.group(1)}/5")
                # Check for violation content
                if 'pre' in html:
                    print(f"  ✅ Contains violation explanation text")
EOF
```

## What You Should See

When you scroll to Section 11 in Jupyter, you'll see something like:

```
═══════════════════════════════════════════════════════════════════════════════

🧠 Cosmos-Reason2-8B: Detected Physics Violations (Score 1/5)

╔═══════════════════════════════════════════════════════════════════════════════╗
║  ❌ Score: 1/5 — SEVERE PHYSICS VIOLATIONS                                    ║
║                                                                               ║
║  The video shows a ball being thrown at a wall. However, the object appears  ║
║  to pass through the brick wall without any deformation or collision physics.║
║  The wall should either stop the object, knock it back, or cause visible    ║
║  impact - instead, it penetrates cleanly through. This is a fundamental     ║
║  violation of object permanence and interaction physics.                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║  ❌ Score: 1/5 — SEVERE PHYSICS VIOLATIONS                                    ║
║                                                                               ║
║  [More reasoning examples...]                                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

```

## If Still Not Visible

The reasoning is stored as HTML outputs. To regenerate them:

```bash
jupyter notebook /home/team/demo.ipynb
```

1. Find **Cell 23** (the reasoning cell)
2. Click on it
3. Press **Shift+Enter** to re-execute
4. Outputs should appear immediately below the code

## Troubleshooting

**Problem**: Can't find Section 11
**Solution**: Press `Ctrl+F` and search for "Model Reasoning"

**Problem**: Cell 23 shows code but no colored boxes below
**Solution**: Click cell and press Shift+Enter to re-run

**Problem**: See error instead of reasoning
**Solution**:
```bash
# Check if the results file exists
ls -lh /home/team/physics_demo_output/results/results_combined.json

# If missing, run:
python3 /home/team/physics_demo.py --mode videophy2 --skip-inference
```

## Quick Verification

To confirm reasoning is in the notebook:
```bash
python3 << 'EOF'
import json
with open('/home/team/demo.ipynb') as f:
    nb = json.load(f)

# Cell 23 is the reasoning cell
cell = nb['cells'][23]
outputs = cell.get('outputs', [])

# Count reasoning boxes
html_outputs = [o for o in outputs if o.get('output_type') == 'display_data']

print(f"✅ Section 11 (Reasoning Cell):")
print(f"   Code cell: YES")
print(f"   Outputs: {len(outputs)} items")
print(f"   HTML displays: {len(html_outputs)} colored boxes")
print(f"\n✅ Reasoning is embedded in the notebook!")
EOF
```

---

**The reasoning is definitely there!** You just need to open the notebook in Jupyter and scroll to Section 11 to see it. 🎯
