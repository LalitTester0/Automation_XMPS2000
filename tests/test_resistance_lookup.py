import time
import pytest
from config import DEFAULT_TAG_NAME, DEFAULT_LOGICAL_ADDR
from pages import io_config
from pages.dialogs import NewProjectDialog
from pywinauto.keyboard import send_keys
from pathlib import Path
from pywinauto import Application
import pywinauto
import sys
import pyperclip
from excel_report import update_excel_result
from tests.conftest import project_page

def test_2_default_row_count_for_resistance_table(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.click_ioconfig()

    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name("sdfs")
    io_config.doubleclick_resistance_lookup_table()

    io_config.wait_until_resistance_rows(2)

    io_config.assert_resistance_lookup_table_has_2_rows()
    print("Test passed: Resistance lookup table has 2 rows!")  



def test_add_resistance_value(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"
    RESISTANCE = 143
    OUTPUT = 455


    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.click_ioconfig()

    # Add resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME)
    io_config.doubleclick_resistance_lookup_table()

    io_config.verify_resistance_table_exists(TABLE_NAME)

    # Right click on created table
    io_config.rightclick_resistance_table(TABLE_NAME)

    # Select "Add Resistance Values" via keyboard
    io_config.select_add_resistance_values_from_context_menu()

    io_config.enter_resistance_and_output_values(RESISTANCE, OUTPUT)
    io_config.click_save_resistance_value()

    io_config.assert_resistance_and_output_values_added(
    expected_resistance=RESISTANCE,
    expected_output=OUTPUT
)

def test_add_resistance_value_limit_20(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"

    # Prepare 10 resistance-output pairs
    resistance_data = [
        (101, 10),
        (200, 20),
        (300, 30),
        (400, 40),
        (500, 50),
        (600, 60),
        (700, 70),
        (800, 80),
        (900, 90),
        (1000, 100),
        (1012, 10),
        (2002, 20),
        (3003, 30),
        (4004, 40),
        (5006, 50),
        (6006, 60),
        (7007, 70),
        (8008, 80),
    ]

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.click_ioconfig()

    # Create resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME)
    io_config.doubleclick_resistance_lookup_table()

    io_config.verify_resistance_table_exists(TABLE_NAME)

    # Add 10 resistance-output values
    for resistance, output in resistance_data:

        io_config.rightclick_resistance_table(TABLE_NAME)
        io_config.select_add_resistance_values_from_context_menu()

        io_config.enter_resistance_and_output_values(resistance, output)
        io_config.click_save_resistance_value()

    # Optional final validation
    io_config.assert_resistance_table_row_count(expected_count=20)


def test_add_table_limit5(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_PREFIX = "Lookup"

    table_names = [
        "Lookup_table",
        "Lookup_table1",
        "Lookup_table2",
        "Lookup_table3",
        "Lookup_table5",
    ]

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.click_ioconfig()

    # Add first table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(table_names[0])

    # Expand parent node
    io_config.doubleclick_resistance_lookup_table()
    io_config.verify_resistance_table_exists(table_names[0])

    # Add remaining tables
    for table_name in table_names[1:]:
        io_config.rightclick_resistance_lookup_table()
        io_config.click_add_resistance_lookup_table()
        io_config.enter_resistance_name(table_name)
        io_config.verify_resistance_table_exists(table_name)

    # ✅ FINAL ASSERTION (prefix + count)
    io_config.assert_resistance_tables_by_prefix_and_count(
        table_prefix=TABLE_PREFIX,
        expected_table_names=table_names,
        expected_count=5
    )

def test_delete_resistance_table(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.click_ioconfig()

    # Add resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME)

    # Expand node so table is visible
    io_config.doubleclick_resistance_lookup_table()
    io_config.verify_resistance_table_exists(TABLE_NAME)

    # Delete the table
    io_config.delete_resistance_table(TABLE_NAME)

    # ✅ FINAL ASSERTION → NO tables should exist
    io_config.assert_no_resistance_tables_exist(table_prefix="Lookup")

def test_edit_resistance_tablename(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"
    EDITED_NAME = "Edited_table"

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.click_ioconfig()

    # Add resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME)

    # Expand node so table is visible
    io_config.doubleclick_resistance_lookup_table()
    io_config.verify_resistance_table_exists(TABLE_NAME)

    # Edit table name
    io_config.edit_resistance_table_name(TABLE_NAME)
    io_config.enter_resistance_name(EDITED_NAME)

    # Existing verify (kept)
    io_config.verify_resistance_table_exists(EDITED_NAME)

    # ✅ STRONG RENAME ASSERTION
    io_config.assert_resistance_table_renamed_in_node(
        old_name=TABLE_NAME,
        new_name=EDITED_NAME
    )

def test_resistance_table_in_universal_mode(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"
    EXPANSION_MODEL = "XBLD-UI4-UO2"
    selected_mode = "Lookup_table"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.click_ioconfig()
    # Add resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME) 
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.select_mode(selected_mode)
    time.sleep(2)
    io_config.save_expansion()
    io_config.assert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

def test_edited_resistance_table_in_universal_mode(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"
    EXPANSION_MODEL = "XBLD-UI4-UO2"
    EDITED_NAME = "Modified_table"
    selected_mode = "Modified_table"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.click_ioconfig()
    # Add resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME) 
    io_config.doubleclick_resistance_lookup_table()
    io_config.verify_resistance_table_exists(TABLE_NAME)
    io_config.edit_resistance_table_name(TABLE_NAME)
    io_config.enter_resistance_name(EDITED_NAME)
    io_config.verify_resistance_table_exists(EDITED_NAME)
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.select_mode(selected_mode)
    time.sleep(2)
    io_config.save_expansion()
    io_config.assert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

    
#HOLD
# def test_delete_resistance_table_in_universal_mode(main_page, project_page, io_config):

#     PLC_MODEL = "XBLD-14E"
#     TABLE_NAME = "Lookup_table"
#     EXPANSION_MODEL = "XBLD-UI4-UO2"
#     selected_mode = "Lookup_table"   
#     main_page.click_new_project()
#     main_page.select_model_and_confirm(PLC_MODEL)
#     project_page.click_ioconfig()
#     # Add resistance lookup table
#     io_config.rightclick_resistance_lookup_table()
#     io_config.click_add_resistance_lookup_table()
#     io_config.enter_resistance_name(TABLE_NAME) 
#     io_config.doubleclick_resistance_lookup_table()
#     io_config.verify_resistance_table_exists(TABLE_NAME)
#     io_config.delete_resistance_table(TABLE_NAME)
#     io_config.assert_no_resistance_tables_exist(table_prefix="Lookup")
#     project_page.right_click_expansion_io()
#     project_page.click_add_device_expansion()
#     io_config.open_dropdown()
#     io_config.select_model(EXPANSION_MODEL)
#     io_config.click_add()
#     project_page.double_click_expansion()
#     project_page.doubleclick_open_expansion_form()
#     io_config.select_mode(selected_mode)
#     io_config.assert_mode_does_not_matches_selected_resistance_mode(selected_mode)
#     print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")


# def test_add_resistance_value_range(main_page, project_page, io_config):

#     PLC_MODEL = "XBLD-14E"
#     TABLE_NAME = "Lookup_table"
#     RESISTANCE = 2147483647
#     OUTPUT = 2147483647


#     main_page.click_new_project()
#     main_page.select_model_and_confirm(PLC_MODEL)

#     project_page.click_ioconfig()

#     # Add resistance lookup table
#     io_config.rightclick_resistance_lookup_table()
#     io_config.click_add_resistance_lookup_table()
#     io_config.enter_resistance_name(TABLE_NAME)
#     io_config.doubleclick_resistance_lookup_table()

#     io_config.verify_resistance_table_exists(TABLE_NAME)

#     # Right click on created table
#     io_config.rightclick_resistance_table(TABLE_NAME)

#     # Select "Add Resistance Values" via keyboard
#     io_config.select_add_resistance_values_from_context_menu()

#     io_config.enter_resistance_and_output_values(RESISTANCE, OUTPUT)
#     io_config.click_save_resistance_value()

#     io_config.assert_resistance_and_output_values_added(
#     expected_resistance=RESISTANCE,
#     expected_output=OUTPUT
# )

def test_edit_resistance_value(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"
    RESISTANCE = 143
    OUTPUT = 455


    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.click_ioconfig()

    # Add resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME)
    io_config.doubleclick_resistance_lookup_table()

    io_config.verify_resistance_table_exists(TABLE_NAME)

    # Right click on created table
    io_config.rightclick_resistance_table(TABLE_NAME)

    # Select "Add Resistance Values" via keyboard
    io_config.select_add_resistance_values_from_context_menu()

    io_config.enter_resistance_and_output_values(RESISTANCE, OUTPUT)
    io_config.click_save_resistance_value()
    time.sleep(2)
    io_config.edit_resistance_value()
    time.sleep(2)
    io_config.update_resistance_and_output_values(new_resistance=123, new_output=189)
    io_config.click_save_resistance_value()
    io_config.assert_resistance_and_output_values_in_grid(
    row_index=1,
    expected_resistance=123,
    expected_output=189
)

# def test_delete_resistance_value(main_page, project_page, io_config):

#     PLC_MODEL = "XBLD-14E"
#     TABLE_NAME = "Lookup_table"
#     RESISTANCE = 143
#     OUTPUT = 455


#     main_page.click_new_project()
#     main_page.select_model_and_confirm(PLC_MODEL)

#     project_page.click_ioconfig()

#     # Add resistance lookup table
#     io_config.rightclick_resistance_lookup_table()
#     io_config.click_add_resistance_lookup_table()
#     io_config.enter_resistance_name(TABLE_NAME)
#     io_config.doubleclick_resistance_lookup_table()

#     io_config.verify_resistance_table_exists(TABLE_NAME)

#     # Right click on created table
#     io_config.rightclick_resistance_table(TABLE_NAME)

#     # Select "Add Resistance Values" via keyboard
#     io_config.select_add_resistance_values_from_context_menu()

#     io_config.enter_resistance_and_output_values(RESISTANCE, OUTPUT)
#     io_config.click_save_resistance_value()
#     io_config.rightclick_resistance_value_row1()
#     io_config.delete_resistance_value_row1()
#     io_config.confirm_delete_resistance_value()
#     io_config.assert_specific_resistance_row_not_present(deleted_row_index=2)

# def test_user_cannot_delete_default_resistance_value(main_page, project_page, io_config):

#     PLC_MODEL = "XBLD-14E"
#     TABLE_NAME = "Lookup_table"
#     main_page.click_new_project()
#     main_page.select_model_and_confirm(PLC_MODEL)

#     project_page.click_ioconfig()

#     # Add resistance lookup table
#     io_config.rightclick_resistance_lookup_table()
#     io_config.click_add_resistance_lookup_table()
#     io_config.enter_resistance_name(TABLE_NAME)
#     io_config.doubleclick_resistance_lookup_table()

#     io_config.verify_resistance_table_exists(TABLE_NAME)

#     # Right click on created table
#     io_config.rightclick_resistance_table(TABLE_NAME)
#     io_config.delete_resistance_value_row1()
#     io_config.confirm_delete_resistance_value()
#     io_config.assert_user_cannot_delete_default_row(deleted_row_index=1)

def test_copy_resistance_value(main_page, project_page, io_config):

    PLC_MODEL = "XBLD-14E"
    TABLE_NAME = "Lookup_table"
    RESISTANCE = 143
    OUTPUT = 455

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.click_ioconfig()

    # Add resistance lookup table
    io_config.rightclick_resistance_lookup_table()
    io_config.click_add_resistance_lookup_table()
    io_config.enter_resistance_name(TABLE_NAME)
    io_config.doubleclick_resistance_lookup_table()
    io_config.verify_resistance_table_exists(TABLE_NAME)

    # Right click on created table
    io_config.rightclick_resistance_table(TABLE_NAME)

    # Select "Add Resistance Values" via keyboard
    io_config.select_add_resistance_values_from_context_menu()

    io_config.enter_resistance_and_output_values(RESISTANCE, OUTPUT)
    io_config.click_save_resistance_value()
    io_config.copy_paste_resistance_value(row_index=0)
    io_config.update_resistance_and_output_values(new_resistance=146, new_output=189)
    io_config.click_save_resistance_value()
    io_config.assert_resistance_and_output_values_in_grid(
    row_index=3,
    expected_resistance=146,
    expected_output=189
    )

#Hold
# def test_cut_resistance_value(main_page, project_page, io_config):

#     PLC_MODEL = "XBLD-14E"
#     TABLE_NAME = "Lookup_table"
#     RESISTANCE = 143
#     OUTPUT = 455

#     main_page.click_new_project()
#     main_page.select_model_and_confirm(PLC_MODEL)

#     project_page.click_ioconfig()

#     # Add resistance lookup table
#     io_config.rightclick_resistance_lookup_table()
#     io_config.click_add_resistance_lookup_table()
#     io_config.enter_resistance_name(TABLE_NAME)
#     io_config.doubleclick_resistance_lookup_table()
#     io_config.verify_resistance_table_exists(TABLE_NAME)

#     # Right click on created table
#     io_config.rightclick_resistance_table(TABLE_NAME)

#     # Select "Add Resistance Values" via keyboard
#     io_config.select_add_resistance_values_from_context_menu()

#     io_config.enter_resistance_and_output_values(RESISTANCE, OUTPUT)
#     io_config.click_save_resistance_value()
#     io_config.cut_paste_resistance_value(row_index=2)
#     io_config.update_resistance_and_output_values(new_resistance=146, new_output=189)
#     io_config.click_save_resistance_value()
#     io_config.assert_resistance_and_output_values_in_grid(
#     row_index=3,
#     expected_resistance=146,
#     expected_output=189
#     )