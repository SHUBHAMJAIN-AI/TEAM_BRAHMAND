#!/bin/bash
# Quick script to run the Physics Violation Detection Demo

echo "=================================="
echo "🎬 Physics Violation Detection Demo"
echo "=================================="
echo ""

# Check if Jupyter is installed
if ! command -v jupyter &> /dev/null; then
    echo "❌ Jupyter not found. Installing..."
    pip install -q jupyter ipykernel
fi

echo "✅ Jupyter kernel available:"
jupyter kernelspec list | grep python3

echo ""
echo "🚀 Starting Jupyter Lab..."
echo "   The notebook will open in your browser"
echo "   File: /home/team/demo.ipynb"
echo ""
echo "   If it doesn't open automatically, visit:"
echo "   http://localhost:8888"
echo ""

# Start Jupyter
jupyter notebook /home/team/demo.ipynb
