import os
import sys
import ctypes

def check_admin_privileges():
    """Check if the application has administrative privileges."""
    try:
        if sys.platform == 'win32':
            # Windows
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # Unix-based systems (Linux, macOS)
            return os.geteuid() == 0
    except Exception:
        return False