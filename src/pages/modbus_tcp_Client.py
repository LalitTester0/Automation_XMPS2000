import time
from pywinauto.timings import always_wait_until
from config.settings import TIMEOUT_MED
from pywinauto import Desktop
from pywinauto.timings import wait_until_passes
import re






class NewModbusTCPDialog:
    def __init__(self, parent_win):
        self.parent = parent_win
        # the dialog is a child window of the main window
        self.dlg = parent_win.child_window(title_re=".*(Modbus TCP Client Settings|Add User|IO Model).*", control_type="Window")
        self.dlg.wait("visible", timeout=TIMEOUT_MED)
        
    def get_tagnamesofdropdown(self):
        try:
            dropdown_list = self.dlg.child_window(auto_id="1000", control_type="List")
            dropdown_list.wait("visible", timeout=20)
            list_wrapper = dropdown_list.wrapper_object()
            items = list_wrapper.items()
            val = []
            for item in items:
                text = item.window_text().strip()
                if text and text != "-Select Tag Name-":
                    val.append(text)   
            print(val)         
            return val
           
            
        except Exception as e:
            print(f"Could not read dropdown: {e}")
            print("Make sure the dropdown is expanded!")
            return []