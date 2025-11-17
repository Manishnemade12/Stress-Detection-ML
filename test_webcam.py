#!/usr/bin/env python3
"""
Webcam Test Script
This script tests webcam access and helps diagnose camera issues.
"""

import cv2
import sys

def test_webcam():
    """Test webcam access"""
    print("🎥 Testing webcam access...")
    print("=" * 40)
    
    # Test different camera indices
    for i in range(5):
        print(f"Testing camera index {i}...")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            print(f"✅ Camera {i} is available")
            
            # Try to read a frame
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera {i} can capture frames")
                print(f"   Frame size: {frame.shape}")
                
                # Show frame for 3 seconds
                print(f"   Showing camera {i} feed for 3 seconds...")
                cv2.imshow(f'Camera {i}', frame)
                cv2.waitKey(3000)
                cv2.destroyAllWindows()
                
                cap.release()
                return i
            else:
                print(f"❌ Camera {i} cannot capture frames")
        else:
            print(f"❌ Camera {i} is not available")
        
        cap.release()
    
    print("\n❌ No working camera found!")
    return None

def check_webcam_permissions():
    """Check for common webcam issues"""
    print("\n🔍 Checking for common webcam issues...")
    print("=" * 40)
    
    # Check if OpenCV can access cameras
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ OpenCV can access camera 0")
            cap.release()
        else:
            print("❌ OpenCV cannot access camera 0")
    except Exception as e:
        print(f"❌ OpenCV error: {e}")
    
    print("\n💡 Troubleshooting tips:")
    print("1. Close other applications using the webcam (Zoom, Skype, Teams, etc.)")
    print("2. Check Windows camera permissions in Settings > Privacy > Camera")
    print("3. Try running as administrator")
    print("4. Restart your computer if camera was recently connected")
    print("5. Check if camera drivers are installed")

def main():
    """Main test function"""
    print("🎯 Webcam Test for Stress Detection ML")
    print("=" * 50)
    
    # Test webcam access
    working_camera = test_webcam()
    
    if working_camera is not None:
        print(f"\n✅ SUCCESS: Camera {working_camera} is working!")
        print("You can now run the emotion detection app.")
    else:
        print("\n❌ FAILURE: No working camera found")
        check_webcam_permissions()
        print("\n🔄 You can still use the demo version with random emotions:")
        print("   python main_demo.py")

if __name__ == "__main__":
    main()
