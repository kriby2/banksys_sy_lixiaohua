"""测试 app 主入口基本可导入性."""

import importlib


def test_app_package_importable():
    import app  # noqa: F401


def test_main_module_importable():
    from app import main  # noqa: F401


def test_pages_importable():
    importlib.import_module("app.pages.01_data_analysis")
    importlib.import_module("app.pages.02_prediction")
