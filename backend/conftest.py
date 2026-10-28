# conftest.py — ensures backend/ is on sys.path so `from app.xxx import ...` works
# pytest.ini sets pythonpath = . which is the primary mechanism;
# this file is kept as a fallback marker for pytest rootdir detection.
