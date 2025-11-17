# config.py
from pathlib import Path

# ----------------------------------------------------------------------
# Change ONLY the values below when you move the suite to another PC
# ----------------------------------------------------------------------
EXE_PATH = r"C:\Program Files (x86)\Messung Systems\XMPS2000_Setup\XMPS2000_1.100.exe"

# Default values for the “Add User Defined Tag” dialog
DEFAULT_TAG_NAME      = "YourTagValue"
DEFAULT_LOGICAL_ADDR  = ""          # leave empty or set a value

# Timeouts (seconds)
TIMEOUT_SHORT = 5
TIMEOUT_MED   = 10
TIMEOUT_LONG  = 30

# ----------------------------------------------------------------------
# You normally do **not** edit anything below this line
# ----------------------------------------------------------------------
BASE_DIR = Path(__file__).parent