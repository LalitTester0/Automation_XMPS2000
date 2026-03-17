import win32com.client
from datetime import datetime

def update_excel_result(excel_path, tc_id, status, reason=""):
    import os
    if not os.path.exists(excel_path):
        print(f"ERROR: Excel file not found at {excel_path}")
        return

    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    workbook = None
    try:
        print(f"Attempting to open: {excel_path}")
        workbook = excel.Workbooks.Open(os.path.abspath(excel_path), ReadOnly=False)
        sheet = workbook.Sheets("Execution_Report")

        # ... rest of your loop ...

        workbook.Save()
        print("Excel updated and saved successfully")

    except Exception as e:
        print(f"COM Error details: {e}")
        print(f"HRESULT: {e.hresult if hasattr(e, 'hresult') else 'N/A'}")
        print("Common causes: File open in Excel, wrong path, or Office issue")

    finally:
        if workbook:
            workbook.Close(SaveChanges=True)
        excel.Quit()