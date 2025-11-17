# tests/test_add_tag.py
import time
import pytest
from config import DEFAULT_TAG_NAME, DEFAULT_LOGICAL_ADDR
from pages.dialogs import NewProjectDialog
from pywinauto.keyboard import send_keys

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
    project_page.assert_row_count(expected=0)
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