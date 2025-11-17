#!/usr/bin/env python3
"""
Complete Installation and Run Script for Stress Detection ML Project
यह script सभी dependencies को सही versions के साथ install करेगा और project को run करेगा
This script analyzes the project, installs all dependencies with correct versions, and runs the project.
"""

import sys
import subprocess
import os
import platform
import re
import glob

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.RESET):
    """Print colored message"""
    print(f"{color}{message}{Colors.RESET}")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print_colored(f"\n🐍 Python Version: {version.major}.{version.minor}.{version.micro}", Colors.BLUE)
    
    if version.major == 3 and 8 <= version.minor <= 11:
        print_colored("✅ Python version is compatible", Colors.GREEN)
        return True
    elif version.major == 3 and version.minor == 14:
        print_colored("⚠️  Python 3.14 detected - may have compatibility issues", Colors.YELLOW)
        print_colored("   Recommendation: Use Python 3.8-3.11 for best compatibility", Colors.YELLOW)
        return False
    else:
        print_colored("❌ Python version may not be compatible", Colors.RED)
        print_colored("   Recommendation: Use Python 3.8-3.11", Colors.YELLOW)
        return False

def analyze_project_dependencies():
    """Analyze project files to find all dependencies"""
    print_colored("\n🔍 Analyzing project for dependencies...", Colors.BLUE)
    
    dependencies = set()
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Extract imports from Python files
    import_pattern = re.compile(r'^(?:from|import)\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = import_pattern.findall(content)
                for match in matches:
                    dependencies.add(match)
        except Exception as e:
            print_colored(f"   ⚠️  Could not read {py_file}: {e}", Colors.YELLOW)
    
    # Map module names to package names
    package_map = {
        'flask': 'Flask',
        'cv2': 'opencv-python-headless',
        'numpy': 'numpy',
        'tensorflow': 'tensorflow',
        'PIL': 'Pillow',
        'Image': 'Pillow',
        'sklearn': 'scikit-learn',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'h5py': 'h5py',
        'gunicorn': 'gunicorn'
    }
    
    # Built-in modules (don't need installation)
    builtin_modules = {
        'sys', 'os', 'json', 'random', 'base64', 'subprocess', 'platform',
        're', 'glob', 'collections', 'datetime', 'time', 'math', 'io', 'pathlib'
    }
    
    required_packages = set()
    for dep in dependencies:
        if dep not in builtin_modules:
            package_name = package_map.get(dep, dep)
            required_packages.add(package_name)
    
    print_colored(f"   ✅ Found {len(required_packages)} required packages", Colors.GREEN)
    return required_packages

def get_compatible_versions():
    """Get compatible package versions based on Python version"""
    version = sys.version_info
    
    # Base versions that work with Python 3.8-3.11
    versions = {
        "Flask": ">=2.3.0,<3.0.0",
        "numpy": ">=1.21.0,<2.0.0",
        "opencv-python-headless": ">=4.5.0",
        "Pillow": ">=9.0.0",
        "h5py": ">=3.7.0",
        "pandas": ">=1.3.0,<2.0.0",
        "scikit-learn": ">=1.0.0,<2.0.0",
        "matplotlib": ">=3.5.0",
        "gunicorn": ">=20.1.0"
    }
    
    # TensorFlow version based on Python version
    if version.minor == 8:
        versions["tensorflow"] = ">=2.10.0,<2.11.0"
    elif version.minor == 9:
        versions["tensorflow"] = ">=2.10.0,<2.12.0"
    elif version.minor == 10:
        versions["tensorflow"] = ">=2.10.0,<2.13.0"
    elif version.minor == 11:
        versions["tensorflow"] = ">=2.12.0,<2.16.0"
    else:
        versions["tensorflow"] = ">=2.10.0"
    
    return versions

def install_pip_upgrade():
    """Upgrade pip to latest version"""
    print_colored("\n⬆️  Upgrading pip...", Colors.BLUE)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_colored("   ✅ pip upgraded", Colors.GREEN)
    except:
        print_colored("   ⚠️  Could not upgrade pip, continuing...", Colors.YELLOW)

def install_packages():
    """Install all required packages with proper versions"""
    print_colored("\n" + "="*60, Colors.BOLD)
    print_colored("📦 INSTALLING DEPENDENCIES", Colors.BOLD)
    print_colored("="*60, Colors.RESET)
    
    # Upgrade pip first
    install_pip_upgrade()
    
    # Analyze project for dependencies
    project_deps = analyze_project_dependencies()
    
    # Get compatible versions
    versions = get_compatible_versions()
    
    # Core dependencies (always needed)
    core_dependencies = {
        "Flask": versions["Flask"],
        "numpy": versions["numpy"],
        "opencv-python-headless": versions["opencv-python-headless"],
        "Pillow": versions["Pillow"],
        "h5py": versions["h5py"]
    }
    
    # ML dependencies
    ml_dependencies = {
        "tensorflow": versions["tensorflow"]
    }
    
    # Training dependencies
    training_dependencies = {
        "pandas": versions["pandas"],
        "scikit-learn": versions["scikit-learn"],
        "matplotlib": versions["matplotlib"]
    }
    
    # Production dependencies
    production_dependencies = {
        "gunicorn": versions["gunicorn"]
    }
    
    # Combine all dependencies
    all_deps = {**core_dependencies, **ml_dependencies, **training_dependencies, **production_dependencies}
    
    # Install core dependencies first (always install these)
    print_colored("\n🔧 Installing Core Dependencies...", Colors.BLUE)
    for package, version_spec in core_dependencies.items():
        print_colored(f"   Installing {package}{version_spec}...", Colors.YELLOW)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}{version_spec}"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print_colored(f"   ✅ {package} installed", Colors.GREEN)
        except subprocess.CalledProcessError as e:
            print_colored(f"   ⚠️  Warning: Failed to install {package}", Colors.YELLOW)
    
    # Install ML dependencies
    print_colored("\n🤖 Installing ML Dependencies...", Colors.BLUE)
    for package, version_spec in ml_dependencies.items():
        print_colored(f"   Installing {package}{version_spec}...", Colors.YELLOW)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}{version_spec}"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print_colored(f"   ✅ {package} installed", Colors.GREEN)
        except subprocess.CalledProcessError as e:
            print_colored(f"   ⚠️  Warning: Failed to install {package}", Colors.YELLOW)
            print_colored("   💡 You can use demo version: python main_demo.py", Colors.YELLOW)
    
    # Install training dependencies
    print_colored("\n📊 Installing Training Dependencies...", Colors.BLUE)
    for package, version_spec in training_dependencies.items():
        print_colored(f"   Installing {package}{version_spec}...", Colors.YELLOW)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}{version_spec}"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print_colored(f"   ✅ {package} installed", Colors.GREEN)
        except subprocess.CalledProcessError as e:
            print_colored(f"   ⚠️  Warning: Failed to install {package}", Colors.YELLOW)
    
    # Install production dependencies
    print_colored("\n🚀 Installing Production Dependencies...", Colors.BLUE)
    for package, version_spec in production_dependencies.items():
        print_colored(f"   Installing {package}{version_spec}...", Colors.YELLOW)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}{version_spec}"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print_colored(f"   ✅ {package} installed", Colors.GREEN)
        except subprocess.CalledProcessError as e:
            print_colored(f"   ⚠️  Warning: Failed to install {package}", Colors.YELLOW)
    
    print_colored("\n✅ Dependency installation completed!", Colors.GREEN)

def verify_installation():
    """Verify that all critical packages are installed"""
    print_colored("\n🔍 Verifying Installation...", Colors.BLUE)
    
    critical_packages = {
        "flask": "Flask",
        "cv2": "opencv-python-headless",
        "numpy": "numpy",
        "PIL": "Pillow",
        "h5py": "h5py"
    }
    
    optional_packages = {
        "tensorflow": "tensorflow"
    }
    
    all_ok = True
    
    # Check critical packages
    for module, package in critical_packages.items():
        try:
            __import__(module)
            print_colored(f"   ✅ {package} - OK", Colors.GREEN)
        except ImportError:
            print_colored(f"   ❌ {package} - NOT FOUND", Colors.RED)
            all_ok = False
    
    # Check optional packages
    for module, package in optional_packages.items():
        try:
            __import__(module)
            print_colored(f"   ✅ {package} - OK", Colors.GREEN)
        except ImportError:
            print_colored(f"   ⚠️  {package} - NOT FOUND (Optional for demo)", Colors.YELLOW)
    
    return all_ok

def check_model_file():
    """Check if model file exists"""
    model_path = "model/emotion_model.h5"
    if os.path.exists(model_path):
        print_colored(f"   ✅ Model file found: {model_path}", Colors.GREEN)
        return True
    else:
        print_colored(f"   ⚠️  Model file not found: {model_path}", Colors.YELLOW)
        print_colored("   💡 You can use demo version: python main_demo.py", Colors.YELLOW)
        return False

def check_webcam():
    """Check if webcam is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print_colored("   ✅ Webcam is available", Colors.GREEN)
            cap.release()
            return True
        else:
            print_colored("   ⚠️  Webcam not available", Colors.YELLOW)
            return False
    except ImportError:
        print_colored("   ⚠️  OpenCV not installed - cannot check webcam", Colors.YELLOW)
        return False
    except Exception as e:
        print_colored(f"   ⚠️  Webcam check failed: {e}", Colors.YELLOW)
        return False

def run_project():
    """Run the project"""
    print_colored("\n" + "="*60, Colors.BOLD)
    print_colored("🚀 STARTING PROJECT", Colors.BOLD)
    print_colored("="*60, Colors.RESET)
    
    # Check if model exists
    model_exists = check_model_file()
    
    # Determine which version to run
    if model_exists:
        try:
            import tensorflow as tf
            print_colored("\n🎯 Running Full Version (with ML Model)...", Colors.BLUE)
            print_colored("   Open browser: http://localhost:5000", Colors.YELLOW)
            print_colored("   Press Ctrl+C to stop\n", Colors.YELLOW)
            
            # Run main.py
            os.system(f"{sys.executable} main.py")
        except ImportError:
            print_colored("\n⚠️  TensorFlow not available, running demo version...", Colors.YELLOW)
            print_colored("   Open browser: http://localhost:5000", Colors.YELLOW)
            print_colored("   Press Ctrl+C to stop\n", Colors.YELLOW)
            
            # Run main_demo.py
            os.system(f"{sys.executable} main_demo.py")
    else:
        print_colored("\n🎯 Running Demo Version (no ML Model required)...", Colors.BLUE)
        print_colored("   Open browser: http://localhost:5000", Colors.YELLOW)
        print_colored("   Press Ctrl+C to stop\n", Colors.YELLOW)
        
        # Run main_demo.py
        os.system(f"{sys.executable} main_demo.py")

def main():
    """Main setup function"""
    print_colored("\n" + "="*60, Colors.BOLD)
    print_colored("🎯 STRESS DETECTION ML - INSTALLATION & RUN SCRIPT", Colors.BOLD)
    print_colored("="*60, Colors.RESET)
    
    # Check Python version
    python_ok = check_python_version()
    
    if not python_ok:
        response = input("\n⚠️  Continue anyway? (y/n): ").lower()
        if response != 'y':
            print_colored("Installation cancelled.", Colors.RED)
            return
    
    # Install packages
    install_packages()
    
    # Verify installation
    verify_ok = verify_installation()
    
    if not verify_ok:
        print_colored("\n⚠️  Some critical packages failed to install", Colors.YELLOW)
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            print_colored("Installation cancelled.", Colors.RED)
            return
    
    # Check webcam
    print_colored("\n📹 Checking Webcam...", Colors.BLUE)
    check_webcam()
    
    # Check model file
    print_colored("\n🤖 Checking Model File...", Colors.BLUE)
    check_model_file()
    
    # Summary
    print_colored("\n" + "="*60, Colors.BOLD)
    print_colored("✅ INSTALLATION COMPLETE!", Colors.GREEN)
    print_colored("="*60, Colors.RESET)
    print_colored("\n📋 Summary:", Colors.BLUE)
    print_colored(f"   Python compatibility: {'✅' if python_ok else '⚠️'}", Colors.GREEN if python_ok else Colors.YELLOW)
    print_colored(f"   Dependencies installed: {'✅' if verify_ok else '⚠️'}", Colors.GREEN if verify_ok else Colors.YELLOW)
    
    # Ask to run project
    print_colored("\n🚀 Ready to run the project!", Colors.GREEN)
    response = input("Would you like to start the application now? (y/n): ").lower()
    
    if response == 'y':
        run_project()
    else:
        print_colored("\n💡 To run the project later:", Colors.BLUE)
        print_colored("   Full version: python main.py", Colors.YELLOW)
        print_colored("   Demo version: python main_demo.py", Colors.YELLOW)
        print_colored("   Open browser: http://localhost:5000", Colors.YELLOW)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n👋 Installation cancelled by user.", Colors.YELLOW)
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", Colors.RED)
        sys.exit(1)
