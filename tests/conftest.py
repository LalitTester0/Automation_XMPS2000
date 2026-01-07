# tests/conftest.py
import pytest
import os
import pyautogui
from datetime import datetime
from pywinauto import Application
from config import EXE_PATH
from pages.main_window import MainWindow
from pages.project_window import ProjectWindow
from pages.io_config import IOConfig
import ctypes
import shutil
# ==================== SCREENSHOT ON FAILURE + SCENARIO ====================
 
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on failure and docstring as scenario."""
    outcome = yield
    rep = outcome.get_result()
 
    # Capture scenario from test docstring
    if item.function.__doc__:
        rep.scenario = item.function.__doc__.strip()
    else:
        rep.scenario = "No scenario description provided"
 
    # Screenshot only on failure in call phase
    if rep.when == "call" and rep.failed:
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
 
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = item.name.replace(" ", "_").replace("[", "_").replace("]", "_") \
                                .replace("/", "_").replace("\\", "_").replace(":", "_")
        screenshot_path = os.path.join(screenshot_dir, f"FAIL_{safe_name}_{timestamp}.png")
 
        try:
            pyautogui.screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
            rep.screenshot_path = os.path.abspath(screenshot_path)
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
 
 
# ==================== CUSTOM COLUMN ORDER ====================
 
def pytest_html_results_table_header(cells):
    """
    Default columns in pytest-html are:
    0: Result
    1: Test
    2: Duration
    3: Links
 
    We insert our custom columns in the desired positions:
    → After Test (index 2): Scenario
    → After Duration (index 4 after insert): Screenshot
    """
    # Insert Scenario after "Test" column (becomes position 2)
    cells.insert(2, "<th class='sortable'>Scenario</th>")
   
    # Insert Screenshot after "Duration" (which will be at position 4 after previous insert)
    cells.insert(4, "<th class='sortable'>Screenshot</th>")
 
 
def pytest_html_results_table_row(report, cells):
    """Insert values in the same order as headers."""
 
    # Insert Scenario after "Test" (position 2)
    scenario = getattr(report, "scenario", "No scenario")
    scenario_display = scenario.replace("\n", "<br>")  # Support multi-line
    cells.insert(2, f"<td class='col-scenario'>{scenario_display}</td>")
 
    # Insert Screenshot after "Duration" (position 4)
    if hasattr(report, "screenshot_path"):
        path = report.screenshot_path
        if path and os.path.exists(path):
            filename = os.path.basename(path)
            dest_dir = "assets/screenshots"
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            shutil.copy2(path, dest_path)
 
            img_html = f"""
            <img src="{dest_path}" alt="Failure screenshot"
                 width="600" style="max-width:100%; height:auto; cursor:zoom-in;"
                 onclick="window.open(this.src, '_blank')">
            """
            cells.insert(4, f"<td class='col-screenshot'>{img_html}</td>")
        else:
            cells.insert(4, "<td>No screenshot</td>")
    else:
        cells.insert(4, "<td>-</td>")
 
 
# ==================== STYLING & TITLE ====================
 
def pytest_html_report_title(report):
    report.title = "XMPS 2000 Automation Test Report"
 
 
def pytest_configure(config):
    """Add custom CSS for better readability."""
    if hasattr(config, "_html"):
        config._html.extra_css.append(
            "data:text/css,"
            ".col-scenario { white-space: pre-wrap; word-wrap: break-word; max-width: 500px; text-align: left; vertical-align: top; }"
            ".col-screenshot img { border: 1px solid #ddd; border-radius: 4px; }"
            "th.sortable { background-color: #f5f5f5; }"
        )
 
 
@pytest.fixture
def app():
    app = Application(backend="uia").start(EXE_PATH)
    yield app
    try:
        app.kill()
    except:
        pass
 
 
@pytest.fixture
def main_page(app):
    main_win = MainWindow(app)
    main_win.wait_for_visible()
    return main_win
 
 
@pytest.fixture
def project_page(app, main_page):
    main_page.wait_for_visible()
    project_win = ProjectWindow(app)
    project_win.wait_for_visible()
    return project_win

@pytest.fixture
def io_config(project_page):
    return IOConfig(project_page.win)