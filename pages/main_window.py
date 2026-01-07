# pages/main_window.py
from pywinauto import Desktop
from config import TIMEOUT_MED
from pywinauto.keyboard import send_keys
import time
import pywinauto
from pywinauto import Application


class MainWindow:
    
    def __init__(self, app):
        self.app = app
        self.win = None
      
    def wait_for_visible(self, timeout=TIMEOUT_MED):
        """Wait for XMPS 2000 main window by title"""
        win = self.app.window(title_re=".*XMPS.*2000.*", visible_only=False)
        win.wait("visible", timeout=timeout)
        self.win = win
        return self.win
    
    # ------------------------------------------------------------------
    # UI elements (lazy – created only when first accessed)
    # ------------------------------------------------------------------
    @property
    def btn_new_project(self):
        return self.win.child_window(title="StrpBtnNewProject", control_type="Button")

    @property
    def btn_open_project(self):
        return self.win.child_window(title="strpBtnOpenProejct", control_type="Button")

    @property
    def ddl_model(self):
        """Returns the model selection ComboBox"""
        return self.win.child_window(auto_id="ddlModel", control_type="ComboBox")
    @property
    def btn_ok(self):
        """Returns the OK button"""
        return self.win.child_window(auto_id="btnOK", control_type="Button")
    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def click_new_project(self):
        self.btn_new_project.click_input()

    def click_open_project(self):
        self.btn_open_project.click_input()

    def select_model_and_confirm(self, model_name):
        """
        Dynamically selects any PLC model from the dropdown and confirms with OK
        Usage: main_page.select_model_and_confirm("XBLD-14E")
        """
        print(f"Selecting PLC model: {model_name}")

        # Open the dropdown
        dropdown = self.ddl_model
        dropdown.wait("visible", timeout=15)
        dropdown.wait("enabled", timeout=15)
        dropdown.expand()  # Opens the list reliably

        # Wait for the list to appear
        list_box = dropdown.child_window(control_type="List")
        list_box.wait("visible", timeout=10)

        # Dynamically locate the model item
        model_item = list_box.child_window(title=model_name, control_type="ListItem")
        # If exact title has spaces or variation, use regex:
        # model_item = list_box.child_window(title_re=f".*{model_name}.*", control_type="ListItem")

        model_item.wait("visible", timeout=1)
        model_item.click_input()
        print(f"Selected model: '{model_name}'")

        # Click OK
        ok_button = self.btn_ok
        ok_button.wait("visible", timeout=1)
        ok_button.wait("enabled", timeout=1)
        ok_button.click_input()
        print("Model selection confirmed with OK")

    def click_no_button(self):
        try:
            dlg = Desktop(backend="uia").window(title="Save Current Project", control_type="Window")
            dlg.wait("visible", timeout=3)
            dlg.child_window(auto_id="7", control_type="Button").click_input()
        except TimeoutError:
            pass
    
    def press_enter(self):
        send_keys("{ENTER}")
