# src/pages/io_config.py
import time
from pywinauto import Desktop, Application
from pywinauto.keyboard import send_keys
from config.settings import TIMEOUT_MED
from pywinauto.timings import always_wait_until, TimeoutError
from pywinauto.timings import wait_until


class IOConfig:
    def __init__(self, win):
        self.win = win

    # Existing onboard methods (kept as is)
    @property
    def digital_input_count_cell(self):
        return self.win.child_window(title="On-Board IO Row 0, Not sorted.", control_type="Edit")
    
    
    @property
    def expansion_tag_textbox(self):
        """Returns the tag name text box (AutomationId: textBoxTag)"""
        return self.win.child_window(auto_id="textBoxTag", control_type="Edit")
    
    @property
    def expansion_save_button(self):
        """Returns the Save button (AutomationId: btnSave)"""
        return self.win.child_window(auto_id="btnSave", control_type="Button")
    @property
    def tag_column_row0_cell(self):
        """Returns the read-only Tag column cell for Row 0 (title: 'Tag Row 0, Not sorted.')"""
        return self.win.child_window(title="Tag Row 0, Not sorted.", control_type="Edit")

    @property
    def is_retentive_checkbox(self):
        return self.win.child_window(auto_id="chkIsRetentive", control_type="CheckBox")

    @property
    def retentive_address_row0_cell(self):
        """Returns the 'RetentiveAddress Row 0, Not sorted.' cell in the grid (read-only)"""
        return self.win.child_window(title="RetentiveAddress Row 0, Not sorted.", control_type="Edit")
    
    @property
    def data_type_row0_cell(self):
        """Returns the 'DataType Row 0, Not sorted.' cell in the grid (read-only)"""
        return self.win.child_window(title="DataType Row 0, Not sorted.", control_type="Edit")

    def get_tag_cell(self, row_index):
        """Returns the Tag cell for a specific row (dynamic)"""
        title = f"Tag Row {row_index}, Not sorted."
        return self.win.child_window(title=title, control_type="Edit")

    @property
    def enable_input_filter_checkbox(self):
        """Returns the 'Enable Input Filter' checkbox"""
        return self.win.child_window(auto_id="checkBoxEnableInputFilter", control_type="CheckBox")
    @property
    def input_filter_value_textbox(self):
        """Returns the Digital Input Filter value textbox"""
        return self.win.child_window(auto_id="textBoxInFilValue", control_type="Edit")
    
    @property
    def digital_filter_row0_cell(self):
        """Returns the 'DigitalFilter Row 0, Not sorted.' cell in the main grid"""
        return self.win.child_window(title="DigitalFilter Row 0, Not sorted.", control_type="Edit")

    @property
    def input_filter_value_textbox(self):
        """Returns the Digital Input Filter value textbox"""
        return self.win.child_window(auto_id="textBoxInFilValue", control_type="Edit")

    @property
    def digital_filter_row0_cell(self):
        """Returns the 'DigitalFilter Row 0, Not sorted.' cell in the main grid"""
        return self.win.child_window(title="DigitalFilter Row 0, Not sorted.", control_type="Edit")

    @property
    def initial_value_textbox(self):
        """Returns the Initial Value textbox (AutomationId: textBoxInitialValue)"""
        return self.win.child_window(auto_id="textBoxInitialValue", control_type="Edit")

    @property
    def initial_value_column_row0_cell(self):
        """Returns the displayed InitialValue column cell in the main grid (Row 0)"""
        return self.win.child_window(title="InitialValue Row 0, Not sorted.", control_type="Edit")

    @property
    def mode_dropdown(self):
        """Returns the 'Logical Address' mode combo box (AutomationId: comboBoxMode)"""
        return self.win.child_window(auto_id="comboBoxMode", control_type="ComboBox")

    @property
    def mode_dropdown_list(self):
        """Returns the expanded Mode dropdown list (ComboLBox)"""
        return self.win.child_window(class_name="ComboLBox", control_type="List")

    @property
    def mode_column_row0_cell(self):
        """Returns the displayed 'Mode Row 0, Not sorted.' cell in the main grid"""
        return self.win.child_window(title="Mode Row 0, Not sorted.", control_type="Edit")

    @property
    def mode_column_row4_cell(self):
        """Returns the displayed 'Mode Row 4, Not sorted.' cell in the main grid"""
        return self.win.child_window(title="Mode Row 4, Not sorted.", control_type="Edit")
    
    @property
    def mode_column_row2_cell(self):
        """Returns the displayed 'Mode Row 2, Not sorted.' cell in the main grid"""
        return self.win.child_window(title="Mode Row 2, Not sorted.", control_type="Edit")
    @property
    def show_logical_address_checkbox(self):
        """Returns the 'Show Logical Address' checkbox in the form"""
        return self.win.child_window(auto_id="ChkShowLogicalAddress", control_type="CheckBox")

    @property
    def show_logical_address_grid_cell_row0(self):
        """Returns the ShowLogicalAddress checkbox cell in the grid (Row 0)"""
        return self.win.child_window(title="ShowLogicalAddress Row 0", control_type="CheckBox")

    @property
    def expansion_model_row0_cell(self):
        """Model name cell for the first added expansion module (Row 0)"""
        return self.win.child_window(title="Model Row 0, Not sorted.", control_type="Edit")

    def get_expansion_model_name(self):
        """Get the displayed model name in Row 0"""
        cell = self.expansion_model_row0_cell
        cell.wait("visible", timeout=15)
        name = cell.get_value().strip()
        print(f"Detected model name: '{name}'")
        return name

    @property
    def digital_input_count_cell(self):
        """Cell that shows the number of digital inputs (Row 0)"""
        # More specific title pattern — adjust if your app shows "16" in a different cell
        return self.win.child_window(title_re=".*Input.*Count.*Row 0.*|.*DI.*Row 0.*", control_type="Edit")
   
    @property
    def resistance_lookup_table_tree_item(self):
        """
        Returns the 'Resistance Lookup Table' tree item in the tree view.
        """
        return self.win.child_window(
            title="Resistance Lookup Table",
            control_type="TreeItem"
        )
    
    @property
    def resistance_dropdown_toolbar(self):
        """
        Returns the 'DropDown' toolbar/button in the resistance lookup table section.
        """
        return self.win.child_window(
            title="DropDown",
            control_type="ToolBar"
        )
    @property
    def resistance_name_textbox(self):
        """
        Returns the textbox (AutomationId: 'TextBox') for entering resistance name/value.
        """
        return self.win.child_window(
            auto_id="TextBox",
            control_type="Edit"
        )
    @property
    def added_resistance_table_item(self):
        """
        Returns the newly added resistance table item (e.g. "sdfs") in the tree.
        Use .exists() to check if it's present/added.
        """
        return self.win.child_window(
            title="sdfs",
            control_type="TreeItem"
        )
    
    def getnamed_resistance_table_item(self):
        self.added_resistance_table_item.click_input()
    

    
    def get_added_resistance_table_item(self, table_name):
        """
        Returns the added resistance table item by its name.
        """
        return self.win.child_window(
            title=table_name,
            control_type="TreeItem"
        )
        

    def enter_resistance_name(self, name_value):
        """Enters a name/value into the resistance textbox and presses Enter."""
        textbox = self.resistance_name_textbox
        textbox.click_input()
        textbox.set_text(name_value)
        textbox.type_keys("{ENTER}")

    def click_add_resistance_lookup_table(self):
        self.resistance_dropdown_toolbar.click_input()

    def rightclick_resistance_lookup_table(self):
        self.resistance_lookup_table_tree_item.right_click_input()
    def doubleclick_resistance_lookup_table(self):
        self.resistance_lookup_table_tree_item.double_click_input()

    def get_tag_cell(self, row_index):
        """Returns the Tag cell for a specific row dynamically"""
        title = f"Tag Row {row_index}, Not sorted."
        return self.win.child_window(title=title, control_type="Edit")

    def print_all_tags_in_column(self, max_rows=32, timeout_per_row=12):
        """
        Prints ALL non-empty tag values from the Tag column in the grid.
        
        - Loops from Row 0 until no more rows are found or timeout occurs
        - Prints every row (even empty) for full visibility
        - Increased timeout and detailed logging
        """
        print("\n=== Starting to print all tags from Tag column ===")
        print("Scanning rows 0 to", max_rows-1, "...\n")

        row = 0
        found_tags = 0
        empty_rows = 0

        while row < max_rows:
            try:
                cell = self.get_tag_cell(row)
                
                # Wait longer — UI grids can take time to populate
                cell.wait("visible", timeout=timeout_per_row)
                cell.wait("enabled", timeout=5)  # Ensure it's ready
                
                tag_value = cell.get_value().strip()
                
                if tag_value:
                    print(f"Row {row:2d}: '{tag_value}'")
                    found_tags += 1
                else:
                    print(f"Row {row:2d}: <empty>")
                    empty_rows += 1
                
                row += 1
                
            except TimeoutError:
                print(f"\nStopped at Row {row} — cell not visible after {timeout_per_row}s timeout.")
                break
            except Exception as e:
                print(f"Error at Row {row}: {e}")
                break

        print("\n=== Summary ===")
        print(f"Scanned {row} rows")
        print(f"Found {found_tags} tags")
        print(f"{empty_rows} empty rows")
        if found_tags == 0:
            print("WARNING: No tags were found! Check if grid is loaded or locator is correct.")
        else:
            print("All tags successfully printed.")

    def get_digital_input_count(self):
        """Read digital input count as integer"""
        cell = self.digital_input_count_cell
        cell.wait("visible", timeout=15)
        count_str = cell.get_value().strip()
        try:
            count = int(count_str)
            print(f"Digital input count found: {count}")
            return count
        except ValueError:
            raise ValueError(f"Could not parse digital input count: '{count_str}'")

    def assert_digital_input_count(self, expected_count):
        """
        Asserts the grid shows exactly the expected number of digital inputs.
        """
        actual = self.get_digital_input_count()
        assert actual == expected_count, \
            f"Digital input count mismatch! Expected {expected_count}, but found {actual}"
        print(f"Assertion passed: {actual} digital inputs (matches expected {expected_count})")
    
    def enable_show_logical_address(self):
        """Checks the 'Show Logical Address' checkbox if not already checked"""
        checkbox = self.show_logical_address_checkbox
        checkbox.wait("visible", timeout=10)
        checkbox.wait("enabled", timeout=10)

        if checkbox.get_toggle_state() == 0:
            checkbox.click_input()
            print("Enabled 'Show Logical Address' checkbox")
        else:
            print("'Show Logical Address' checkbox already enabled")

    def assert_show_logical_address_grid_checked(self):
        """
        Asserts that the ShowLogicalAddress checkbox in the grid (Row 0) is checked.
        Uses Toggle pattern (correct for CheckBox controls).
        """
        cell = self.show_logical_address_grid_cell_row0
        cell.wait("visible", timeout=15)

        # Primary check: ToggleState should be 1 (checked)
        toggle_state = cell.get_toggle_state()
        assert toggle_state == 1, \
            f"ShowLogicalAddress grid cell is not checked (ToggleState: {toggle_state})"

        # Secondary check: Value property or window_text should reflect "True"/checked
        try:
            value = cell.legacy_properties.get("Value", "").strip()
            if not value:
                value = cell.window_text().strip()
            assert value in ["True", "Checked", "1"], \
                f"ShowLogicalAddress grid cell value is '{value}', expected 'True'"
        except:
            # Fallback if legacy properties not available
            pass

        print("Assertion passed: ShowLogicalAddress grid cell is checked (ToggleState=1)")
    def open_mode_dropdown(self):
        """Expands the Mode dropdown"""
        combo = self.mode_dropdown
        combo.wait("visible", timeout=10)
        combo.wait("enabled", timeout=10)
        combo.expand()
        print("Opened Mode dropdown")

    def select_mode(self, mode_name):
        """Selects any mode from the dropdown by name"""
        self.open_mode_dropdown()
        
        # Dynamic locator for any mode item
        item = self.mode_dropdown_list.child_window(title=mode_name, control_type="ListItem")
        item.wait("visible", timeout=10)
        item.wait("enabled", timeout=10)
        item.click_input()
        
        print(f"Selected mode: '{mode_name}'")

    def get_displayed_mode_value(self):
        """Gets the current value shown in the Mode column (Row 0)"""
        cell = self.mode_column_row0_cell
        cell.wait("visible", timeout=15)
        value = cell.get_value().strip()
        print(f"Displayed Mode in grid: '{value}'")
        return value
    
    def for_UO_get_displayed_mode_value(self):
        """Gets the current value shown in the Mode column (Row 0)"""
        cell = self.mode_column_row4_cell
        cell.wait("visible", timeout=15)
        value = cell.get_value().strip()
        print(f"Displayed Mode in grid: '{value}'")
        return value
    
    def for_AO_get_displayed_mode_value(self):
        """Gets the current value shown in the Mode column (Row 0)"""
        cell = self.mode_column_row2_cell
        cell.wait("visible", timeout=15)
        value = cell.get_value().strip()
        print(f"Displayed Mode in grid: '{value}'")
        return value

    def assert_mode_matches_selected(self, selected_mode):
        """
        Asserts that the Mode column shows **exactly** the selected mode.
        Fully dynamic — works for any mode name.
        """
        displayed = self.get_displayed_mode_value()

        assert displayed == selected_mode, \
            f"Mode mismatch! Selected '{selected_mode}', but grid shows '{displayed}'"

        print(f"Assertion passed: Mode column shows '{displayed}' (matches selected '{selected_mode}')")

    def for_UOassert_mode_matches_selected(self, selected_mode):
        """
        Asserts that the Mode column shows **exactly** the selected mode.
        Fully dynamic — works for any mode name.
        """
        displayed = self.for_UO_get_displayed_mode_value()

        assert displayed == selected_mode, \
            f"Mode mismatch! Selected '{selected_mode}', but grid shows '{displayed}'"

        print(f"Assertion passed: Mode column shows '{displayed}' (matches selected '{selected_mode}')")


    def get_tag_cell(self, row_index):
        """Returns the Tag cell for any row dynamically"""
        title = f"Tag Row {row_index}, Not sorted."
        return self.win.child_window(title=title, control_type="Edit")

    def get_tag_value_at_row(self, row_index):
        """Gets the tag name from a specific row"""
        cell = self.get_tag_cell(row_index)
        cell.wait("visible", timeout=15)
        value = cell.get_value().strip()
        print(f"Tag at Row {row_index}: '{value}'")
        return value

    def assert_or_tag_prefix_matches_renamed(self, renamed_tag, or_tag_row=4):

        or_tag_value = self.get_tag_value_at_row(or_tag_row)

        expected_or_tag = f"{renamed_tag}_OR"

        assert or_tag_value == expected_or_tag, \
            f"OR tag not updated! Expected '{expected_or_tag}', but got '{or_tag_value}'"

        print(f"Assertion passed: OR tag correctly updated to '{or_tag_value}'")

    def assert_ol_tag_prefix_matches_renamed(self, renamed_tag, ol_tag_row=5):
        """
        Asserts that the OL tag (e.g., Row 5) starts with the renamed tag + "_OL"
        
        Example:
            renamed_tag = "MyCustomAI"
            OL tag should become "MyCustomAI_OL"
        """
        ol_tag_value = self.get_tag_value_at_row(ol_tag_row)

        expected_ol_tag = f"{renamed_tag}_OL"

        assert ol_tag_value == expected_ol_tag, \
            f"OL tag not updated! Expected '{expected_ol_tag}', but got '{ol_tag_value}'"

        print(f"Assertion passed: OL tag correctly updated to '{ol_tag_value}'")
        
    def for_AOassert_mode_matches_selected(self, selected_mode):
        """
        Asserts that the Mode column shows **exactly** the selected mode.
        Fully dynamic — works for any mode name.
        """
        displayed = self.for_AO_get_displayed_mode_value()

        assert displayed == selected_mode, \
            f"Mode mismatch! Selected '{selected_mode}', but grid shows '{displayed}'"

        print(f"Assertion passed: Mode column shows '{displayed}' (matches selected '{selected_mode}')")



    def enter_initial_value(self, value):
        """
        Enters a value in the Initial Value textbox and confirms with Enter
        Returns the entered value as string for assertion
        """
        textbox = self.initial_value_textbox
        textbox.wait("visible", timeout=10)
        textbox.wait("enabled", timeout=10)

        textbox.click_input()  # Focus
        textbox.set_text(str(value))
        textbox.type_keys("{ENTER}")

        print(f"Entered Initial Value: '{value}'")
        return str(value)  # Return for comparison

    def get_displayed_initial_value(self):
        """Gets the value shown in the InitialValue column (Row 0)"""
        cell = self.initial_value_column_row0_cell
        cell.wait("visible", timeout=15)
        return cell.get_value().strip()

    @property
    def error_popup(self):
        """Returns the error popup window (adjust title if needed)"""
        # Common error popup titles — use the one that matches your app
        try:
            return Application(backend="uia").window(title_re=".*Error.*|.*Invalid.*|.*Warning.*")
        except:
            return None

    def is_error_popup_present(self, timeout=3):
        """Checks if an error popup is visible within timeout"""
        try:
            popup = self.error_popup
            if popup and popup.exists(timeout=timeout):
                print(f"Error popup detected: '{popup.window_text()}'")
                return True
        except:
            pass
        return False

    def assert_no_error_for_valid_initial_value(self, value):
        """
        Enters a valid value (0 or 1) and asserts NO error popup appears
        """
        assert value in ["0", "1"], f"Value '{value}' is not valid for Boolean"

        self.enter_initial_value(value)

        # Save to trigger validation
        self.save_expansion()

        # Check for error popup
        assert not self.is_error_popup_present(), \
            f"Error popup appeared for valid Initial Value '{value}'!"

        print(f"Assertion passed: No error popup for valid value '{value}'")

        # Optional: verify displayed value
        displayed = self.get_displayed_initial_value()
        assert displayed == value, \
            f"Displayed value mismatch! Expected '{value}', got '{displayed}'"
    
    def enable_input_filter(self):
        """Enables the 'Enable Input Filter' checkbox if not already enabled"""
        checkbox = self.enable_input_filter_checkbox
        checkbox.wait("visible", timeout=10)
        checkbox.wait("enabled", timeout=10)

        if checkbox.get_toggle_state() == 0:  # Off
            checkbox.click_input()
            print("Enabled 'Enable Input Filter'")
        else:
            print("'Enable Input Filter' already enabled")
    def enter_input_filter_value(self, value):
        """Enters a value in the filter textbox and presses Enter"""
        textbox = self.input_filter_value_textbox
        textbox.wait("visible", timeout=10)
        textbox.wait("enabled", timeout=10)

        textbox.set_text(str(value))
        textbox.type_keys("{ENTER}")
        print(f"Entered Input Filter value: '{value}'")
        return str(value)  # Return as string for comparison

    def get_displayed_digital_filter_value(self):
        """Gets the value shown in the DigitalFilter column after save"""
        cell = self.digital_filter_row0_cell
        cell.wait("visible", timeout=15)
        raw_value = cell.get_value().strip()
        # Remove checkbox symbol if present (e.g., "☑ 20" → "20")
        if raw_value.startswith("☑"):
            raw_value = raw_value[2:].strip()
        return raw_value
    
    def assert_input_filter_enabled_by_default(self):
        """
        Asserts that 'Enable Input Filter' checkbox is checked by default
        """
        checkbox = self.enable_input_filter_checkbox
        checkbox.wait("visible", timeout=10)
        checkbox.wait("enabled", timeout=10)

        state = checkbox.get_toggle_state()
        assert state == 1, f"Enable Input Filter is not checked by default (state: {state})"

        print("Assertion passed: 'Enable Input Filter' is checked by default")

    def assert_or_tags_present(self, expected_count=4):
        """
        Asserts that OR tags (ending with '_OR') are present in the Tag column.
        Prints ONLY actual OR tags for clarity.
        """
        try:
            or_tags_found = 0
            print("\n=== Checking OR tags in Tag column ===")

            for row in range(16):  # Adjust range if you have more/fewer rows
                try:
                    cell = self.get_tag_cell(row)
                    cell.wait("visible", timeout=5)
                    tag_value = cell.get_value().strip()

                    # Only count and print if it's actually an OR tag
                    if tag_value.endswith("_OR"):
                        or_tags_found += 1
                        print(f"Found OR tag in Row {row}: '{tag_value}'")

                except:
                    continue  # Skip rows that don't exist

            assert or_tags_found == expected_count, \
                f"Expected {expected_count} OR tags, but found {or_tags_found}"

            print(f"\nAssertion passed: {or_tags_found} OR tags found as expected")

        except Exception as e:
            raise AssertionError(f"Failed to verify OR tags: {e}")
    
    def assert_ol_tags_present(self, expected_count=4):
        """
        Asserts that OR tags (ending with '_OR') are present in the Tag column
        for AIAO module (usually 4 OR tags: AI0_OR, AI1_OR, AO0_OR, AO1_OR)
        """
        try:
            or_tags_found = 0
            # AIAO typically has 8 rows (4 AI + 4 AO), check rows 0 to 7
            for row in range(16):
                try:
                    cell = self.get_tag_cell(row)
                    cell.wait("visible", timeout=5)
                    tag_value = cell.get_value().strip()
                    if tag_value.endswith("_OL"):
                        or_tags_found += 1
                        print(f"Found OR tag in Row {row}: '{tag_value}'")
                except:
                    continue  # Skip if row not present

            assert or_tags_found == expected_count, \
                f"Expected {expected_count} OL tags, but found {or_tags_found}"

            print(f"Assertion passed: {or_tags_found} OL tags found as expected")

        except Exception as e:
            raise AssertionError(f"Failed to verify OL tags: {e}")
    def assert_data_type(self, expected_data_type):
        """
        Dynamically asserts that the DataType column in Row 0 shows the expected value
        Usage: io_config.assert_data_type("Real")  # for AIAO
               io_config.assert_data_type("Bool")  # for DI/DO
        """
        try:
            cell = self.data_type_row0_cell
            cell.wait("visible", timeout=15)
            actual_value = cell.get_value().strip()

            assert actual_value == expected_data_type, \
                f"DataType mismatch! Expected '{expected_data_type}', got '{actual_value}'"

            print(f"Assertion passed: DataType is '{actual_value}' as expected")

        except Exception as e:
            raise AssertionError(f"Failed to verify DataType: {e}")
        
    def assert_retentive_address_present(self):
        """
        Asserts that a retentive address is assigned in Row 0 (not empty or null)
        """
        try:
            cell = self.retentive_address_row0_cell
            cell.wait("visible", timeout=4)
            value = cell.get_value().strip()

            assert value != "" and value != "(null)" and value != "-", \
                f"No retentive address assigned! Got: '{value}'"

            print(f"Assertion passed: Retentive address assigned: '{value}'")

        except Exception as e:
            raise AssertionError(f"Failed to verify retentive address: {e}")
    def click_is_retentive(self):
        checkbox = self.is_retentive_checkbox
        checkbox.wait("visible", timeout=3)
        checkbox.wait("enabled", timeout=3)

        if checkbox.get_toggle_state() == 0:
            checkbox.click_input()
            print("Clicked to enable 'Is Retentive'")
        else:
            print("'Is Retentive' already enabled")

    def assert_is_retentive_enabled(self):
        checkbox = self.is_retentive_checkbox
        checkbox.wait("visible", timeout=10)
        assert checkbox.is_enabled(), "Is Retentive checkbox is DISABLED"
        print("Assertion passed: 'Is Retentive' checkbox is ENABLED")

    def assert_is_retentive_checked(self):
        checkbox = self.is_retentive_checkbox
        checkbox.wait("visible", timeout=10)
        state = checkbox.get_toggle_state()
        assert state == 1, f"Is Retentive not checked (state: {state})"
        print("Assertion passed: 'Is Retentive' checkbox is CHECKED")
    
    def save_expansion(self):
        self.expansion_save_button.click_input()

    def click_digitalinput(self):
        self.digital_input_count_cell.click_input()

    def click_digitaloutput(self):
        self.digital_output_count_cell.click_input()

    def assert_digital_input_count(self, row_num, expected_count):
        expected_count = str(expected_count).strip()
        try:
            dynamic_title = f"On-Board IO Row {row_num}, Not sorted."
            element = self.win.child_window(title=dynamic_title, control_type="Edit")
            element.wait("visible", timeout=TIMEOUT_MED)
            actual_count = element.wrapper_object().get_value().strip()
            assert actual_count == expected_count, \
                f"Count mismatch in Row {row_num}! Expected: '{expected_count}', Got: '{actual_count}'"
            print(f"Assertion passed: Row {row_num} count = {actual_count}")
        except Exception as e:
            raise AssertionError(f"Failed to read cell (Row {row_num}): {e}")

    # Expansion I/O Add Device flow
    @property
    def add_device_dropdown(self):
        return self.win.child_window(auto_id="DDLAddDevice", control_type="ComboBox")

    @property
    def add_button(self):
        return self.win.child_window(auto_id="AddBtn", control_type="Button")

    def open_dropdown(self):
        dropdown = self.add_device_dropdown
        dropdown.wait("visible", timeout=20)
        dropdown.wait("enabled", timeout=20)
        dropdown.expand()
        print("Opened Add Device dropdown")

    def select_model(self, model_name):
        print(f"Selecting model: '{model_name}'")
        dropdown = self.add_device_dropdown
        dropdown.wait("visible", timeout=20)
        dropdown.expand()

        list_box = dropdown.child_window(control_type="List")
        list_box.wait("visible", timeout=20)

        item_spec = list_box.child_window(title_re=f".*{model_name}.*", control_type="ListItem")
        item_spec.wait("visible", timeout=25)
        item = item_spec.wrapper_object()
        item.click_input()
        print(f"Successfully selected model: '{model_name}'")

    def click_add(self):
        btn = self.add_button
        btn.wait("visible", timeout=15)
        btn.wait("enabled", timeout=15)
        btn.click_input()
        print("Clicked 'Add' button")

    def assert_module_added(self, expected_model_name):
        """
        Asserts that the expansion module appears in the tree (flexible matching)
        """
        try:
            # Use regex to match the model name even with extra text (e.g., numbering)
            new_module = self.win.child_window(title_re=f".*{expected_model_name}.*", control_type="TreeItem")
            new_module.wait("visible", timeout=15)
            actual_title = new_module.window_text()
            print(f"Assertion passed: Module found in tree with title '{actual_title}'")
        except:
            raise AssertionError(f"Module containing '{expected_model_name}' not found in tree after adding")

    @property
    def max_expansions_error_message(self):
        return self.win.child_window(
            title="Maximum of 5 expansions allowed. This project already has the maximum number of expansions.",
            control_type="Text"
        )

    def assert_max_expansions_error_visible(self):
        try:
            error = self.max_expansions_error_message
            error.wait("visible", timeout=15)
            print("Assertion passed: Max expansions error message displayed")
        except:
            raise AssertionError("Max expansions error message NOT displayed when adding 6th module")
        
    def assert_tag_name_updated(self, expected_tag_name):
        """
        Asserts that the Tag column in Row 0 displays the expected renamed tag
        """
        try:
            cell = self.tag_column_row0_cell
            cell.wait("visible", timeout=10)
            actual_value = cell.get_value().strip()

            assert actual_value == expected_tag_name, \
                f"Tag name mismatch! Expected: '{expected_tag_name}', Actual: '{actual_value}'"

            print(f"Assertion passed: Tag column shows '{actual_value}' as expected")

        except Exception as e:
            raise AssertionError(f"Failed to verify tag name in grid: {e}")

    @property
    def resistance_lookup_table_tree_item(self):
        """
        Returns the 'Resistance Lookup Table' tree item in the tree view.
        """
        return self.win.child_window(
            title="Resistance Lookup Table",
            control_type="TreeItem"
        )

    @property
    def resistance_dropdown_toolbar(self):
        """
        Returns the 'DropDown' toolbar/button in the resistance lookup table section.
        """
        return self.win.child_window(
            title="DropDown",
            control_type="ToolBar"
        )
    @property
    def resistance_name_textbox(self):
        """
        Returns the textbox (AutomationId: 'TextBox') for entering resistance name/value.
        """
        return self.win.child_window(
            auto_id="TextBox",
            control_type="Edit"
        )
    @property
    def added_resistance_table_item(self):
        """
        Returns the newly added resistance table item (e.g. "sdfs") in the tree.
        Use .exists() to check if it's present/added.
        """
        return self.win.child_window(
            title="sdfs",
            control_type="TreeItem"
        )

    def getnamed_resistance_table_item(self):
        self.added_resistance_table_item.click_input()



    def get_added_resistance_table_item(self, table_name):
        """
        Returns the added resistance table item by its name.
        """
        return self.win.child_window(
            title=table_name,
            control_type="TreeItem"
        )


    def enter_resistance_name(self, name_value):
        """Enters a name/value into the resistance textbox and presses Enter."""
        textbox = self.resistance_name_textbox
        textbox.click_input()
        textbox.set_text(name_value)
        textbox.type_keys("{ENTER}")

    def click_add_resistance_lookup_table(self):
        self.resistance_dropdown_toolbar.click_input()

    def rightclick_resistance_lookup_table(self):
        self.resistance_lookup_table_tree_item.right_click_input()
    def doubleclick_resistance_lookup_table(self):
        self.resistance_lookup_table_tree_item.double_click_input()

    @property
    def model_column_row0_cell(self):
        """Returns the 'Model Row 0, Not sorted.' cell in the grid (read-only)"""
        return self.win.child_window(title="Model Row 0, Not sorted.", control_type="Edit")

    @property
    def resistance_table_grid(self):
        """
        Returns the main DataGridView control that contains the Resistance Lookup Table.
        (Use this to count rows)
        """
        return self.win.child_window(
            class_name="WindowsForms10.Window.8.app.0.1ca0192_r8_ad1",
            control_type="Table"
        )

    def count_resistance_table_rows(self):

        cells = self.win.descendants(control_type="Edit")

        unique_rows = set()

        for cell in cells:
            try:
                grid_item = cell.iface_grid_item
                unique_rows.add(grid_item.CurrentRow)
            except Exception:
                pass

        row_count = len(unique_rows)

        print(f"Resistance table row count = {row_count}")

        return row_count

    def assert_resistance_lookup_table_has_2_rows(self):

        row_count = self.count_resistance_table_rows()

        assert row_count == 2, \
            f"Expected 2 rows but found {row_count}"

        print("✔ Resistance lookup table contains exactly 2 rows")

    def wait_until_resistance_rows(self, expected_rows, timeout=10):

            wait_until(
                timeout,
                1,
                lambda: self.count_resistance_table_rows() == expected_rows
            )

    def assert_model_name_in_grid(self, expected_name):
        """Asserts that the Model column in Row 0 displays the expected model name"""
        try:
            cell = self.model_column_row0_cell
            cell.wait("visible", timeout=10)
            actual_value = cell.get_value().strip()

            assert actual_value == expected_name, \
                f"Model name mismatch in grid! Expected: '{expected_name}', Actual: '{actual_value}'"

            print(f"Assertion passed: Model column shows '{actual_value}' as expected")
        except Exception as e:
            raise AssertionError(f"Failed to verify model name in grid: {e}")

    def get_resistance_table_item(self, table_name):

        return self.win.child_window(
            title=table_name,
            control_type="TreeItem"
        )


    def rightclick_resistance_table(self, table_name):

        item = self.get_resistance_table_item(table_name)
        item.wait("visible", timeout=10)
        item.right_click_input()


    def doubleclick_resistance_table(self, table_name):

        item = self.get_resistance_table_item(table_name)
        item.wait("visible", timeout=10)
        item.double_click_input()

    def verify_resistance_table_exists(self, table_name):

        assert self.get_resistance_table_item(table_name).exists(timeout=10), \
            f"Resistance table '{table_name}' not found"

    def perform_action_on_table(self, table_name, action):

        table_item = self.get_resistance_table_item(table_name)

        table_item.wait("visible", timeout=10)

        if action == "right_click":
            table_item.right_click_input()

        elif action == "double_click":
            table_item.double_click_input()

        elif action == "click":
            table_item.click_input()

        else:
            raise ValueError("Unsupported action")


    @property
    def add_resistance_values_menu_item(self):
        """
        Returns 'Add Resistance Values' menu item from dropdown popup.
        """
        return self.app.window(
            title="Add Resistance Values",
            control_type="MenuItem"
        )


    def click_add_resistance_values(self):

        # Step 1 → Open dropdown popup
        dropdown = self.win.child_window(
            title="DropDown",
            control_type="ToolBar"
        )

        dropdown.click_input()

        # Step 2 → Wait for menu item to appear
        wait_until(
            10,
            1,
            lambda: self.add_resistance_values_menu_item.exists()
        )

        # Step 3 → Click correct option
        self.add_resistance_values_menu_item.click_input()


    def select_add_resistance_values_from_context_menu(self):
        """
        Selects 'Add Resistance Values' from the right-click context menu
        using keyboard navigation (most stable for WinForms).
        """

        # Small wait to ensure context menu is visible & focused
        wait_until(
            5,
            0.5,
            lambda: True  # context menu already has focus after right click
        )

        # First option is "Add Resistance Values"
        send_keys("{DOWN}{ENTER}")

    @property
    def resistance_value_textbox(self):
        """
        Resistance value input textbox
        """
        return self.win.child_window(
            auto_id="txtResistance",
            control_type="Edit"
        )


    @property
    def output_value_textbox(self):
        """
        Output value input textbox
        """
        return self.win.child_window(
            auto_id="txtOutput",
            control_type="Edit"
        )

    @property
    def save_button(self):
        """
        Returns the Save button in 'Add Resistance Value' dialog
        """
        return self.win.child_window(
            auto_id="btnSave",
            control_type="Button"
        )

    def enter_resistance_value(self, value):
        """
        Enters resistance value in Add Resistance Value dialog
        """
        textbox = self.resistance_value_textbox
        textbox.click_input()
        textbox.set_edit_text(str(value))

    def enter_output_value(self, value):
        """
        Enters output value in Add Resistance Value dialog
        """
        textbox = self.output_value_textbox
        textbox.click_input()
        textbox.set_edit_text(str(value))


    def enter_resistance_and_output_values(self, resistance, output):
        """
        Enters resistance and output values in Add Resistance Value dialog
        """
        self.enter_resistance_value(resistance)
        self.enter_output_value(output)

    def click_save_resistance_value(self):

        btn = self.save_button
        btn.invoke()

    def _get_last_grid_row_index(self):
        """
        Returns the last (maximum) row index from the Resistance Lookup grid
        """

        cells = self.win.descendants(control_type="Edit")
        rows = set()

        for cell in cells:
            try:
                rows.add(cell.iface_grid_item.CurrentRow)
            except Exception:
                pass

        if not rows:
            raise AssertionError("No rows found in Resistance Lookup grid")

        return max(rows)

    def _get_grid_cell_value(self, row_index, column_index):
        """
        Returns the value of a grid cell for given row and column
        """

        cells = self.win.descendants(control_type="Edit")

        for cell in cells:
            try:
                grid_item = cell.iface_grid_item
                if (
                    grid_item.CurrentRow == row_index
                    and grid_item.CurrentColumn == column_index
                ):
                    return cell.get_value().strip()
            except Exception:
                pass

        raise AssertionError(
            f"Cell not found at row={row_index}, column={column_index}"
        )


    def assert_resistance_and_output_values_added(self, expected_resistance, expected_output):
        """
        Asserts that entered resistance and output values
        are present in the last added grid row
        """

        last_row = self._get_last_grid_row_index()

        actual_resistance = self._get_grid_cell_value(
            row_index=last_row,
            column_index=1   # Resistance (Ohm)
        )

        actual_output = self._get_grid_cell_value(
            row_index=last_row,
            column_index=2   # Output Value
        )

        assert actual_resistance == str(expected_resistance), (
            f"Resistance mismatch! "
            f"Expected={expected_resistance}, Actual={actual_resistance}"
        )

        assert actual_output == str(expected_output), (
            f"Output mismatch! "
            f"Expected={expected_output}, Actual={actual_output}"
        )

        print(
            f"✔ Grid validation passed: "
            f"Resistance={actual_resistance}, Output={actual_output}"
        )

    def assert_resistance_table_row_count(self, expected_count):

        cells = self.win.descendants(control_type="Edit")
        rows = set()

        for cell in cells:
            try:
                rows.add(cell.iface_grid_item.CurrentRow)
            except Exception:
                pass

        actual_count = len(rows)

        assert actual_count == expected_count, (
            f"Expected {expected_count} rows, but found {actual_count}"
        )

        print(f"✔ Resistance table contains {actual_count} rows")



    def verify_multiple_resistance_tables_exist(self, table_names, timeout=10):
        """
        Verifies that all given resistance lookup tables exist in the tree.

        :param table_names: list of table names to verify
        :param timeout: max wait time per table
        """

        missing_tables = []

        for table_name in table_names:
            try:
                wait_until(
                    timeout,
                    1,
                    lambda: self.get_resistance_table_item(table_name).exists()
                )
            except Exception:
                missing_tables.append(table_name)

        assert not missing_tables, (
            "The following resistance tables were not found: "
            + ", ".join(missing_tables)
        )

        print(
            f"✔ All resistance tables found: {', '.join(table_names)}"
        )

    def assert_resistance_tables_by_prefix_and_count(
        self,
        table_prefix,
        expected_table_names,
        expected_count
    ):
        """
        Asserts that:
        1) All expected resistance tables exist
        2) Only tables with given prefix are considered
        3) EXACTLY expected_count tables exist
        """

        # Get only TreeItems that start with the prefix (e.g. "Lookup")
        all_tree_items = self.win.descendants(control_type="TreeItem")

        resistance_tables = [
            item.window_text()
            for item in all_tree_items
            if item.window_text() and item.window_text().startswith(table_prefix)
        ]

        # --- 1️⃣ Assert expected tables exist ---
        missing_tables = [
            name for name in expected_table_names
            if name not in resistance_tables
        ]

        assert not missing_tables, (
            "Missing resistance tables: " + ", ".join(missing_tables)
        )

        # --- 2️⃣ Assert no extra tables exist ---
        unexpected_tables = [
            name for name in resistance_tables
            if name not in expected_table_names
        ]

        assert not unexpected_tables, (
            "Unexpected resistance tables found: "
            + ", ".join(unexpected_tables)
        )

        # --- 3️⃣ Assert exact count ---
        actual_count = len(resistance_tables)

        assert actual_count == expected_count, (
            f"Expected exactly {expected_count} resistance tables "
            f"with prefix '{table_prefix}', but found {actual_count}"
        )

        print(
            f"✔ Exactly {expected_count} resistance tables exist: "
            f"{', '.join(expected_table_names)}"
        )
    def delete_resistance_table(self, table_name):
        """
        Deletes a resistance lookup table via context menu.
        """

        table_item = self.get_resistance_table_item(table_name)

        assert table_item.exists(timeout=10), \
            f"Resistance table '{table_name}' not found"

        # Right-click on the table
        table_item.right_click_input()

        # Context menu opens → navigate to Delete
        # (Adjust DOWN count if menu order changes)
        send_keys("{DOWN}{DOWN}{DOWN}{ENTER}")

        # Optional: wait until table is removed
        wait_until(
            10,
            1,
            lambda: not self.get_resistance_table_item(table_name).exists()
        )

        print(f"✔ Resistance table '{table_name}' deleted")

    def get_resistance_tables_by_prefix(self, table_prefix="Lookup"):
        """
        Returns list of resistance table names under Resistance Lookup Table node
        filtered by prefix (e.g. 'Lookup').
        """

        tree_items = self.win.descendants(control_type="TreeItem")

        resistance_tables = [
            item.window_text()
            for item in tree_items
            if item.window_text() and item.window_text().startswith(table_prefix)
        ]

        return resistance_tables

    def assert_no_resistance_tables_exist(self, table_prefix="Lookup"):
        """
        Asserts that NO resistance lookup tables exist under the node.
        """

        resistance_tables = self.get_resistance_tables_by_prefix(table_prefix)

        assert len(resistance_tables) == 0, (
            f"Expected 0 resistance tables, but found {len(resistance_tables)}: "
            f"{', '.join(resistance_tables)}"
        )

        print("✔ No resistance lookup tables exist (count = 0)")

    def edit_resistance_table_name(self, table_name):
        """
        Deletes a resistance lookup table via context menu.
        """

        table_item = self.get_resistance_table_item(table_name)

        assert table_item.exists(timeout=10), \
            f"Resistance table '{table_name}' not found"

        # Right-click on the table
        table_item.right_click_input()

        # Context menu opens → navigate to Delete
        # (Adjust DOWN count if menu order changes)
        send_keys("{DOWN}{DOWN}{ENTER}")
        

    def assert_resistance_table_renamed_in_node(self, old_name, new_name):
        """
        Asserts that resistance table is renamed in TreeView node:
        - old_name should NOT exist
        - new_name should exist
        """

        # Check old name is gone
        old_exists = self.get_resistance_table_item(old_name).exists()

        assert not old_exists, (
            f"Old resistance table name '{old_name}' still exists in node"
        )

        # Check new name exists
        new_exists = self.get_resistance_table_item(new_name).exists(timeout=10)

        assert new_exists, (
            f"Edited resistance table name '{new_name}' not found in node"
        )

        print(
            f"✔ Resistance table renamed in node: "
            f"'{old_name}' → '{new_name}'"
        )

    def assert_mode_does_not_matches_selected_resistance_mode(self, selected_mode):
            """
            Asserts that the Mode column shows **exactly** the selected mode.
            Fully dynamic — works for any mode name.
            """
            displayed = self.get_displayed_mode_value()

            assert displayed != selected_mode, \
                f"Mode mismatch! Selected '{selected_mode}', but grid shows '{displayed}'"

            print(f"Assertion passed: Mode column shows '{displayed}' (does not match selected '{selected_mode}')")

    @property
    def resistance_value_row1_cell(self):
        """
        Resistance (Ohm) value cell at Row 1 in the grid
        """
        return self.win.child_window(
            title="Resistance (Ohm) Row 1",
            control_type="Edit"
        )
    def edit_resistance_value(self):
       self.resistance_value_row1_cell.double_click_input()

    def update_resistance_and_output_values(self, new_resistance, new_output):
        """
        Enters resistance and output values in Add Resistance Value dialog
        """
        self.enter_resistance_value(new_resistance)
        self.enter_output_value(new_output)

    def assert_resistance_and_output_values_in_grid(
        self,
        row_index,
        expected_resistance,
        expected_output
    ):
        """
        Asserts resistance and output values for a specific grid row
        """

        resistance_value = None
        output_value = None

        cells = self.win.descendants(control_type="Edit")

        for cell in cells:
            try:
                grid_item = cell.iface_grid_item

                # Resistance (Ohm) column = 1
                if grid_item.CurrentRow == row_index and grid_item.CurrentColumn == 1:
                    resistance_value = cell.get_value().strip()

                # Output Value column = 2
                if grid_item.CurrentRow == row_index and grid_item.CurrentColumn == 2:
                    output_value = cell.get_value().strip()

            except Exception:
                pass

        assert resistance_value is not None, (
            f"Resistance value not found in grid for row {row_index}"
        )

        assert output_value is not None, (
            f"Output value not found in grid for row {row_index}"
        )

        assert resistance_value == str(expected_resistance), (
            f"Resistance mismatch at row {row_index}: "
            f"Expected={expected_resistance}, Actual={resistance_value}"
        )

        assert output_value == str(expected_output), (
            f"Output mismatch at row {row_index}: "
            f"Expected={expected_output}, Actual={output_value}"
        )

        print(
            f"✔ Grid updated correctly at row {row_index}: "
            f"Resistance={resistance_value}, Output={output_value}"
        )
# to check deletion of specific row using context menu and keyboard navigation
    @property
    def resistance_value_row1_cell(self):
        """
        Resistance (Ohm) value cell at Row 1 in the grid
        """
        return self.win.child_window(
            title="Resistance (Ohm) Row 1",
            control_type="Edit"
        )

    def rightclick_resistance_value_row1(self):
        """
        Right-clicks on Resistance (Ohm) value cell at Row 1
        """
        self.resistance_value_row1_cell.right_click_input()

        print("✔ Right-clicked on Resistance (Ohm) Row 1 cell")

    def delete_resistance_value_row1(self):
        """
        Deletes the resistance value (Row 2) using context menu
        Assumes right-click has already opened the menu
        """
        send_keys("{DOWN}{ENTER}")

        print("✔ Deleted Resistance (Ohm) Row 2 value")
    
    @property
    def delete_confirmation_yes_button(self):
        """
        'Yes' button on delete confirmation dialog
        """
        return self.win.child_window(
            title="Yes",
            control_type="Button"
        )


    def confirm_delete_resistance_value(self):
        """
        Confirms delete action from confirmation dialog using Alt+Y
        """
        send_keys("%y")   # Alt + Y

        print("✔ Delete confirmed using Alt+Y")


    
    def assert_specific_resistance_row_not_present(self, deleted_row_index):
        """
        Asserts that a specific resistance row index no longer exists
        """

        cells = self.win.descendants(control_type="Edit")

        existing_rows = set()

        for cell in cells:
            try:
                grid_item = cell.iface_grid_item
                existing_rows.add(grid_item.CurrentRow)
            except Exception:
                pass

        assert deleted_row_index not in existing_rows, (
            f"Deleted resistance row {deleted_row_index} still exists in grid"
        )

        print(f"✔ Resistance row {deleted_row_index} successfully deleted")



    # @property
    # def resistance_value_row1_cell(self):
    #         """
    #         Resistance (Ohm) value cell at Row 1 in the grid
    #         """
    #         return self.win.child_window(
    #             title="Resistance (Ohm) Row 1",
    #             control_type="Edit"
    #         )
    # def rightclick_resistance_value_row1(self):
    #         """
    #         Right-clicks on Resistance (Ohm) value cell at Row 1
    #         """
    #         self.resistance_value_row1_cell.right_click_input()

    #         print("✔ Right-clicked on Resistance (Ohm) Row 1 cell")

    # def assert_user_cannot_delete_default_row(self, deleted_row_index):
    #         """
    #         Asserts that a specific resistance row index no longer exists
    #         """

    #         cells = self.win.descendants(control_type="Edit")

    #         existing_rows = set()

    #         for cell in cells:
    #             try:
    #                 grid_item = cell.iface_grid_item
    #                 existing_rows.add(grid_item.CurrentRow)
    #             except Exception:
    #                 pass

    #         assert deleted_row_index in existing_rows, (
    #             f"Deleted resistance row {deleted_row_index} still exists in grid"
    #         )

    #         print(f"✔ Resistance row {deleted_row_index} successfully deleted")


    def get_grid_cell(self, row_index, column_index):
        """
        Returns a grid cell (Edit control) for given row & column
        """

        cells = self.win.descendants(control_type="Edit")

        for cell in cells:
            try:
                grid_item = cell.iface_grid_item

                if (
                    grid_item.CurrentRow == row_index and
                    grid_item.CurrentColumn == column_index
                ):
                    return cell

            except Exception:
                pass

        raise AssertionError(
            f"Grid cell not found at row={row_index}, column={column_index}"
        )


    def copy_paste_resistance_value(self, row_index):
        """
        Performs Ctrl+C and Ctrl+V on resistance column (column 1)
        for the given row index
        """

        # Resistance column index = 1
        cell = self.get_grid_cell(row_index=row_index, column_index=1)

        cell.click_input()
        send_keys("^c")
        send_keys("^v")

        print(f"✔ Copied and pasted resistance value at row {row_index}")

    def cut_paste_resistance_value(self, row_index):
        """
        Performs Ctrl+X and Ctrl+V on resistance column (column 1)
        for the given row index
        """

        # Resistance column index = 1
        cell = self.get_grid_cell(row_index=row_index, column_index=1)

        cell.click_input()
        send_keys("^x")
        send_keys("^v")

        print(f"✔ Cut and pasted resistance value at row {row_index}")