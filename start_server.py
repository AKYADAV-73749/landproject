#!/usr/bin/env python3
"""
Startup script for the Land Registry Blockchain System
"""

import os
import sys
import time
import webbrowser
from threading import Timer

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://127.0.0.1:5000')

def main():
    print("🔗 Starting Land Registry Blockchain System")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ['app.py', 'blockchain.py', 'land_registry.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    
    # Check if templates and static directories exist
    if not os.path.exists('templates'):
        print("❌ Templates directory not found")
        return False
    
    if not os.path.exists('static'):
        print("❌ Static directory not found")
        return False
    
    print("✅ Templates and static directories found")
    
    # Import and check Flask
    try:
        import flask
        print(f"✅ Flask {flask.__version__} is available")
    except ImportError:
        print("❌ Flask is not installed. Please run: pip install Flask")
        return False
    
    # Import and check our modules
    try:
        from templates.land_registry import LandRegistry
        from templates.blockchain import Blockchain
        print("✅ All modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    print("\n🚀 Starting Flask server...")
    print("📋 Available at:")
    print("   • Main Application: http://127.0.0.1:5000")
    print("   • Test Page: simple_test.html")
    print("\n⚡ Features available:")
    print("   • Register new land parcels")
    print("   • Transfer land ownership")
    print("   • View all land records")
    print("   • Explore blockchain transactions")
    print("   • Verify blockchain integrity")
    
    print("\n🌐 Opening browser in 2 seconds...")
    
    # Open browser after delay
    Timer(2.0, open_browser).start()
    
    # Start the Flask app
    try:
        from templates.app import app
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        print("\n❌ Failed to start the server")
        sys.exit(1)
