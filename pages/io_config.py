# pages/io_config.py
import time
from pywinauto import Desktop, Application
from pywinauto.keyboard import send_keys
from config import TIMEOUT_MED
from pywinauto.timings import always_wait_until, TimeoutError


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

    def get_label_cell(self, row_index):
        """Returns the 'Label Row X, Not sorted.' cell for a given row"""
        title = f"Label Row {row_index}, Not sorted."
        return self.win.child_window(title=title, control_type="Edit")

    def assert_aiao_has_2_ai_and_2_ao(self):
        """
        Asserts that AIAO module shows:
        - Row 0: AI0
        - Row 1: AI1
        - Row 4: AO0
        - Row 5: AO1
        (Typical layout for AI2-AO2 modules)
        """
        expected_labels = {
            0: "AI0",
            1: "AI1",
            4: "AO0",
            5: "AO1"
        }

        found = {}
        for row, expected in expected_labels.items():
            try:
                cell = self.get_label_cell(row)
                cell.wait("visible", timeout=10)
                actual = cell.get_value().strip()
                assert actual == expected, \
                    f"Row {row} Label mismatch! Expected '{expected}', got '{actual}'"
                found[row] = actual
                print(f"Row {row}: Label '{actual}' - correct")
            except Exception as e:
                raise AssertionError(f"Failed to find Label in Row {row}: {e}")

        print("Assertion passed: AIAO module has 2 AI (AI0, AI1) and 2 AO (AO0, AO1) labels")
    
    def assert_or_tags_present(self, expected_count=4):
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
                    if tag_value.endswith("_OR"):
                        or_tags_found += 1
                        print(f"Found OR tag in Row {row}: '{tag_value}'")
                except:
                    continue  # Skip if row not present

            assert or_tags_found == expected_count, \
                f"Expected {expected_count} OR tags, but found {or_tags_found}"

            print(f"Assertion passed: {or_tags_found} OR tags found as expected")

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
    
    