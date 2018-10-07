"""
Config module.
"""


try:
    from .configlocal import *
except ImportError:
    import os
    f_path = os.path.join(os.path.dirname(__file__), 'configlocal.py')
    raise ImportError(f"You need to create a local config file at {f_path}")

assert ACCESS_TOKEN, "Please set the ACCESS_TOKEN value in the local config" \
                     " file"
