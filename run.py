#!/usr/bin/env python3
"""
Entry point for the CV & Cover Letter Generator application.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import streamlit.cli as stcli
    sys.argv = ["streamlit", "run", "app/main.py"]
    sys.exit(stcli.main())