# pages/dialogs.py
import time
from pywinauto.timings import always_wait_until
from config import TIMEOUT_MED
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
    def btn_save(self):
        return self.dlg.child_window(auto_id="btnSave", control_type="Button")

    @property
    def btn_cancel(self):
        return self.dlg.child_window(auto_id="btnCancel", control_type="Button")

    @property
    def datatype_dropdown(self):
        return self.dlg.child_window(
            auto_id="comboBoxIOType",
            control_type="ComboBox"
        )
    
    @property
    def error_message(self):
        """Returns the validation error message text element."""
        return self.dlg.child_window(
            title="Please correct the errors before saving.",
            control_type="Text"
        )

    def assert_error_message_visible(self, expected_message="Please correct the errors before saving."):
        """
        Asserts that the error message is visible with the expected text.
        Fails the test if the message doesn't appear.
        """
        try:
            self.error_message.wait("visible", timeout=5)
            actual_text = self.error_message.window_text()
            assert actual_text == expected_message, (
                f"Error message mismatch: expected '{expected_message}', got '{actual_text}'"
            )
            print(f"✔ Error message displayed: '{actual_text}'")
        except Exception as e:
            raise AssertionError(
                f"Expected error message '{expected_message}' did not appear. "
                f"Test should fail because validation didn't trigger."
            ) from e
    
    def select_datatype(self, value="Byte"):
        combo = self.datatype_dropdown
        combo.wait("visible enabled", timeout=10)
        combo.select(value)  # expands, selects, and collapses cleanly
        print(f"✔ Data type set to: {value}")

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
        print(f"✔ Double-clicked row {row} to open edit dialog")
        time.sleep(0.5)  # brief pause for dialog to appear

    def fill(self, tag_name, logical_addr=""):
        self.txt_tag.set_text(tag_name)
        if logical_addr:
            self.txt_logical_address.set_text(logical_addr)
    def fill_update(self, tag_name):
        self.txt_tag.set_text(tag_name)
    
    def save(self):
        self.btn_save.click_input()
        time.sleep(0.5)          # tiny pause for UI to settle

    def cancel(self):
        self.btn_cancel.click_input()


  