# tests/test_add_tag.py
import time
import pytest
from config import DEFAULT_TAG_NAME, DEFAULT_LOGICAL_ADDR, Edited_LOGICAL_ADDR, Edited_TAG_NAME, Number_TAG_NAME
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


def test_add_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(2) 
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(tag_name=DEFAULT_TAG_NAME, logical_addr=DEFAULT_LOGICAL_ADDR)
    dialog.save()
    time.sleep(1)
    project_page.assert_row_count(expected=1)
    dialog.cancel()

def test_add_byte_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    EXPECTED_DATATYPE = "Byte"  # must match exactly what grid shows

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)

    dialog.fill(
        tag_name=DEFAULT_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )

    dialog.select_datatype(EXPECTED_DATATYPE)  # from your earlier fix
    dialog.save()

    project_page.assert_row_count(expected=1)
    project_page.assert_row_datatype(expected=EXPECTED_DATATYPE, row=0)  # ← new

    dialog.cancel()


def test_add_word_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    EXPECTED_DATATYPE = "Word"  # must match exactly what grid shows

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)

    dialog.fill(
        tag_name=DEFAULT_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )

    dialog.select_datatype(EXPECTED_DATATYPE)  # from your earlier fix
    dialog.save()

    project_page.assert_row_count(expected=1)
    project_page.assert_row_datatype(expected=EXPECTED_DATATYPE, row=0)  # ← new

    dialog.cancel()


def test_add_double_word_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    EXPECTED_DATATYPE = "Double Word"  # must match exactly what grid shows

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)

    dialog.fill(
        tag_name=DEFAULT_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )

    dialog.select_datatype(EXPECTED_DATATYPE)  # from your earlier fix
    dialog.save()

    project_page.assert_row_count(expected=1)
    project_page.assert_row_datatype(expected=EXPECTED_DATATYPE, row=0)  # ← new

    dialog.cancel()

def test_add_int_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    EXPECTED_DATATYPE = "Int"  # must match exactly what grid shows

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)

    dialog.fill(
        tag_name=DEFAULT_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )

    dialog.select_datatype(EXPECTED_DATATYPE)  # from your earlier fix
    dialog.save()

    project_page.assert_row_count(expected=1)
    project_page.assert_row_datatype(expected=EXPECTED_DATATYPE, row=0)  # ← new

    dialog.cancel()


def test_add_real_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    EXPECTED_DATATYPE = "Real"  # must match exactly what grid shows

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)

    dialog.fill(
        tag_name=DEFAULT_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )

    dialog.select_datatype(EXPECTED_DATATYPE)  # from your earlier fix
    dialog.save()

    project_page.assert_row_count(expected=1)
    project_page.assert_row_datatype(expected=EXPECTED_DATATYPE, row=0)  # ← new

    dialog.cancel()


def test_add_dint_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    EXPECTED_DATATYPE = "DINT"  # must match exactly what grid shows

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)

    dialog.fill(
        tag_name=DEFAULT_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )

    dialog.select_datatype(EXPECTED_DATATYPE)  # from your earlier fix
    dialog.save()

    project_page.assert_row_count(expected=1)
    project_page.assert_row_datatype(expected=EXPECTED_DATATYPE, row=0)  # ← new

    dialog.cancel()

def test_accept_undescore_tagname(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(2) 
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(tag_name=Edited_TAG_NAME, logical_addr=Edited_LOGICAL_ADDR)
    dialog.save()
    time.sleep(1)
    project_page.assert_row_count(expected=1)
    dialog.cancel()

def test_tag_name_cannot_start_with_number(main_page, project_page):
    """Verify that tag name cannot start with number."""
    PLC_MODEL = "XBLD-17E"
    INVALID_TAG_NAME = "1InvalidTag"  # starts with number
    
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    
    dialog.fill(
        tag_name=INVALID_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )
    
    dialog.select_datatype("Byte")
    dialog.save()  
    dialog.assert_error_message_visible()
    project_page.assert_row_count(expected=0)

    dialog.cancel()


def test_tag_name_cannot_contain_space(main_page, project_page):
    """Verify that tag name should not contain space."""
    PLC_MODEL = "XBLD-17E"
    INVALID_TAG_NAME = "Invalid Tag"  # contains space
    
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    
    dialog.fill(
        tag_name=INVALID_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )
    
    dialog.select_datatype("Byte")
    dialog.save()  
    dialog.assert_error_message_visible()
    project_page.assert_row_count(expected=0)

    dialog.cancel()


def test_tag_name_cannot_contain_special_characters(main_page, project_page):
    """verify that error should be shown if user enters name apart of IEC standards validation."""
    PLC_MODEL = "XBLD-17E"
    INVALID_TAG_NAME = "Invalid#Tag"  # contains special character
    
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    
    dialog.fill(
        tag_name=INVALID_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )
    
    dialog.select_datatype("Byte")
    dialog.save()  
    dialog.assert_error_message_visible()
    project_page.assert_row_count(expected=0)

    dialog.cancel()

def test_edit_user_defined_tag_name(main_page, project_page):
    """Test editing tag name by double-clicking the grid row."""
    PLC_MODEL = "XBLD-17E"
    ORIGINAL_TAG_NAME = "OriginalTag"
    UPDATED_TAG_NAME = "UpdatedTag"
    DATATYPE = "Byte"
    
    # Step 1: Create initial tag
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    
    dialog.fill(
        tag_name=ORIGINAL_TAG_NAME,
        logical_addr=DEFAULT_LOGICAL_ADDR
    )
    dialog.select_datatype(DATATYPE)
    dialog.save()
    dialog.cancel()  # close dialog to return to main grid view
    dialog = NewProjectDialog(project_page.win)
    project_page.double_click_tag_row(row=0)
    dialog.fill_update(
        tag_name=UPDATED_TAG_NAME
     )
    