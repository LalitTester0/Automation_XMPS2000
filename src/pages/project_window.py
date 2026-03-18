# src/pages/project_window.py
import time
from pywinauto import Desktop,Application
from pywinauto.keyboard import send_keys
from config.settings import TIMEOUT_MED
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
    @property
    def compile_button(self):
        return self.win.child_window(title="Compile", control_type="Button")
    @property
    def main_node(self):
        return self.tree.child_window(title="Main", control_type="TreeItem")
    
    @property
    def save_project_button(self):
        return self.win.child_window(title="strpBtnSaveProejct", control_type="Button")

    @property
    def project_saved_message(self):
        return self.win.child_window(title="Project Saved Sucessfully",control_type="Text")
    
    @property
    def status_bar(self):
        return self.win.child_window(auto_id="statusMain", control_type="StatusBar")

    @property
    def io_configuration_node(self):
    
        return self.tree.child_window(title="IO Configuration", control_type="TreeItem")
    
    @property
    def expansion_io_node(self):
        return self.tree.child_window(title="Expansion I/O", control_type="TreeItem")

    @property
    def add_expansion_menu(self):
        return self.win.child_window(title="DropDown", control_type="ToolBar")
  

    @property
    def rename_expansionname(self):
        return self.win.child_window(title="Model Row 0, Not sorted.", control_type="Edit")
    
    @property
    def For_UO(self):
        return self.win.child_window(title="Model Row 4, Not sorted.", control_type="Edit")
    
    @property
    def For_AO(self):
        return self.win.child_window(title="Model Row 2, Not sorted.", control_type="Edit")
    

    @property
    def retentive_address_row0_cell(self):
        return self.win.child_window(title="RetentiveAddress Row 0, Not sorted.", control_type="Edit")
   
   
   
    def click_rename_expansion(self):
        self.rename_expansion.click_input()

    def doubleclick_open_expansion_form(self):
        self.rename_expansionname.double_click_input()

    def doubleclick_for_open_UO(self):
        self.For_UO.double_click_input()
    
    def doubleclick_for_open_AO(self):
        self.For_AO.double_click_input()

    def click_add_device_expansion(self):
        self.add_expansion_menu.click_input()

    def right_click_expansion_io(self):
        self.expansion_io_node.right_click_input()

    def double_click_expansion(self):
        self.expansion_io_node.double_click_input()
    
    def click_save_project_button(self):
        self.save_project_button.click_input()

    def click_ioconfig(self):
        self.io_configuration_node.double_click_input()
    
    
    def click_compile_button(self):
        self.compile_button.click_input()

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
                        break  
        except Exception as e:
            print(f"Error while handling alert: {e}")   


    def open_add_user_tag_dialog(self):
        self._expand_tags()
        self.click_add_user_defined_tags()
       
    def assert_row_count(self, expected: int):
        self.grid.wait("visible", timeout=TIMEOUT_MED)
        actual = self.grid.item_count()
        assert actual == expected, f"Expected {expected} rows, got {actual}"


    def get_row_count(self):
        self.grid.wait("visible", timeout=TIMEOUT_MED)
        actual = self.grid.item_count()
        print("row count",actual)   
        return actual

    def click_system_tags(self):
        self._expand_tags()
        self.system_tags_node.click_input()

    def get_system_tags_gridrow_count(self):
        row_count = self.grid.item_count()
        print(row_count)
        return row_count

    def get_corevalue_by_row_header(self,rowNumber=0):
        element = self.win.child_window(
        title=f"Tag    ˅ Row {rowNumber}, Not sorted.",
        control_type="Edit"
        ).wrapper_object()
        value = element.get_value()
        print(value)

    def get_value_of_initialValueColumn(self,rowNumber=0):
        element = self.win.child_window(
        title=f"InitialValue Row {rowNumber}, Not sorted.",
        control_type="Edit"
        ).wrapper_object()
        value = element.get_value()
        return value
        
    def get_value_of_retentiveStatusColumn(self,rowNumber=0):
        element = self.win.child_window(
        title=f"Retentive Row {rowNumber}",
        control_type="CheckBox"
        ).wrapper_object()
        value = element.get_toggle_state() == 1
        return value
    
    def select_lastRowofUserDefinedTags(self,rowNumber=0):
        element = self.win.child_window(
        title=f"Retentive Row {rowNumber}",
        control_type="CheckBox"
        ).wrapper_object()
        element.double_click_input()

    def delete_UDT(self,rowNumber=0):
        element = self.win.child_window(
        title=f"Retentive Row {rowNumber}",
        control_type="CheckBox"
        ).wrapper_object()
        element.right_click_input()
        time.sleep(5)
        send_keys("{DOWN}{ENTER}")  

    
    def get_value_of_showLogicalAddressStatusColumn(self,rowNumber=0):
        element = self.win.child_window(
        title=f"ShowLogicalAddress Row {rowNumber}",
        control_type="CheckBox"
        ).wrapper_object()
        value = element.get_toggle_state() == 1
        return value
        
    def get_value_of_retentiveAddressColumn(self,rowNumber=0):
        element = self.win.child_window(
        title=f"RetentiveAddress Row {rowNumber}, Not sorted.",
        control_type="Edit"
        ).wrapper_object()
        value = element.get_value()
        return value
    
        
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

    def get_multivalue_expansion(self, count):
        val = []
        for i in range(count):
            # dynamic_title = f"Tag    ˅ Row {i}, Not sorted."
            dynamic_title = f"Tag Row {i}, Not sorted."
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
            
            # This is the important part
            val = []
            for item in items:
                text = item.window_text().strip()
                if text:                    # skip completely empty items
                    val.append(text)
                # else: continue            # we ignore <empty> entries
                    
            # Optional: show what we got
            print("Collected items:", val)
            
            return val
            
        except Exception as e:
            print(f"Could not read dropdown: {e}")
            print("Make sure the dropdown is expanded!")
            return []
        
    def print_dropdown_items_that_match_expansion(self, expansion_count=5):
        """
        1. Collects values from expansion Edit fields (Tag Row 0..N)
        2. Collects all items from the dropdown
        3. Finds dropdown items that appear in the expansion list
        4. Prints only the matching dropdown items + summary
        """
        # ── Step 1: Get expansion values ───────────────────────────────
        expansion_values = []
        for i in range(expansion_count):
            dynamic_title = f"Tag Row {i}, Not sorted."
            print(f"Reading expansion → {dynamic_title}")
            
            try:
                element = self.win.child_window(
                    title=dynamic_title,
                    control_type="Edit"
                ).wrapper_object()
                
                value = element.get_value() or ""   # protect against None
                value = value.strip()
                if value:
                    expansion_values.append(value)
            except Exception as e:
                print(f"  → Could not read {dynamic_title}: {e}")
        
        if not expansion_values:
            print("\nNo non-empty expansion values found.")
            return []
        
        print("\nExpansion values collected:", expansion_values)
        print(f"({len(expansion_values)} non-empty items)\n")
        
        # ── Step 2: Get dropdown items ─────────────────────────────────
        try:
            dropdown_list = self.win.child_window(auto_id="1000", control_type="List")
            dropdown_list.wait("visible", timeout=20)
            
            list_wrapper = dropdown_list.wrapper_object()
            items = list_wrapper.items()
            
            dropdown_values = [
                item.window_text().strip()
                for item in items
                if item.window_text().strip()
            ]
            
            print("All dropdown items:", dropdown_values)
            print(f"({len(dropdown_values)} items total)\n")
            
        except Exception as e:
            print(f"Could not read dropdown: {e}")
            print("Make sure the dropdown is expanded!")
            return []
        
        # ── Step 3: Find matches (dropdown items that are in expansion) ──
        matching_in_dropdown = [
            item for item in dropdown_values
            if item in expansion_values
        ]
        
        # ── Step 4: Print result ────────────────────────────────────────
        print("═" * 60)
        print("DROPDOWN ITEMS THAT MATCH EXPANSION VALUES")
        print("═" * 60)
        
        if not matching_in_dropdown:
            print("→ NO MATCHES FOUND")
            print("  (none of the expansion values appear in the dropdown)")
        else:
            for idx, value in enumerate(matching_in_dropdown, 1):
                print(f"  {idx:2d}. {value}")
            
            print(f"\nFound {len(matching_in_dropdown)} matching item(s)")
        
        print("═" * 60)
        
        # Also return the list in case you want to use it later (e.g. assert len > 0)
        return matching_in_dropdown
    
    def get_row_datatype(self, row=0):
        cell = self.win.child_window(
            title=f"DataType    ˅ Row {row}, Not sorted.",  # exact string from inspect
            control_type="Edit"
        )
        cell.wait("visible", timeout=10)
        print(cell.get_value())
        return cell.get_value()

    def assert_row_datatype(self, expected: str, row=0):
        actual = self.get_row_datatype(row)
        assert actual == expected, (
            f"DataType mismatch at row {row}: expected '{expected}', got '{actual}'"
        )


    def get_row_tag_name(self, row=0):
        """Reads the Tag name from the grid."""
        cell = self.get_tag_cell(row)
        return cell.get_value()
    def get_tag_cell(self, row=0):
            """
            Returns the Tag cell element for the given row.
            Uses the pattern: 'Tag    ˅ Row {row}, Not sorted.'
            """
            cell = self.win.child_window(
                title_re=rf"Tag.*Row {row}.*",
                control_type="Edit"
            )
            cell.wait("visible", timeout=10)
            return cell

    def double_click_tag_row(self, row=0):
            """
            Double-clicks on the Tag cell to open the edit dialog.
            """
            cell = self.get_tag_cell(row)
            cell.double_click_input()
            print(f"[OK] Double-clicked row {row} to open edit dialog")
            time.sleep(0.5)  # brief pause for dialog to appear
    def assert_row_tag_name(self, expected: str, row=0):
        actual = self.get_row_tag_name(row)
        assert actual == expected, (
            f"Tag name mismatch at row {row}: expected '{expected}', got '{actual}'"
        )

    def edit_tag_inline(self, row=0, new_tag_name=""):
        """
        Double-clicks the tag cell and edits it inline (no dialog).
        """
        cell = self.get_tag_cell(row)
        cell.double_click_input()
        time.sleep(0.3)  # brief pause for cell to enter edit mode
        
        # The cell should now be editable
        cell.set_focus()
        cell.set_edit_text("")  # clear existing text
        cell.type_keys(new_tag_name, with_spaces=True)
        cell.type_keys("{ENTER}")  # commit the edit
        
        print(f"[OK] Edited tag inline to: {new_tag_name}")
        time.sleep(0.5)  # let grid update

    def fill(self, tag_name, logical_addr=""):
        """
        Fill the tag form. Aggressively clears existing text.
        """
        # Method 1: Use set_edit_text (direct Win32 API call)
        self.txt_tag.set_focus()
        self.txt_tag.set_edit_text(tag_name)
        
        if logical_addr:
            self.txt_logical_address.set_focus()
            self.txt_logical_address.set_edit_text(logical_addr)
        
        time.sleep(0.3)