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
        return self.win.child_window(auto_id="ddlModel", control_type="ComboBox")

    @property
    def list_item_xbld(self):
        return self.win.child_window(title="XBLD-14E", control_type="ListItem")

    @property
    def btn_ok(self):
        return self.win.child_window(auto_id="btnOK", control_type="Button")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def click_new_project(self):
        self.btn_new_project.click_input()

    def click_open_project(self):
        self.btn_open_project.click_input()

    def select_model_and_confirm(self):
        self.ddl_model.click_input()
        self.list_item_xbld.click_input()
        self.btn_ok.click_input()

    def click_no_button(self):
        try:
            dlg = Desktop(backend="uia").window(title="Save Current Project", control_type="Window")
            dlg.wait("visible", timeout=3)
            dlg.child_window(auto_id="7", control_type="Button").click_input()
        except TimeoutError:
            pass
    
    def press_enter(self):
        send_keys("{ENTER}")


    ## pages/main_window.py — FINAL WORKING METHOD
    # pages/main_window.py — FINAL METHOD

    # pages/main_wi# pages/main_window.py — FINAL WORKING METHOD

    def open_project_file_dialog(self, file_path):
        """
        Open any .xmprj file — WORKS 100% with your XMPS 2000
        """
        print(f"Opening project: {file_path}")

        # Click Open button
        self.btn_open_project.click_input()

        # Wait for the dialog to appear
        time.sleep(2)

        # THIS IS THE ONLY LINE THAT WORKS IN REAL LIFE
        dlg = pywinauto.Application(backend="uia").connect(title_re="Browse.*", timeout=15).top_window()

        print(f"Dialog found: '{dlg.window_text()}'")

        # Enter the file path using the correct AutomationId
        file_edit = dlg.child_window(auto_id="1148", control_type="Edit")
        file_edit.wait("ready", timeout=10)
        file_edit.set_text(file_path)

        # Click Open button
        open_btn = dlg.child_window(auto_id="1", control_type="Button")
        open_btn.wait("enabled", timeout=10)
        open_btn.click_input()

        print("Project opening...")
        time.sleep(8)