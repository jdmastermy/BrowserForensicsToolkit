# BrowserForensicsToolkit - Beta 0.1

BrowserForensicsToolkit is a powerful Python-based tool designed for forensic analysis of web browser artifacts. It supports extracting history, downloads, and cookies from various browsers, making it a versatile choice for digital forensics, data analysis, and investigative purposes.



## 📋 Project Summary

Web browsers store a wealth of information that can be invaluable in investigations, including browsing history, downloaded files, and cookies. **BrowserForensicsToolkit** simplifies the process of extracting and analyzing this data from major browsers like:

- Microsoft Edge
- Google Chrome
- Mozilla Firefox
- Opera
- Brave

Whether you’re a digital forensic expert, a researcher, or simply curious about your browser data, this tool offers the flexibility and power you need.

------

## ✨ Features

- CLI Mode:
  - Extract browsing history, downloads, and cookies from browser profile folders.
  - Support for multiple browsers: Edge, Chrome, Firefox, Opera, and Brave.
  - Flexible output formats: CSV, JSON, HTML, or TXT.
  - Automatic detection of the browser type based on artifact paths.
- GUI Mode:
  - User-friendly interface with tabs for history, downloads, and cookies.
  - Searchable and sortable tables for easy analysis.
  - Export functionality to save data in various formats.
- Lightweight and easy to use with minimal dependencies.

------

## 📥 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

Clone this repository and install the required dependencies:

```
bashCopy codegit clone https://github.com/jdmastermy/BrowserForensicsToolkit.git
cd BrowserForensicsToolkit
pip install -r requirements.txt
```

------

## 🚀 How to Run

### Command-Line Interface (CLI)

Use the following command to run the CLI:

```
python cli.py --root <path_to_browser_profile> --output <output_directory> --format <output_format>
```

### Graphical User Interface (GUI)

To run the GUI version:

```
python main.py
```

The GUI provides a more intuitive way to interact with the toolkit. Features include:

- Selecting browser profiles and output folders via file dialogs.
- Viewing extracted data in searchable, sortable tables.
- Exporting results to CSV, JSON, HTML, or TXT formats.

------

### CLI Parameters

| Parameter   | Description                                                  | Example                                        |
| ----------- | ------------------------------------------------------------ | ---------------------------------------------- |
| `--root`    | Path to the browser profile folder containing user data.     | `C:\Users\<User>\AppData\Local\Microsoft\Edge` |
| `--output`  | Directory where the parsed data will be saved.               | `C:\Output`                                    |
| `--format`  | Output format: `csv`, `json`, `html`, or `txt`. Default is `csv`. | `csv`                                          |
| `--verbose` | (Optional) Enable verbose mode for detailed logs.            | N/A                                            |

------

## 📸 Screenshots

### 1. **Main Interface (GUI Mode)**

<img src="screenshots\gui.PNG" style="zoom:67%;" />



### 2. **History Tab**

<img src="screenshots\history.PNG" style="zoom:67%;" />



### 3. **Downloads Tab**

<img src="screenshots\download.PNG" style="zoom: 67%;" />

### 4. **Cookies Tab**

<img src="screenshots\cookies.PNG" style="zoom:67%;" />

### 5. **CLI Example Output**

<img src="screenshots\cli.PNG" style="zoom:67%;" />

## 🖥 Supported Browsers

- **Microsoft Edge**: `AppData\Local\Microsoft\Edge`
- **Google Chrome**: `AppData\Local\Google\Chrome`
- **Mozilla Firefox**: `AppData\Roaming\Mozilla\Firefox`
- **Opera**: `AppData\Roaming\Opera Software\Opera Stable`
- **Brave**: `AppData\Local\BraveSoftware\Brave-Browser`

------

## 📂 Output Details

The toolkit generates output files in the specified format containing the following data:

### 1. **Browsing History**

| Column       | Description                          |
| ------------ | ------------------------------------ |
| Visit Time   | Timestamp of the visit.              |
| URL          | Visited URL.                         |
| Title        | Page title.                          |
| Visit Count  | Number of times the URL was visited. |
| Visit Type   | Type of visit (e.g., Link, Reload).  |
| Duration     | Duration of the visit in seconds.    |
| Browser      | Detected browser name.               |
| User Profile | Browser user profile name.           |
| Source       | File path of the artifact.           |

### 2. **Downloads**

| Column           | Description                                                 |
| ---------------- | ----------------------------------------------------------- |
| Start Time       | Download start timestamp.                                   |
| End Time         | Download end timestamp.                                     |
| File Path        | Path of the downloaded file.                                |
| Total Bytes      | Total size of the file.                                     |
| Received Bytes   | Bytes downloaded.                                           |
| Danger Type      | Indicates potential dangers (e.g., Safe, Uncommon Content). |
| Interrupt Reason | Reason for download interruption.                           |
| Opened           | Whether the file was opened post-download.                  |
| Browser          | Detected browser name.                                      |
| User Profile     | Browser user profile name.                                  |
| Source           | File path of the artifact.                                  |

### 3. **Cookies**

| Column           | Description                      |
| ---------------- | -------------------------------- |
| Host             | Domain of the cookie.            |
| Name             | Name of the cookie.              |
| Value            | Value of the cookie.             |
| Creation Time    | Cookie creation timestamp.       |
| Last Access Time | Last access timestamp.           |
| Expiry Time      | Expiration timestamp.            |
| Secure           | Whether the cookie is secure.    |
| HTTP Only        | Whether the cookie is HTTP-only. |
| Browser          | Detected browser name.           |
| User Profile     | Browser user profile name.       |
| Source           | File path of the artifact.       |

------

## 💡 Use Cases

1. **Digital Forensics**:
   - Analyze browsing behavior.
   - Investigate downloaded files, malwares and cookie usage.
2. **Parental Monitoring**:
   - Monitor web activity of children.
3. **Security Audits**:
   - Identify potentially dangerous downloads or sites visited.
4. **Data Backup**:
   - Export browser data for backup or migration.

------

## 🔧 Development

### Running Tests

To verify the toolkit, use the test script:

```
python test_imports.py
```

------

## 🛠 Troubleshooting

If you encounter issues:

1. Ensure you have the correct `--root` path to the browser profile folder.
2. Check the browser is installed and the user profile exists.
3. Run with the `--verbose` flag for more detailed logs.

------

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

------

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed explanations.

