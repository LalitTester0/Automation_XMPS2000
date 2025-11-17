# pages/dialogs.py
import time
from pywinauto.timings import always_wait_until
from config import TIMEOUT_MED
from pywinauto import Desktop


class NewProjectDialog:
    """The small dialog that appears after clicking New Project."""
    def __init__(self, parent_win):
        self.parent = parent_win
        # the dialog is a child window of the main window
        self.dlg = parent_win.child_window(title_re=".*(Add User|IO Model).*", control_type="Window")
        self.dlg.wait("visible", timeout=TIMEOUT_MED)

    @property
    def txt_tag(self):
        return self.dlg.child_window(auto_id="textBoxTag", control_type="Edit")

    @property
    def txt_logical_address(self):
        return self.dlg.child_window(auto_id="textBoxLogicalAddress", control_type="Edit")

    @property
    def btn_save(self):
        return self.dlg.child_window(auto_id="btnSave", control_type="Button")

    @property
    def btn_cancel(self):
        return self.dlg.child_window(auto_id="btnCancel", control_type="Button")

    def fill(self, tag_name, logical_addr=""):
        self.txt_tag.set_text(tag_name)
        if logical_addr:
            self.txt_logical_address.set_text(logical_addr)

    def save(self):
        self.btn_save.click_input()
        time.sleep(0.5)          # tiny pause for UI to settle

    def cancel(self):
        self.btn_cancel.click_input()


  