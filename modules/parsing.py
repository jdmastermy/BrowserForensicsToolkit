import sqlite3
import os
from modules.utils import convert_webkit_time, convert_firefox_time

TRANSITION_TYPES = {
    0: 'Link',
    1: 'Typed URL',
    2: 'Auto Bookmark',
    3: 'Auto Subframe',
    4: 'Manual Subframe',
    5: 'Generated',
    6: 'Start Page',
    7: 'Form Submit',
    8: 'Reload',
    9: 'Keyword',
    10: 'Keyword Generated'
}

DANGER_TYPE_MAP = {
    0: "Safe",
    1: "Dangerous File",
    2: "Dangerous URL",
    3: "Dangerous Content",
    4: "Uncommon Content",
    5: "User Validation Required",
    6: "Dangerous Host",
    7: "Potentially Unwanted Program (PUP)"
}

INTERRUPT_REASON_MAP = {
    0: "No Interrupt",
    1: "File Error",
    2: "Access Denied",
    3: "Disk Full",
    5: "Network Error",
    7: "Virus Detected",
    10: "Timeout",
    11: "Canceled",
    12: "Browser Shutdown"
}

def find_browser_profile_files(root_folder):
    profile_files = {
        "history": [],
        "cookies": [],
        "downloads": [],
        "cache": []
    }

    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            if file == "History":
                profile_files["history"].append(os.path.join(dirpath, file))
            elif file == "Cookies":
                profile_files["cookies"].append(os.path.join(dirpath, file))
            elif file == "places.sqlite":  # Firefox
                profile_files["history"].append(os.path.join(dirpath, file))

    return profile_files

def extract_history(browser, files, user_profile):
    history = []
    for db_file in files:
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            # Check tables in database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]

            if 'urls' in tables:
                # Chromium-based history
                query = '''
                SELECT urls.url, urls.title, urls.visit_count, urls.last_visit_time, visits.visit_time, visits.visit_duration, visits.from_visit, visits.transition
                FROM urls
                JOIN visits ON urls.id = visits.url
                '''
                cursor.execute(query)
                for row in cursor.fetchall():
                    url, title, visit_count, last_visit_time, visit_time, visit_duration, from_visit, transition = row
                    visit_time_utc = convert_webkit_time(visit_time)
                    visit_duration_sec = visit_duration / 1000000 if visit_duration else 0
                    visit_type = TRANSITION_TYPES.get(transition & 0xFF, 'Unknown')
                    history.append([visit_time_utc, url, title, visit_count, visit_type, visit_duration_sec, browser, user_profile, db_file])

            elif 'moz_places' in tables and 'moz_historyvisits' in tables:
                # Firefox history
                query = '''
                SELECT moz_places.url, moz_places.title, moz_places.visit_count, moz_historyvisits.visit_date
                FROM moz_places
                JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id
                '''
                cursor.execute(query)
                for row in cursor.fetchall():
                    url, title, visit_count, visit_time = row
                    visit_time_utc = convert_firefox_time(visit_time)
                    history.append([visit_time_utc, url, title, visit_count, None, None, browser, user_profile, db_file])
            conn.close()
        except sqlite3.Error as e:
            print(f"Error extracting history from {db_file}: {e}")
    return history

def extract_downloads(browser, files, user_profile):
    downloads = []
    for db_file in files:
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            query = '''
            SELECT target_path, start_time, total_bytes, received_bytes, danger_type, interrupt_reason, end_time, opened
            FROM downloads
            '''
            cursor.execute(query)
            for row in cursor.fetchall():
                target_path, start_time, total_bytes, received_bytes, danger_type, interrupt_reason, end_time, opened = row
                start_time_utc = convert_webkit_time(start_time)
                end_time_utc = convert_webkit_time(end_time) if end_time else None
                danger_description = DANGER_TYPE_MAP.get(danger_type, "Unknown")
                interrupt_description = INTERRUPT_REASON_MAP.get(interrupt_reason, "Unknown")
                opened_description = "Yes" if opened == 1 else "No"
                downloads.append([start_time_utc, end_time_utc, target_path, total_bytes, received_bytes, danger_description, interrupt_description, opened_description, browser, user_profile, db_file])
            conn.close()
        except sqlite3.Error as e:
            print(f"Error extracting downloads from {db_file}: {e}")
    return downloads

def extract_cookies(browser, files, user_profile):
    cookies = []
    for db_file in files:
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            query = '''
            SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, is_secure, is_httponly
            FROM cookies
            '''
            cursor.execute(query)
            for row in cursor.fetchall():
                host_key, name, value, creation_utc, last_access_utc, expires_utc, is_secure, is_httponly = row
                creation_time_utc = convert_webkit_time(creation_utc)
                last_access_time_utc = convert_webkit_time(last_access_utc)
                expiry_time_utc = convert_webkit_time(expires_utc)
                cookies.append([host_key, name, value, creation_time_utc, last_access_time_utc, expiry_time_utc, "Yes" if is_secure else "No", "Yes" if is_httponly else "No", browser, user_profile, db_file])
            conn.close()
        except sqlite3.Error as e:
            print(f"Error extracting cookies from {db_file}: {e}")
    return cookies
