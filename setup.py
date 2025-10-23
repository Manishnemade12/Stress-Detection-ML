#!/usr/bin/env python3
"""
Setup script for Stress Detection ML Project
This script helps with installation and setup of the project.
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8 and version.minor <= 11:
        print("✅ Python version is compatible")
        return True
    elif version.major == 3 and version.minor == 14:
        print("⚠️  Python 3.14 detected - may have compatibility issues")
        print("   Recommendation: Use Python 3.8-3.11 for best compatibility")
        return False
    else:
        print("❌ Python version may not be compatible")
        print("   Recommendation: Use Python 3.8-3.11")
        return False

def install_packages():
    """Install required packages"""
    print("\n📦 Installing packages...")
    
    # Try to install from requirements.txt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        print("🔄 Trying alternative installation...")
        
        # Try installing packages individually
        packages = [
            "Flask",
            "opencv-python-headless", 
            "numpy",
            "Pillow",
            "h5py"
        ]
        
        for package in packages:
            try:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
        
        # Try TensorFlow separately
        try:
            print("Installing TensorFlow...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tensorflow"])
            print("✅ TensorFlow installed")
        except subprocess.CalledProcessError:
            print("❌ TensorFlow installation failed")
            print("   You can use the demo version: python main_demo.py")
        
        return True

def check_webcam():
    """Check if webcam is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Webcam is available")
            cap.release()
            return True
        else:
            print("❌ Webcam not available")
            return False
    except ImportError:
        print("⚠️  OpenCV not installed - cannot check webcam")
        return False

def run_demo():
    """Run the demo version"""
    print("\n🚀 Running demo version...")
    try:
        subprocess.run([sys.executable, "main_demo.py"])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def main():
    """Main setup function"""
    print("🎯 Stress Detection ML Project Setup")
    print("=" * 40)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Install packages
    install_packages()
    
    # Check webcam
    webcam_ok = check_webcam()
    
    print("\n📋 Setup Summary:")
    print(f"Python compatibility: {'✅' if python_ok else '⚠️'}")
    print(f"Webcam available: {'✅' if webcam_ok else '❌'}")
    
    print("\n🚀 Next Steps:")
    print("1. For full functionality: python main.py")
    print("2. For demo version: python main_demo.py")
    print("3. Open browser: http://localhost:5000")
    
    # Ask if user wants to run demo
    if input("\n🤔 Would you like to run the demo now? (y/n): ").lower() == 'y':
        run_demo()

if __name__ == "__main__":
    main()
