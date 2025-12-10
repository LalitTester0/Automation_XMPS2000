# tests/conftest.py
import pytest
import os
import pyautogui
from datetime import datetime
from pywinauto import Application
from config import EXE_PATH
from pages.main_window import MainWindow
from pages.project_window import ProjectWindow

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name.replace(" ", "_").replace("[", "_").replace("]", "")
        screenshot_path = os.path.abspath(os.path.join(screenshot_dir, f"FAIL_{test_name}_{timestamp}.png"))

        try:
            pyautogui.screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
            rep.screenshot_path = screenshot_path
        except Exception as e:
            print(f"Failed to take screenshot: {e}")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.insert(1, "<th>Screenshot</th>")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    if hasattr(report, "screenshot_path"):
        path = report.screenshot_path
        if os.path.exists(path):
            # Use absolute path → avoid relpath error
            rel_path = os.path.basename(path)  # Just filename
            # Copy screenshot to report folder
            report_dir = os.path.dirname(getattr(report, "nodeid", "")) or "."
            dest_path = os.path.join(report_dir, "screenshots", os.path.basename(path))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            import shutil
            shutil.copy2(path, dest_path)
            cells.insert(1, f'<td><img src="screenshots/{os.path.basename(path)}" width="600" style="cursor:pointer;" onclick="window.open(this.src)"/></td>')


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