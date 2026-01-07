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
from excel_report import update_excel_result

@pytest.mark.UD_tags
@pytest.mark.dependency
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

@pytest.mark.other
def test_get_system_tags(main_page, project_page):
    tc_id = "TC_SYS_TAG_001"
    excel_path = r"C:\Users\admin\Desktop\XMPS_Automation\Automation_XMPS2000\Execution_Report.xlsx"

    try:
        PLC_MODEL = "XBLD-17E"
        main_page.click_new_project()
        main_page.select_model_and_confirm(PLC_MODEL)
        time.sleep(2)

        project_page.click_system_tags()
        count = project_page.get_system_tags_gridrow_count()
        project_page.get_multivalue_by_row_header(10)

        assert count > 0, "System tags grid is empty"

        update_excel_result(excel_path, tc_id, "PASS")

    except Exception as e:
        update_excel_result(excel_path, tc_id, "FAIL", str(e))
        raise

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

