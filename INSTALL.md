# Quick Installation Guide

## 🚀 Fastest Way to Get Started

### For Windows Users (Easiest)

1. **Double-click `run_demo.bat`** - This will run the demo version immediately
2. **Open your browser** and go to `http://localhost:5000`
3. **Allow webcam access** when prompted
4. **Enjoy the demo!**

### For Full ML Functionality

1. **Install Python 3.11** (recommended) from [python.org](https://python.org)
2. **Open Command Prompt** in the project folder
3. **Run setup script**: `python setup.py`
4. **Double-click `run_full.bat`** or run `python main.py`

## 🐍 Python Installation Issues?

If you're having trouble with Python 3.14:

### Option 1: Use Demo Version (No ML)
```bash
# Just run this - no installation needed!
python main_demo.py
```

### Option 2: Install Python 3.11
1. Download Python 3.11 from [python.org](https://python.org)
2. Install it alongside your current Python
3. Use `py -3.11` instead of `python` in commands

### Option 3: Use Conda
```bash
# If you have Anaconda/Miniconda
conda create -n stress-detection python=3.11
conda activate stress-detection
conda install tensorflow opencv flask
python main.py
```

## 🔧 Troubleshooting

### "ModuleNotFoundError" Errors
- **Solution**: Use demo version - `python main_demo.py`
- **Alternative**: Install Python 3.11 and try again

### "Could not capture frame" Error
- **Solution**: Close other apps using webcam (Zoom, Skype, etc.)
- **Check**: Webcam permissions in browser

### "Model file not found" Error
- **Solution**: Use demo version - `python main_demo.py`
- **Alternative**: Ensure `model/emotion_model.h5` exists

## 📱 How to Use

1. **Start the application** (demo or full version)
2. **Open browser** to `http://localhost:5000`
3. **Allow webcam access** when prompted
4. **Wait 5 seconds** for automatic emotion detection
5. **View your result** and personalized advice!

## 🎯 What You'll See

- **Live webcam feed** with emotion detection
- **Detected emotion** (Angry, Happy, Sad, etc.)
- **Personalized advice** based on your emotion
- **Beautiful dark theme** interface

## 🆘 Still Having Issues?

1. **Try the demo first**: `python main_demo.py`
2. **Check Python version**: `python --version`
3. **Use Python 3.11** if you have 3.14
4. **Check webcam permissions**
5. **Close other webcam apps**

---

**Remember**: The demo version works on any Python version and gives you the full experience with random emotions!
