# tests/test_add_tag.py
import time
import pytest
from config.settings import DEFAULT_TAG_NAME, DEFAULT_LOGICAL_ADDR, Edited_LOGICAL_ADDR, Edited_TAG_NAME, Number_TAG_NAME
from src.pages import io_config
from src.pages.dialogs import NewProjectDialog
from pywinauto.keyboard import send_keys
from pathlib import Path
from pywinauto import Application
import pywinauto
import sys
import pyperclip
from src.utils.report_utils import update_excel_result
from tests.conftest import project_page
import pytest_check as check
from src.utils.assertion_utils import verify_equal
from src.utils.assertion_utils import verify_not_equal

@pytest.mark.UD_tags
def test_merge_add_user_defined_tag(main_page, project_page):
    PLC_MODEL = "XM-14-DT"
    EXPECTED_DATATYPES = ["Byte", "Word", "Double Word", "Int", "Real", "DINT"]
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    time.sleep(1)
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(tag_name=DEFAULT_TAG_NAME, logical_addr=DEFAULT_LOGICAL_ADDR)
    dialog.cancel()
    time.sleep(1)
    actual_rows = project_page.get_row_count()
    verify_equal(actual_rows, 0, "After click on cancel button row count")
    #checking all datatypes is get entered or not
    # for idx, datatype in enumerate(EXPECTED_DATATYPES):
    #     project_page.click_add_user_defined_tags()
    #     tag_name = f"TAG_{datatype.replace(' ', '_')}_{idx}"
    #     dialog.fill(
    #         tag_name=tag_name,
    #         logical_addr=DEFAULT_LOGICAL_ADDR
    #     )
    #     dialog.select_datatype(datatype)
    #     dialog.save()
    #     time.sleep(1)
    #     expected_count = idx + 1
    #     actual_rows = project_page.get_row_count()
    #     verify_equal(actual_rows, expected_count, f"After adding {datatype}, row count")
    #     actual_datatype = project_page.get_row_datatype(row=actual_rows - 1)
    #     verify_equal(actual_datatype, datatype, f"DataType mismatch for {datatype}")
    #     dialog.cancel()
    project_page.click_add_user_defined_tags()
    dialog = NewProjectDialog(project_page.win)
    dialog.fill(
        tag_name="FirstTag",
        logical_addr=DEFAULT_LOGICAL_ADDR
    )
    dialog.select_datatype("Bool")
    dialog.fillInitialValue(initial="1")
    dialog.clickRetentivecheckbox()
    dialog.clickshowLogicalAddresscheckbox()
    dialog.save()
    dialog.cancel()
    rownum=project_page.get_row_count()-1
    actualInitialValue=project_page.get_value_of_initialValueColumn(rownum)
    actualretentiveStatusValue=project_page.get_value_of_retentiveStatusColumn(rownum)
    actualretentiveAddressValue=project_page.get_value_of_retentiveAddressColumn(rownum)
    actualLogicalAddressValue=project_page.get_value_of_showLogicalAddressStatusColumn(rownum)
    verify_equal(actualInitialValue, 1, "Verify that user is able to add initial value as 0 or 1 for boolean datatype")
    verify_equal(actualretentiveStatusValue, True, "Verify that user is able to add retentive address for boolean datatype.")
    verify_equal(actualretentiveAddressValue, "X8:000", "Verify that user is able to see rententive address in retentive address column.")
    verify_equal(actualLogicalAddressValue, True, "Verify that user is able to add show logical address.")
    # test_data = [
    # ("1InvalidTag", "Verify that tag name cannot start with number."),
    # ("Invalid Tag", "Verify that tag name should not contain space."),
    # ("Invalid#Tag", "Verify that error should be shown for non-IEC characters.")
    # ]
    # EXPECTED_ERROR = "Please correct the errors before saving."
    # for tag_name, validation_msg in test_data:
    #     project_page.click_add_user_defined_tags()
    #     dialog = NewProjectDialog(project_page.win)
    #     dialog.fill(
    #         tag_name=tag_name,
    #         logical_addr=DEFAULT_LOGICAL_ADDR
    #     )
    #     dialog.select_datatype("Bool")
    #     dialog.save()
    #     actual_msg = dialog.getErrorMesage()
    #     verify_equal(
    #         actual_msg,
    #         EXPECTED_ERROR,
    #         validation_msg
    #     )
    #     send_keys("{ENTER}")
    #     dialog.cancel()
    rownum=project_page.get_row_count()-1
    updatedIntialValue="0"
    newtagName="SecondTag"
    project_page.select_lastRowofUserDefinedTags(rownum)
    dialog.filltagName(newtagName)
    dialog.fillInitialValue(initial=updatedIntialValue)
    dialog.clickRetentivecheckbox()
    dialog.clickshowLogicalAddresscheckbox()
    dialog.save()
    newupdatedInitialValue=project_page.get_value_of_initialValueColumn(rownum)
    newupdatedTagValue=project_page.get_corevalue_by_row_header(rownum)
    newretentiveAddressValue=project_page.get_value_of_retentiveAddressColumn(rownum)
    newLogicalAddressValue=project_page.get_value_of_showLogicalAddressStatusColumn(rownum)
    verify_equal(newupdatedInitialValue,"0", "Verify that user is able to edit initial value for boolean datatype")
    verify_equal(newupdatedTagValue,"SecondTag", "Verify that user is able to edit tag name for boolean datatype")
    verify_equal(newretentiveAddressValue, False, "Verify that user should not  able to see rententive address in retentive address column if user edits it as uncheck.")
    verify_equal(newLogicalAddressValue, False, "Verify that user able uncheck for show logical address if show logical address checkbox is already checked.")
  
    
    project_page.select_lastRowofUserDefinedTags(rownum)
    dialog.fillInitialValue(initial="2")
    dialog.save()
    Expected_Error="Please resolve the errors first"
    actual_msg= dialog.getErrorMesage2()
    verify_equal(actual_msg,Expected_Error,"Verify that error should be shown if user enters incorrect initial value.")
    project_page.click_add_user_defined_tags()
    dialog = NewProjectDialog(project_page.win)
    dialog.filllogicalAddress("P2:000")
    dialog.save()
    EXPECTED_ERROR="Please resolve the errors first"
    actual_msg= dialog.getErrorMesage2()
    send_keys("{ENTER}")
    dialog.cancel()
    verify_equal(actual_msg,EXPECTED_ERROR,"Verify that Logical address of boolean datatype starts with F2.")
    rownum=project_page.get_row_count()-1
    beforedeletecount=str(rownum)
    project_page.delete_UDT(rownum)
    time.sleep(5)
    afterrownum=project_page.get_row_count()-1
    afterdeletecount=str(afterrownum)
    verify_not_equal(beforedeletecount,afterdeletecount,"Verify that user is able to delete added tag.")

        

def test_edit_user_defined_tag_name(main_page, project_page):
    """Test editing tag name by double-clicking the grid row."""
    PLC_MODEL = "XM-14-DT"
    ORIGINAL_TAG_NAME = "OriginalTag"
    UPDATED_TAG_NAME = "UpdatedTag"
    DATATYPE = "Bool"
    
    # Step 1: Create initial tag
    main_page.click_new_project()
    main_page.select_model_and_confirm(PLC_MODEL)
    
    project_page.open_add_user_tag_dialog()
    dialog = NewProjectDialog(project_page.win)
    
   