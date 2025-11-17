# pages/project_window.py
import time
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
from config import TIMEOUT_MED


class ProjectWindow:
    """The window that contains the tree view and the data-grid."""

    def __init__(self, app):
        self.app = app
        # find the first top-level window that owns a Tree control
        windows = Desktop(backend="uia").windows(process=app.process)
        self.win = next(
            (Desktop(backend="uia").window(handle=w.handle)
             for w in windows
             if Desktop(backend="uia").window(handle=w.handle)
                .child_window(control_type="Tree").exists(timeout=1)),
            None
        )
        if not self.win:
            raise RuntimeError("Project window not found")
        #self.win.wait("visible", timeout=TIMEOUT_MED)

    def _find_window(self):
        """Find the top-level window that contains a Tree control"""
        try:
            windows = Desktop(backend="uia").windows(process=self.app.process)
            for w in windows:
                win = Desktop(backend="uia").window(handle=w.handle)
                # Check if this window has a Tree control
                if win.child_window(control_type="Tree").exists(timeout=1):
                    return win
        except Exception as e:
            print(f"Error finding window: {e}")
        return None

    
    def wait_for_visible(self, timeout=TIMEOUT_MED):
        win = self._find_window()
        if not win:
                raise RuntimeError("Project window with Tree not found")
        win.wait("visible", timeout=timeout)
        self.win = win
        return self.win

    @property
    def tree(self):
        return self.win.child_window(control_type="Tree")

    @property
    def grid(self):
        return self.win.child_window(auto_id="grdMain", control_type="Table")

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------
    def _expand_tags(self):
        tags = self.tree.child_window(title="Tags", control_type="TreeItem")
        tags.double_click_input()
        time.sleep(0.3)

    def open_add_user_tag_dialog(self):
        self._expand_tags()
        udt = self.tree.child_window(title="User Defined Tags", control_type="TreeItem")
        udt.click_input()
        udt.right_click_input()
        time.sleep(0.5)
        send_keys("{DOWN}{ENTER}")      # choose “Add” from context menu
        time.sleep(1)

    # ------------------------------------------------------------------
    # Grid verification
    # ------------------------------------------------------------------
    def assert_row_count(self, expected: int):
        self.grid.wait("visible", timeout=TIMEOUT_MED)
        actual = self.grid.item_count()
        assert actual == expected, f"Expected {expected} rows, got {actual}"