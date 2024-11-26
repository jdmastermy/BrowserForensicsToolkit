
try:
    from modules.parsing import find_browser_profile_files, extract_history
    print("Modules imported successfully.")
except ImportError as e:
    print(f"Import failed: {e}")
