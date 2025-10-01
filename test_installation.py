#!/usr/bin/env python3
"""
Test script to verify all dependencies are installed correctly
"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import trimesh
        print("✅ Trimesh imported successfully")
    except ImportError as e:
        print(f"❌ Trimesh import failed: {e}")
        return False
    
    try:
        import pygltflib
        print("✅ PyGLTF imported successfully")
    except ImportError as e:
        print(f"❌ PyGLTF import failed: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    return True

def test_local_modules():
    """Test if our local modules can be imported"""
    try:
        from cad_processor import CADProcessor
        print("✅ CAD Processor imported successfully")
    except ImportError as e:
        print(f"❌ CAD Processor import failed: {e}")
        return False
    
    try:
        from estimation_engine import EstimationEngine
        print("✅ Estimation Engine imported successfully")
    except ImportError as e:
        print(f"❌ Estimation Engine import failed: {e}")
        return False
    
    try:
        from database import EstimationDatabase
        print("✅ Database module imported successfully")
    except ImportError as e:
        print(f"❌ Database module import failed: {e}")
        return False
    
    try:
        from config import MATERIALS
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config module import failed: {e}")
        return False
    
    return True

def test_database_creation():
    """Test if database can be created"""
    try:
        from database import EstimationDatabase
        import os
        
        # Create test database in current directory
        test_db_path = "test_estimates.db"
        db = EstimationDatabase(test_db_path)
        print("✅ Database created successfully")
        
        # Clean up test database
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("✅ Test database cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Inticore Estimation Automation Installation")
    print("=" * 50)
    
    print("\n📦 Testing external dependencies...")
    deps_ok = test_imports()
    
    print("\n🔧 Testing local modules...")
    modules_ok = test_local_modules()
    
    print("\n🗄️ Testing database creation...")
    db_ok = test_database_creation()
    
    print("\n" + "=" * 50)
    if deps_ok and modules_ok and db_ok:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application, run:")
        print("streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\nTo install missing dependencies, run:")
        print("pip install -r requirements.txt")

