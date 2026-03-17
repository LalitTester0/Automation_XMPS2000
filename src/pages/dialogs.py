# src/pages/dialogs.py
import time
from pywinauto.timings import always_wait_until
from config.settings import TIMEOUT_MED
from pywinauto import Desktop
from pywinauto.timings import wait_until_passes


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
    def txt_InitialValue(self):
        return self.dlg.child_window(auto_id="textBoxInitialValue", control_type="Edit")
    @property
    def checkbox_Retentive(self):
        return self.dlg.child_window(auto_id="chkIsRetentive", control_type="CheckBox")
    @property
    def checkbox_showLogicalAddress(self):
        return self.dlg.child_window(auto_id="ChkShowLogicalAddress", control_type="CheckBox")
    @property
    def btn_save(self):
        return self.dlg.child_window(auto_id="btnSave", control_type="Button")
    @property
    def btn_cancel(self):
        return self.dlg.child_window(auto_id="btnCancel", control_type="Button")
    @property
    def datatype_dropdown(self):
        return self.dlg.child_window(auto_id="comboBoxIOType",control_type="ComboBox")
    @property
    def error_message(self):
        return self.dlg.child_window(title="Please correct the errors before saving.",control_type="Text")


    def clickRetentivecheckbox(self):
        self.checkbox_Retentive.click_input()   
         
    def clickshowLogicalAddresscheckbox(self):
        self.checkbox_showLogicalAddress.click_input()   
    
    def getErrorMesage(self):
           self.error_message.wait("visible", timeout=5)
           actual_text = self.error_message.window_text()
           return actual_text
    
    def select_datatype(self, value="Byte"):
        combo = self.datatype_dropdown
        combo.wait("visible enabled", timeout=10)
        combo.select(value) 

    def get_tag_cell(self, row=0):
        cell = self.win.child_window(
            title_re=rf"Tag.*Row {row}.*",
            control_type="Edit"
        )
        cell.wait("visible", timeout=10)
        return cell

    def double_click_tag_row(self, row=0):
        cell = self.get_tag_cell(row)
        cell.double_click_input()
        time.sleep(0.5) 

    def fill(self, tag_name, logical_addr=""):
        self.txt_tag.set_text(tag_name)
        if logical_addr:
            self.txt_logical_address.set_text(logical_addr)
          
    def fillInitialValue(self,initial="0"):
        self.txt_InitialValue.set_text(initial)
      
    def fill_update(self, tag_name):
        self.txt_tag.set_text(tag_name)
    
    def save(self):
        self.btn_save.click_input()
        time.sleep(0.5)    
        
    def cancel(self):
        self.btn_cancel.click_input()


  