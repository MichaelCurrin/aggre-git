"""
Config module.
"""
import os

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(SRC_DIR, 'var')
PR_CSV_PATH = os.path.join(OUTPUT_PATH, 'pr_report.csv')

try:
    from .configlocal import *
except ImportError:
    import os
    f_path = os.path.join(os.path.dirname(__file__), 'configlocal.py')
    raise ImportError(f"You need to create a local config file at {f_path}")

assert ACCESS_TOKEN, "Please set the ACCESS_TOKEN value in the local config" \
                     " file"
