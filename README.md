# Kitap Pechat 📖 (Booklet Printing Utility)

**PyBooklet Printer** is a cross-platform (Linux & Windows) desktop application built with Python and Tkinter for preparing and printing PDF documents in booklet (saddle-stitch) format. It solves the common problem of manually sorting pages for double-sided printing.

This project was initially developed to bring the convenience of specialized booklet printing features, often found in Windows applications, to the Linux environment.

## ✨ Features

The application provides two core functions to handle your printing needs:

### 1. PDF Document Preparation (Automated)

* **Input:** Selects an original PDF file.
* **Range Selection:** Define a specific range of pages (e.g., page 10 to 50).
* **Automatic Padding:** Automatically checks if the total page count is divisible by 4. If not, the necessary number of blank pages are added (zero-padded) to ensure correct booklet order.
* **Output:** Generates **two separate PDF files**:
    * `filename_ALDI_TÁREP.pdf` (Pages for the front side of the sheets)
    * `filename_ARQA_TÁREP.pdf` (Pages for the back side of the sheets)
* *You simply print the first file, flip the stack, and print the second file.*

### 2. Manual Page Order Calculation (For Word/Excel/PPT)

* **Input:** Enter the total number of pages you wish to print.
* **Output:** Generates the precise, comma-separated sequence of page numbers required for booklet printing.
* **Separate Lists:** Provides **separate lists** for the "Front Side" and "Back Side" pages. (e.g., `8,1,6,3...` and `2,7,4,5...`).
* **Wrapper (Chunking):** Includes an option to split the long list of page numbers into smaller chunks (e.g., 10 sheets/40 pages at a time) to avoid exceeding printer buffer limits.

## 🚀 Installation & Usage

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)

### 1. Setup (Recommended for Development)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/OnlineAzamat/booklet-app.git
    cd booklet-app
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # venv\Scripts\activate   # For Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install pypdf
    ```

4.  **Run the application:**
    ```bash
    python booklet_app.py
    ```

### 2. Downloads (For End-Users)

Pre-compiled executable files for easy installation are available in the [Releases] section:

* **[Download for Linux with AppImage](https://t.me/yakubbaevdev_blog/20)**
* **[Download for Windows](https://t.me/yakubbaevdev_blog/19)**

## 📸 Screenshots

| PDF Document Preparation Tab | Manual Page Order Calculation Tab |
| :---: | :---: |
| **<img width="660" height="497" alt="Screenshot from 2025-10-21 18-25-16" src="https://github.com/user-attachments/assets/3fb7b902-972e-45c6-ba6a-fee4ad630ee6" />** | **<img width="660" height="497" alt="Screenshot from 2025-10-21 18-25-35" src="https://github.com/user-attachments/assets/a7d70d55-3195-42a0-8846-1b85ba3c6a73" />** |

## 💡 Contribution & Feedback

This project is my first attempt at building a cross-platform GUI application using Python/Tkinter. I welcome feedback, suggestions, and contributions from the community, especially regarding code structure, efficiency (for large PDFs), and UI/UX improvements.

Feel free to open an issue or submit a pull request!

## 📜 License

This project is licensed under the MIT License.

---
*Developed by: [Azamat Yakubbaev / <a href="https://github.com/OnlineAzamat">OnlineAzamat</a>]*
