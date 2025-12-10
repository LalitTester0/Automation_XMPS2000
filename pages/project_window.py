# pages/project_window.py
import time
from pywinauto import Desktop,Application
from pywinauto.keyboard import send_keys
from config import TIMEOUT_MED
from pywinauto.timings import always_wait_until, TimeoutError


class ProjectWindow:
    @property
    def tree(self):
        return self.win.child_window(control_type="Tree")
    @property
    def grid(self):
        return self.win.child_window(auto_id="grdMain", control_type="Table")
    @property
    def user_defined_tags_node(self):
        return self.tree.child_window(title="User Defined Tags", control_type="TreeItem")
    @property
    def tags_node(self):
        return self.tree.child_window(title="Tags", control_type="TreeItem")
    @property
    def system_tags_node(self):
        return self.tree.child_window(title="System Tags", control_type="TreeItem")
    @property
    def system_config_node(self):
        return self.tree.child_window(title="System Configuration", control_type="TreeItem")
    @property
    def modbus_tcp_client_node(self):
        return self.tree.child_window(title="MODBUS TCP Client", control_type="TreeItem")
    @property
    def ethernate_node(self):
        return self.tree.child_window(title="Ethernet", control_type="TreeItem")
    @property
    def variable_dropdown(self):
        return self.win.child_window(auto_id="TagEnable", control_type="ComboBox")



    def click_system_config(self):
        self.system_config_node.double_click_input()

    def click_ethernet_node(self):
        self.click_system_config()        
        self.ethernate_node.double_click_input()

    def click_modbus_tcp_client(self):
        self.click_ethernet_node()
        self.modbus_tcp_client_node.click_input()
        self.modbus_tcp_client_node.right_click_input()
        time.sleep(0.5)
        send_keys("{DOWN}{ENTER}")  
        time.sleep(2)
        self.variable_dropdown.click_input()
        time.sleep(2)
    
    def __init__(self, app):
        self.app = app
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

    def _expand_tags(self):
        self.tags_node.double_click_input()
        time.sleep(0.3)

    def click_add_user_defined_tags(self):
        self.user_defined_tags_node.click_input()
        self.user_defined_tags_node.right_click_input()
        time.sleep(0.5)
        send_keys("{DOWN}{ENTER}")  
        time.sleep(1)

    def click_export_user_defined_tags(self):
        self._expand_tags()
        self.user_defined_tags_node.click_input()
        self.user_defined_tags_node.right_click_input()
        time.sleep(0.5)
        send_keys("{DOWN}")  
        send_keys("{DOWN}{ENTER}")
        time.sleep(1)
        send_keys("{DOWN}{ENTER}")
        time.sleep(1)
        try:
            alert_found = False

            # IMPORTANT: self.app instead of undefined 'app'
            for win in Desktop(backend="uia").windows(process=self.app.process):
                win_spec = Desktop(backend="uia").window(handle=win.handle)

                for txt in win_spec.descendants(control_type="Text"):
                    text_value = txt.window_text()

                    print("Found Text:", text_value)
                    if r"Tags are save in C:\Users\Admin\AppData\Roaming\MessungSystems\XMPS2000\XM Projects\XBLDProject02\XBLDProject300.xmprj_UDT.csv File" in text_value:
                        alert_found = True
                        print("Alert found:", text_value)

                        ok_button = win_spec.child_window(title="OK", control_type="Button")
                        if ok_button.exists(timeout=2):
                            ok_button.click_input()
                            print("OK button clicked.")
                        break  # Stop scanning text inside this window
        except Exception as e:
            print(f"Error while handling alert: {e}")   


    def open_add_user_tag_dialog(self):
        self._expand_tags()
        self.click_user_defined_tags()
       
    def assert_row_count(self, expected: int):
        self.grid.wait("visible", timeout=TIMEOUT_MED)
        actual = self.grid.item_count()
        assert actual == expected, f"Expected {expected} rows, got {actual}"

    def click_system_tags(self):
        self._expand_tags()
        self.system_tags_node.click_input()

    def get_system_tags_gridrow_count(self):
        row_count = self.grid.item_count()
        print(row_count)
        return row_count

    def get_corevalue_by_row_header(self,count):
        element = self.win.child_window(
        title="Tag    ˅ Row 0, Not sorted.",
        control_type="Edit"
        ).wrapper_object()
        value = element.get_value()
        print(value)

    def get_multivalue_by_row_header(self, count):
        val = []
        for i in range(count):
            dynamic_title = f"Tag    ˅ Row {i}, Not sorted."
            print("TITLE",dynamic_title)
            element = self.win.child_window(
                    title=dynamic_title,
                    control_type="Edit"
                ).wrapper_object()

            value = element.get_value()
            val.append(value)
        print(val)

    def print_all_items_in_dropdown(self):
        try:
            dropdown_list = self.win.child_window(auto_id="1000", control_type="List")
            dropdown_list.wait("visible", timeout=20)
            list_wrapper = dropdown_list.wrapper_object()
            items = list_wrapper.items()
            print(f"Found {len(items)} items in dropdown:\n")
            for i, item in enumerate(items, 1):
                text = item.window_text().strip()
                if text:
                    print(f"  {i:2d}. {text}")
                else:
                    print(f"  {i:2d}. <empty>")
        except Exception as e:
            print(f"Could not read dropdown list: {e}")
            print("Make sure the dropdown is expanded/open!")