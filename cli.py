import argparse
import os
from modules.parsing import find_browser_profile_files, extract_history, extract_downloads, extract_cookies
from modules.utils import write_to_csv
import json
from pandas import DataFrame


def detect_browser(profile_files):
    """
    Detect the browser type based on profile file paths or folder structure.
    """
    for path in profile_files.get("history", []) + profile_files.get("cookies", []):
        lower_path = path.lower()
        if "microsoft" in lower_path and "edge" in lower_path:
            return "Edge"
        elif "google" in lower_path and "chrome" in lower_path:
            return "Chrome"
        elif "mozilla" in lower_path and "firefox" in lower_path:
            return "Firefox"
        elif "opera" in lower_path:
            return "Opera"
        elif "bravesoftware" in lower_path and "brave" in lower_path:
            return "Brave"
    return "Unknown"


def output_data(data, headers, output_file, output_format):
    """
    Outputs data to the specified file format.
    """
    if output_format == "csv":
        write_to_csv(data, headers, output_file)
    elif output_format == "json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump([dict(zip(headers, row)) for row in data], f, ensure_ascii=False, indent=4)
    elif output_format == "html":
        df = DataFrame(data, columns=headers)
        df.to_html(output_file, index=False)
    elif output_format == "txt":
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\t".join(headers) + "\n")
            for row in data:
                f.write("\t".join(map(str, row)) + "\n")
    else:
        raise ValueError("Unsupported output format. Choose from 'csv', 'json', 'html', or 'txt'.")


def validate_folder(folder_path):
    """
    Validates if the folder path exists.
    """
    if not os.path.isdir(folder_path):
        raise argparse.ArgumentTypeError(f"The folder {folder_path} does not exist.")
    return folder_path


def main():
    parser = argparse.ArgumentParser(
        description="Browser Forensics Toolkit CLI",
        epilog="""
Example Usage:
    python cli.py --root /path/to/browser/profiles --output /path/to/output --format csv [--verbose]

This tool extracts browsing data (history, downloads, and cookies) from supported browsers.
Supported Output Formats: CSV, JSON, HTML, TXT.
        """
    )
    parser.add_argument(
        "--root", required=True, type=validate_folder,
        help="Root folder containing browser profiles (e.g., user data directories)."
    )
    parser.add_argument(
        "--output", required=True, type=validate_folder,
        help="Output folder where the parsed data will be saved."
    )
    parser.add_argument(
        "--format", choices=["csv", "json", "html", "txt"], default="csv",
        help="Output format for the data. Default is CSV."
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose mode for detailed logs."
    )

    args = parser.parse_args()

    root_folder = args.root
    output_folder = args.output
    output_format = args.format
    verbose = args.verbose

    if verbose:
        print(f"Starting Browser Forensics Toolkit...")
        print(f"Root Folder: {root_folder}")
        print(f"Output Folder: {output_folder}")
        print(f"Output Format: {output_format}")

    try:
        # profile files
        profile_files = find_browser_profile_files(root_folder)

        # Detect browser name
        browser_name = detect_browser(profile_files)
        if verbose:
            print(f"Detected Browser: {browser_name}")

        # History
        history_data = extract_history(browser_name, profile_files.get("history", []), "default_user")
        history_output = os.path.join(output_folder, f"history.{output_format}")
        output_data(
            history_data,
            ["Visit Time", "URL", "Title", "Visit Count", "Visit Type", "Duration", "Browser", "User Profile", "Source"],
            history_output,
            output_format
        )
        if verbose:
            print(f"History data saved to {history_output}")

        # Downloads
        downloads_data = extract_downloads(browser_name, profile_files.get("history", []), "default_user")
        downloads_output = os.path.join(output_folder, f"downloads.{output_format}")
        output_data(
            downloads_data,
            ["Start Time", "End Time", "File Path", "Total Bytes", "Received Bytes", "Danger Type", "Interrupt Reason", "Opened", "Browser", "User Profile", "Source"],
            downloads_output,
            output_format
        )
        if verbose:
            print(f"Downloads data saved to {downloads_output}")

        # Cookies
        cookies_data = extract_cookies(browser_name, profile_files.get("cookies", []), "default_user")
        cookies_output = os.path.join(output_folder, f"cookies.{output_format}")
        output_data(
            cookies_data,
            ["Host", "Name", "Value", "Creation Time", "Last Access Time", "Expiry Time", "Secure", "HTTP Only", "Browser", "User Profile", "Source"],
            cookies_output,
            output_format
        )
        if verbose:
            print(f"Cookies data saved to {cookies_output}")

        print(f"Browser Forensics Toolkit completed. Results saved in {output_folder}")

    except Exception as e:
        print(f"Error occurred during processing: {e}")


if __name__ == "__main__":
    main()
