import time
from pywinauto import Desktop, Application
from pywinauto.keyboard import send_keys
from config import TIMEOUT_MED
from pywinauto.timings import always_wait_until, TimeoutError
from pywinauto.timings import wait_until
from pywinauto.timings import wait_until

class ResistanceLookupPage:

    def __init__(self, app, win):
        self.app = app
        self.win = win

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
    @property
    def add_resistance_values_menu_item(self):
        """
        Returns 'Add Resistance Values' menu item from dropdown popup.
        """
        return self.app.window(
            title="Add Resistance Values",
            control_type="MenuItem"
        )
	
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
	
    @property
    def resistance_value_row1_cell(self):
        """
        Resistance (Ohm) value cell at Row 1 in the grid
        """
        return self.win.child_window(
            title="Resistance (Ohm) Row 1",
            control_type="Edit"
        )
	
    @property
    def resistance_value_row1_cell(self):
        """
        Resistance (Ohm) value cell at Row 1 in the grid
        """
        return self.win.child_window(
            title="Resistance (Ohm) Row 1",
            control_type="Edit"
        )
	
    @property
    def delete_confirmation_yes_button(self):
        """
        'Yes' button on delete confirmation dialog
        """
        return self.win.child_window(
            title="Yes",
            control_type="Button"
        )
# @property
    # def resistance_value_row1_cell(self):
    #         """
    #         Resistance (Ohm) value cell at Row 1 in the grid
    #         """
    #         return self.win.child_window(
    #             title="Resistance (Ohm) Row 1",
    #             control_type="Edit"
    #         )


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