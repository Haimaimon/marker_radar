#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Market Radar - Run Once
========================
Runs ONE poll cycle and exits.

Perfect for:
- PythonAnywhere scheduled tasks
- Cron jobs
- Testing

Usage:
    python run_once.py

Environment Variables:
    MAX_ITERATIONS=1  (default: 1, set to 0 for infinite like app.py)
"""

import sys
import os

# Set max iterations to 1 (run once and exit)
os.environ["MAX_ITERATIONS"] = os.getenv("MAX_ITERATIONS", "1")

# Import and run the main app
# But it will exit after one iteration
if __name__ == "__main__":
    from app import main
    main()

