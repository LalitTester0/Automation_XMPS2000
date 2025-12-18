# tests/test_add_tag.py
import time
import pytest
from config import DEFAULT_TAG_NAME, DEFAULT_LOGICAL_ADDR
from pages.dialogs import NewProjectDialog
from pywinauto.keyboard import send_keys
from pathlib import Path
from pywinauto import Application
import pywinauto
import sys
import pyperclip


@pytest.mark.dependency
def test_add_user_defined_tag(main_page, project_page):
    main_page.click_new_project()
    main_page.select_model_and_confirm()
    time.sleep(2) 
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(tag_name=DEFAULT_TAG_NAME, logical_addr=DEFAULT_LOGICAL_ADDR)
    dialog.save()
    time.sleep(1)
    project_page.assert_row_count(expected=1)
    dialog.cancel()


def test_Zero_add_user_defined_tag(main_page, project_page):
    main_page.click_new_project()
    main_page.press_enter()
    main_page.select_model_and_confirm()
    time.sleep(2)
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(tag_name=DEFAULT_TAG_NAME, logical_addr=DEFAULT_LOGICAL_ADDR)
    dialog.cancel()
    time.sleep(1)
    project_page.assert_row_count(expected=0)

def test_get_system_tags(main_page, project_page):
    main_page.click_new_project()
    main_page.press_enter()
    main_page.select_model_and_confirm()
    time.sleep(2)
    project_page.click_system_tags()
    count=project_page.get_system_tags_gridrow_count()
    project_page.get_multivalue_by_row_header(10)


def test_get_data(main_page, project_page):
    main_page.click_new_project()
    main_page.press_enter()
    main_page.select_model_and_confirm()
    time.sleep(2)
    project_page.click_modbus_tcp_client()
    project_page.print_all_items_in_dropdown()
   

def test_open_project_file_via_dialog(main_page,project_page):
    raw_path = r"C:\Users\Admin\AppData\Roaming\MessungSystems\XMPS2000\XM Projects\XBLDProject02\XBLDProject02.xmprj"
    pyperclip.copy(raw_path)  
    main_page.click_open_project()
    time.sleep(1)
    send_keys('^v')
    time.sleep(0.3)
    send_keys('{ENTER}')
    time.sleep(10)
    title = project_page.win.window_text()
    print("Title Bar Text:", title)


def test_export_user_defined_tag(main_page, project_page):
    main_page.click_new_project()
    main_page.select_model_and_confirm()
    time.sleep(2) 
    project_page.click_export_user_defined_tags()
    