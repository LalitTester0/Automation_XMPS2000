# tests/test_add_tag.py
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
import pytest_check as check


@pytest.mark.UD_tags
@pytest.mark.dependency
def test_add_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XM-14-DT"
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

@pytest.mark.UD_tags
def test_Zero_add_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XM-14-DT"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(2)
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(tag_name=DEFAULT_TAG_NAME, logical_addr=DEFAULT_LOGICAL_ADDR)
    dialog.cancel()
    time.sleep(1)
    project_page.assert_row_count(expected=0)

@pytest.mark.UD_tags
def test_merge_add_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XM-14-DT"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(2)
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(tag_name=DEFAULT_TAG_NAME, logical_addr=DEFAULT_LOGICAL_ADDR)
    dialog.cancel()
    time.sleep(1)
    actual_rows = project_page.get_row_count()
    
    # Validation 1: Check row count is 0 after cancel
    if check.equal(actual_rows, 0, f"Validation 1: Row count should be 0, got {actual_rows}"):
        print(f"PASSED: Validation 1 - Row count is {actual_rows} as expected.")
    
    # Validation 2: Check window title contains PLC model
    title = project_page.win.window_text()
    if check.is_in(PLC_MODEL, title, f"Validation 2: {PLC_MODEL} not in title '{title}'"):
        print(f"PASSED: Validation 2 - Window title correctly contains {PLC_MODEL}.")
    
    # Validation 3: Demonstration of another check (e.g. if specific node exists)
    # We can add more as needed.



@pytest.mark.other
def test_get_system_tags(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.click_system_tags()
    count = project_page.get_system_tags_gridrow_count()
    project_page.get_multivalue_by_row_header(10)

    assert count > 0, "System tags grid is empty"

    print("Test passed: System tags grid is not empty")

@pytest.mark.modbus_tcp_client
def test_get_data(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(2)
    project_page.click_modbus_tcp_client()
    project_page.print_all_items_in_dropdown()
   
@pytest.mark.UD_tags
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
    #?print("Title Bar Text:", title)

@pytest.mark.UD_tags
def test_export_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(2) 
    project_page.click_export_user_defined_tags()

@pytest.mark.menu_bar
def test_click_compile_button(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL) 
    project_page.click_compile_button()
    time.sleep(2) 

@pytest.mark.menu_bar
def test_save_project(main_page, project_page):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()

    project_page.click_save_project_button()

    # Call immediately - no time.sleep()!
    project_page.print_save_success_message()

 
@pytest.mark.io_config
def test_click_digitalIP(main_page, project_page, io_config):
    main_page.click_new_project()
    main_page.select_model_and_confirm()
    time.sleep(2) 
    project_page.click_ioconfig()
    time.sleep(0.5) 
    io_config.click_digitalinput()
    time.sleep(0.5)
    io_config.assert_digital_input_count(0,"8")

    print("Test passed: Digital Input count verified successfully!")

@pytest.mark.io_config 
def test_click_digitalIP(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.click_ioconfig()
    time.sleep(0.5) 
    io_config.click_digitalinput()
    time.sleep(0.5)
    io_config.assert_digital_input_count(0,"8")

    print("Test passed: Digital Input count verified successfully!")
  
@pytest.mark.io_config
def test_click_digitalOP(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    time.sleep(1)
    project_page.click_ioconfig() 
    time.sleep(2)
    io_config.assert_digital_input_count(1, "6")

    print("Test passed: Digital count verified successfully!")

#Only for 14 models
@pytest.mark.io_config
def test_click_AnalogIPOnboard(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-14E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    time.sleep(1)
    project_page.click_ioconfig() 
    time.sleep(2)
    io_config.assert_digital_input_count(2, "0")

    print("Test passed: Analog IP count verified successfully!")

#Only for 14 models
@pytest.mark.io_config
def test_click_AnalogOPOnboard(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-14E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    time.sleep(1)
    project_page.click_ioconfig() 
    time.sleep(2)
    io_config.assert_digital_input_count(3, "0")

    print("Test passed: Analog OP count verified successfully!")

@pytest.mark.io_config
def test_click_UniversalIPOnboard(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    time.sleep(1)
    project_page.click_ioconfig() 
    time.sleep(2)
    io_config.assert_digital_input_count(4, "0")
    print("Test passed: Universal IP count verified successfully!")

@pytest.mark.io_config
def test_click_UniversalOPOnboard(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    time.sleep(1)
    project_page.click_ioconfig() 
    time.sleep(2)
    io_config.assert_digital_input_count(5, "0")

    print("Test passed: Universal OP count verified successfully!")

@pytest.mark.expansion
def test_XBLD_UI_UO_Expansion_model_Selection(main_page, project_page, io_config):
    MODEL_NAME = "XBLD-UI4-UO2"  
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(MODEL_NAME) 
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_module_added(MODEL_NAME)
    print(f"Test passed: Expansion module '{MODEL_NAME}' added and verified!")

@pytest.mark.expansion
def test_XBLD_AI_AO_Expansion_model_Selection(main_page, project_page, io_config):
    MODEL_NAME = "XBLD-AI2-AO2"  
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(MODEL_NAME)  # Dynamic!
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_module_added(MODEL_NAME)
    print(f"Test passed: Expansion module '{MODEL_NAME}' added and verified!")

@pytest.mark.expansion
def test_XBLD_DI16_Expansion_model_Selection(main_page, project_page, io_config):
    MODEL_NAME = "XBLD-DI16"  # ← Change this to test any model!
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(3)
    project_page.wait_for_visible()
    time.sleep(1)
    project_page.click_ioconfig()
    time.sleep(2)
    project_page.right_click_expansion_io()
    time.sleep(1)
    project_page.click_add_device_expansion()
    time.sleep(2)
    io_config.open_dropdown()
    time.sleep(1)
    io_config.select_model(MODEL_NAME)  # Dynamic!
    time.sleep(1)
    io_config.click_add()
    time.sleep(2)
    project_page.double_click_expansion()
    time.sleep(2)
    io_config.assert_module_added(MODEL_NAME)
    print(f"Test passed: Expansion module '{MODEL_NAME}' added and verified!")

# @pytest.mark.io_config
@pytest.mark.expansion
def test_XBLD_DO16_Expansion_model_Selection(main_page, project_page, io_config):
    MODEL_NAME = "XBLD-DO16"  # ← Change this to test any model!
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(3)

    project_page.wait_for_visible()
    time.sleep(1)

    project_page.click_ioconfig()
    time.sleep(2)

    project_page.right_click_expansion_io()
    time.sleep(1)

    project_page.click_add_device_expansion()
    time.sleep(2)

    io_config.open_dropdown()
    time.sleep(1)

    io_config.select_model(MODEL_NAME)  # Dynamic!
    time.sleep(1)

    io_config.click_add()
    time.sleep(2)

    project_page.double_click_expansion()
    time.sleep(2)

    io_config.assert_module_added(MODEL_NAME)

    print(f"Test passed: Expansion module '{MODEL_NAME}' added and verified!")


def test_XBLD_DIDO_Expansion_model_Selection(main_page, project_page, io_config):
    """Scenario: Add a new user-defined tag via the dialog and verify it appears in the project page."""
    expansion_model_name = "XBLD-DI8-DO66" 
    PLC_MODEL = "XBLD-17E"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(expansion_model_name)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_module_added(expansion_model_name)
    print(f"Test passed: Expansion module '{expansion_model_name}' added and verified!")

# @pytest.mark.other
# def test_add_5_expansion_modules(main_page, project_page, io_config):
#     PLC_MODEL = "XM-14-DT"
    
#     # Add 5 expansion modules (can be same or different)
#     expansion_models = [
#         "XM-DI-16",
#         "XM-DI-16",
#         "XM-DI-16",
#         "XM-DI-16",
#         "XM-DI-16"
#     ]

#     main_page.click_new_project()
#     main_page.select_model_and_confirm(PLC_MODEL)
#     time.sleep(6)

#     project_page.wait_for_visible()
#     time.sleep(2)

#     project_page.click_ioconfig()
#     time.sleep(4)

#     project_page.double_click_expansion()
#     time.sleep(2)

#     for i, model in enumerate(expansion_models, 1):
#         print(f"\n=== Adding expansion module {i}/5: {model} ===")

#         project_page.right_click_expansion_io()
#         time.sleep(2)

#         project_page.click_add_device_expansion()
#         time.sleep(10)  # Increased wait for dialog load

#         io_config.open_dropdown()
#         time.sleep(4)

#         io_config.select_model(model)
#         time.sleep(2)

#         io_config.click_add()
#         time.sleep(8)  # Increased wait for add + close

#         project_page.double_click_expansion()
#         time.sleep(2)

#         io_config.assert_module_added(model)

#         print(f"Successfully added module {i}/5: {model}")

#     print("\nAll 5 expansion modules added successfully!")
#     print("Test passed: 5 expansion modules added and verified!")
@pytest.mark.other
def test_Rename_XBLD_DI8_DO6(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DI8-DO6"
    NEW_TAG_NAME = "MyNewTagName"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    io_config.assert_tag_name_updated(NEW_TAG_NAME)
    print(f"Test passed: Expansion tag renamed to '{NEW_TAG_NAME}'")

@pytest.mark.other
def test_Rename_XBLD_UI4_UO2(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-UI4-UO2"
    NEW_TAG_NAME = "MyNewTagName"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    io_config.assert_tag_name_updated(NEW_TAG_NAME)
    print(f"Test passed: Expansion tag renamed to '{NEW_TAG_NAME}'")

@pytest.mark.other
def test_Rename_XBLD_AI2_AO2(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-AI2-AO2"
    NEW_TAG_NAME = "343MyNewTagName"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    io_config.assert_tag_name_updated(NEW_TAG_NAME)
    print(f"Test passed: Expansion tag renamed to '{NEW_TAG_NAME}'")

@pytest.mark.other
def test_Rename_XBLD_DI16(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DI16"
    NEW_TAG_NAME = "TestDI16Tag"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    io_config.assert_tag_name_updated(NEW_TAG_NAME)
    print(f"Test passed: Expansion tag renamed to '{NEW_TAG_NAME}'")

@pytest.mark.other
def test_Rename_XBLD_DO16(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DO16"
    NEW_TAG_NAME = "TestDO16Tag"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    io_config.assert_tag_name_updated(NEW_TAG_NAME)
    print(f"Test passed: Expansion tag renamed to '{NEW_TAG_NAME}'")

@pytest.mark.other
def test_is_retentive_DO(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DO16"

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    # Assert checkbox is enabled
    io_config.assert_is_retentive_enabled()

    # Enable retentive
    io_config.click_is_retentive()

    # Assert checkbox is checked
    io_config.assert_is_retentive_checked()

    # Save
    io_config.save_expansion()

    # Final assertion: retentive address is present in the column
    io_config.assert_retentive_address_present()

    print("Test passed: 'Is Retentive' enabled and retentive address assigned!")

@pytest.mark.other
def test_is_retentive_UI4_UO2(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-UI4-UO2"

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    # Assert checkbox is enabled
    io_config.assert_is_retentive_enabled()

    # Enable retentive
    io_config.click_is_retentive()

    # Assert checkbox is checked
    io_config.assert_is_retentive_checked()

    # Save
    io_config.save_expansion()

    # Final assertion: retentive address is present in the column
    io_config.assert_retentive_address_present()

    print("Test passed: 'Is Retentive' enabled and retentive address assigned!")

@pytest.mark.other
def test_real_AIAO(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-AI2-AO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_data_type("Real")

@pytest.mark.other
def test_word_AIAO(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_data_type("Word")

@pytest.mark.other
def test_word_AIAO(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_data_type("Word")

@pytest.mark.other
def test_real_UIUO(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-UI4-UO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_data_type("Real")

@pytest.mark.other
def test_bool_DI(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DI16"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_data_type("Bool")

@pytest.mark.other
def test_bool_DO(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DO16"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_data_type("Bool")

@pytest.mark.other
def test_bool_DODI(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DI8-DO6"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_data_type("Bool")

@pytest.mark.other
def test_AIAO_OR(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_or_tags_present(expected_count=4)
    print("Test passed: AIAO module shows 4 OR tags as expected!")

@pytest.mark.other1
def test_UIUO_OR(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_or_tags_present(expected_count=6)

    print("Test passed: UIUO module shows 6 OR tags as expected!")

@pytest.mark.other1
def test_XBLD_UIUO_OR(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-UI4-UO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_or_tags_present(expected_count=0)

    print("Test passed: UIUO module shows 0 OR tags as expected!")

@pytest.mark.other1
def test_XBLD_AIAO_OR(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-AI2-AO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_or_tags_present(expected_count=0)

    print("Test passed: UIUO module shows 0 OR tags as expected!")

@pytest.mark.other2
def test_AIAO_OL(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_ol_tags_present(expected_count=2)

    print("Test passed: AIAO module shows 2 OL tags as expected!")

@pytest.mark.other2
def test_UIUO_OL(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_ol_tags_present(expected_count=4)

    print("Test passed: UIUO module shows 4 OL tags as expected!")


@pytest.mark.expansion
def test_verify_16_di_expansion_in_grid(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DI16"
    
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()    
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_model_name_in_grid(EXPANSION_MODEL)

    print(f"Test passed: Expansion model '{EXPANSION_MODEL}' verified in grid!")

    io_config.assert_ol_tags_present(expected_count=4)

    print("Test passed: UIUO module shows 4 OL tags as expected!")

@pytest.mark.other2
def test_XBLD_UIUO_OL(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-UI4-UO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    # Add the expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    io_config.assert_ol_tags_present(expected_count=0)

    print("Test passed: UIUO module shows 0 OL tags as expected!")

@pytest.mark.other3
def test_XBLD_DI16_input_filter_checked_by_default(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DI16"  

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the DI expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()  # Opens the module settings

    # Assert: Input Filter is checked by default
    io_config.assert_input_filter_enabled_by_default()

    print("Test passed: 'Enable Input Filter' is checked by default!")


@pytest.mark.other3
def test_XBLD_DI8_DO6_input_filter_checked_by_default(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    EXPANSION_MODEL = "XBLD-DI8-DO6"  

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the DI expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()  # Opens the module settings

    # Assert: Input Filter is checked by default
    io_config.assert_input_filter_enabled_by_default()

    print("Test passed: 'Enable Input Filter' is checked by default!")

@pytest.mark.other3
def test_XM_DI8_DO6_input_filter_checked_by_default(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-DI8-DO6T"  

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the DI expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()  # Opens the module settings

    # Assert: Input Filter is checked by default
    io_config.assert_input_filter_enabled_by_default()

    print("Test passed: 'Enable Input Filter' is checked by default!")

@pytest.mark.other3
def test_XM_DI16_input_filter_checked_by_default(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-DI-16"  

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the DI expansion module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()  # Opens the module settings

    # Assert: Input Filter is checked by default
    io_config.assert_input_filter_enabled_by_default()

    print("Test passed: 'Enable Input Filter' is checked by default!")

@pytest.mark.expansion
def test_digital_input_filter_rejects_invalid_values(main_page, project_page, io_config):
    PLC_MODEL = "XBLD-17E"
    DI_MODEL = "XBLD-DI16"

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add DI module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(DI_MODEL)
    io_config.click_add()

    # Open the module form
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    # Enable Input Filter
    io_config.enable_input_filter()

    # Test invalid values
    invalid_values = ["0", "21", "30", "-5", "abc", ""]
    for invalid_val in invalid_values:
        print(f"\nTesting invalid value: '{invalid_val}'")

        # Enter invalid value and store it
        entered_value = io_config.enter_input_filter_value(invalid_val)

        # Save to apply changes
        io_config.save_expansion()

        # Re-open form to refresh view (if save closes it)
        project_page.doubleclick_open_expansion_form()

        # Get displayed value in DigitalFilter column
        displayed_value = io_config.get_displayed_digital_filter_value()

        # Key assertion: entered invalid value should NOT match displayed value
        assert entered_value != displayed_value, \
            f"Invalid value '{entered_value}' was accepted! Displayed: '{displayed_value}'"

        # Additional: displayed value should be valid (1–20)
        displayed_num = int(displayed_value)
        assert 1 <= displayed_num <= 20, \
            f"Displayed value '{displayed_value}' is outside valid range after invalid input"

        print(f"Assertion passed: Invalid '{entered_value}' rejected → displayed '{displayed_value}'")

    # Test one valid value to confirm acceptance
    valid_val = "15"
    entered_valid = io_config.enter_input_filter_value(valid_val)
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    displayed_valid = io_config.get_displayed_digital_filter_value()

    assert entered_valid == displayed_valid, \
        f"Valid value '{valid_val}' not accepted! Got '{displayed_valid}'"
    print(f"Valid value '{valid_val}' correctly accepted")

    print("Test passed: Digital Input Filter rejects invalid values and accepts only 1–20!")

@pytest.mark.other4
def test_XM_UIUI_Digital_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"

    # ← Change this line to test any mode
    selected_mode = "Digital"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other4
def test_XM_UIUI_0_10V_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"

    # ← Change this line to test any mode
    selected_mode = "0-10V"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other4
def test_XM_UIUI_0_5V_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"

    # ← Change this line to test any mode
    selected_mode = "0-5V"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other4
def test_XM_UIUI_0_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"

    # ← Change this line to test any mode
    selected_mode = "0-20mA"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other4
def test_XM_UIUI_4_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"

    # ← Change this line to test any mode
    selected_mode = "4-20mA"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other4
def test_XM_UIUI_Resistance_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"

    # ← Change this line to test any mode
    selected_mode = "Resistance"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other4
def test_XM_UIUI_PT100_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "PT100"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.assert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other
def test_XM_UIUI_PT1000_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "PT1000"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.assert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other
def test_XM_UIUI_10K_NTC_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "10K -NTC"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.assert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other
def test_XM_UIUI_20K_NTC_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "20K -NTC"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.assert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.failed
def test_XM_AIUI_0_10V_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"

    # ← Change this line to test any mode
    selected_mode = "0 to 10V"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.failed
def test_XM_AIUI_0_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"

    # ← Change this line to test any mode
    selected_mode = "0 to 20mA"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.failed
def test_XM_AIUI_4_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"

    # ← Change this line to test any mode
    selected_mode = "4 to 20mA"   # or "Analog", "PWM", "Counter", etc.

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add the module
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion form (only once)
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()

    print(f"\n--- Testing mode: '{selected_mode}' ---")

    # Select mode dynamically
    io_config.select_mode(selected_mode)

    # Save to apply changes
    io_config.save_expansion()

    io_config.assert_mode_matches_selected(selected_mode)

    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other5
def test_XM_digital_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "Digital"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_for_open_UO()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.for_UOassert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other5
def test_XM_UO_0_10V_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "0-10V"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_for_open_UO()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.for_UOassert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other5
def test_XM_UO_4_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "4-20mA"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_for_open_UO()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.for_UOassert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other5
def test_XM_UO_0_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"
    selected_mode = "0-20mA"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_for_open_UO()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.for_UOassert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other5
def test_XM_AO_0_10V_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"
    selected_mode = "0-10V"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_for_open_UO()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.for_AOassert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other5
def test_XM_AO_4_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"
    selected_mode = "4-20mA"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_for_open_UO()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.for_AOassert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other5
def test_XM_AO_0_20mA_mode(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"
    selected_mode = "0-20mA"   
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_for_open_UO()
    print(f"\n--- Testing mode: '{selected_mode}' ---")
    io_config.select_mode(selected_mode)
    io_config.save_expansion()
    io_config.for_AOassert_mode_matches_selected(selected_mode)
    print(f"Test passed: Mode '{selected_mode}' correctly reflected in Mode column!")

@pytest.mark.other
def test_OR_Reflection(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-AI2-AO-2"
    NEW_TAG_NAME = "kunal_test_tag"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()

@pytest.mark.other4
def test_tag_rename_updates_or_tag(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    AIAO_MODEL = "XM-AI2-AO-2"           
    ORIGINAL_TAG = "AnalogInput_AI0"   
    NEW_TAG_NAME = "MyCustomAI"          
    OR_TAG_ROW = 4                                         
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(AIAO_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_or_tag_prefix_matches_renamed(NEW_TAG_NAME, or_tag_row=OR_TAG_ROW)
    print(f"Test passed: Tag renamed to '{NEW_TAG_NAME}' and OR tag updated correctly!")


@pytest.mark.other4
def test_tag_rename_updates_ol_tag(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    AIAO_MODEL = "XM-AI2-AO-2"          
    ORIGINAL_TAG = "AnalogInput_AI0"    
    NEW_TAG_NAME = "MyCustomAI"         
    OL_TAG_ROW = 5                    
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(AIAO_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_ol_tag_prefix_matches_renamed(NEW_TAG_NAME, ol_tag_row=OL_TAG_ROW)

@pytest.mark.other
def test_UI_tag_rename_updates_or_tag(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    UIUO_MODEL = "XM-UI4-UO2"           
    ORIGINAL_TAG = "UniversalInput_UI0"   
    NEW_TAG_NAME = "Change"          
    OR_TAG_ROW = 6                                         
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(UIUO_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_or_tag_prefix_matches_renamed(NEW_TAG_NAME, or_tag_row=OR_TAG_ROW)
    print(f"Test passed: Tag renamed to '{NEW_TAG_NAME}' and OR tag updated correctly!")


@pytest.mark.other
def test_UO_tag_rename_updates_ol_tag(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    AIAO_MODEL = "XM-UI4-UO2"          
    ORIGINAL_TAG = "AnalogInput_AI0"    
    NEW_TAG_NAME = "MyCustomOL"         
    OL_TAG_ROW = 7                    
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(AIAO_MODEL)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    tag_box = io_config.expansion_tag_textbox
    tag_box.set_text(NEW_TAG_NAME)
    tag_box.type_keys("{ENTER}")
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_ol_tag_prefix_matches_renamed(NEW_TAG_NAME, ol_tag_row=OL_TAG_ROW)

@pytest.mark.other6
def test_check_DI_show_logical_address(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    MODEL_WITH_TAGS = "XM-DI-16"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(MODEL_WITH_TAGS)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.enable_show_logical_address()
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_show_logical_address_grid_checked()
    print("Test passed: 'Show Logical Address' enabled → grid cell is checked!")

@pytest.mark.other6
def test_check_D0_show_logical_address(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    MODEL_WITH_TAGS = "XM-DO-16"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(MODEL_WITH_TAGS)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.enable_show_logical_address()
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_show_logical_address_grid_checked()
    print("Test passed: 'Show Logical Address' enabled → grid cell is checked!")

@pytest.mark.other6
def test_check_AI_show_logical_address(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    MODEL_WITH_TAGS = "XM-AI2-AO-2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(MODEL_WITH_TAGS)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.enable_show_logical_address()
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_show_logical_address_grid_checked()
    print("Test passed: 'Show Logical Address' enabled → grid cell is checked!")

@pytest.mark.other6
def test_check_UI_show_logical_address(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    MODEL_WITH_TAGS = "XM-UI4-UO2"
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    project_page.wait_for_visible()
    project_page.click_ioconfig()
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(MODEL_WITH_TAGS)
    io_config.click_add()
    project_page.double_click_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.enable_show_logical_address()
    io_config.save_expansion()
    project_page.doubleclick_open_expansion_form()
    io_config.assert_show_logical_address_grid_checked()
    print("Test passed: 'Show Logical Address' enabled → grid cell is checked!")

@pytest.mark.expansion
def test_xm_di16_has_16_digital_inputs(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-DI-16"

    # This is your dynamic expected count
    expected_di_count = 16

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()

    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    project_page.double_click_expansion()
    project_page.win.wait("ready", timeout=10)

    # Optional model check
    added_model = io_config.get_expansion_model_name()
    assert EXPANSION_MODEL.upper() in added_model.upper(), \
        f"Wrong module! Expected '{EXPANSION_MODEL}', got '{added_model}'"

    # FIXED LINE – THIS IS WHAT WAS MISSING
    io_config.assert_digital_input_count(expected_di_count)

    print(f"Test passed: {EXPANSION_MODEL} has exactly {expected_di_count} digital inputs!")


@pytest.mark.other4
def test_print_all_tags_from_expansion(main_page, project_page, io_config):
    PLC_MODEL = "XM-14-DT"
    EXPANSION_MODEL = "XM-UI4-UO2"  # or any module with tags

    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)

    project_page.wait_for_visible()
    project_page.click_ioconfig()

    # Add module if needed
    project_page.right_click_expansion_io()
    project_page.click_add_device_expansion()
    io_config.open_dropdown()
    io_config.select_model(EXPANSION_MODEL)
    io_config.click_add()

    # Open the expansion grid/form
    project_page.double_click_expansion()

    # Give extra time for grid to fully render tags
    project_page.win.wait("ready", timeout=15)
    time.sleep(1)  # Small safety sleep — grids sometimes need it

    # Now print ALL tags
    io_config.print_all_tags_in_column(max_rows=32, timeout_per_row=12)

    print("Test passed: All tags from Tag column printed!")


# def test_Demo(main_page, project_page, io_config):
#     PLC_MODEL = "XM-14-DT"
#     EXPANSION_MODEL = "XM-DI-16"
#     main_page.click_new_project()
#     main_page.select_model_and_confirm(PLC_MODEL)
#     project_page.wait_for_visible()
#     project_page.click_ioconfig()
#     # Add the expansion module
#     project_page.right_click_expansion_io()
#     project_page.click_add_device_expansion()
#     io_config.open_dropdown()
#     io_config.select_model(EXPANSION_MODEL)
#     io_config.click_add()
#     project_page.double_click_expansion()
#     count = project_page.get_system_tags_gridrow_count()
#     project_page. get_multivalue_expansion(count)
#     project_page.click_modbus_tcp_client()
#     project_page.print_all_items_in_dropdown()
#     project_page.print_dropdown_items_that_match_expansion()

#     # assert count > 0, "System tags grid is empty"

#     # print("Test passed: System tags grid is not empty")

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