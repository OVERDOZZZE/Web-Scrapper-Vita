# 🕸️ Multithreaded Web Image Scraper with Excel Export

A modular, thread-safe Python scraper for extracting and downloading images across multiple paginated web pages. Features include session-based login with CSRF protection, multithreaded image downloading with progress logging, and structured Excel export for metadata. Designed with extensibility and clarity in mind.

---

## 📂 Project Structure

```
.
├── config.py             # Loads configuration from .env
├── main.py               # Entry point for scraping and export
├── scrapper.py           # Core scraping logic and controllers
├── tests.py              # Contains test versions of some project sturctures
├── utils.py              # Includes ExcelWriter and Spinner utilities
├── .gitignore            # Git ignored files and folders
├── README.md             # This file

└── config/
    ├── .env.sample       # Environment variable template
    ├── data.xlsx         # Exported Excel data
    ├── requirements.txt  # Python dependencies
```

---

## 🚀 Features

- **🔐 Authenticated Session Handling**  
  Automatically logs into the website using CSRF-secured forms.

- **🧵 Multithreaded Download Engine**  
  Efficiently downloads images concurrently using `threading` and `Semaphore`.

- **📄 Excel Export**  
  Exports structured image metadata into a formatted `.xlsx` file using `xlsxwriter`.

- **📦 Modular & Extensible Architecture**  
  Clear separation of responsibilities via `SessionManager`, `ImageExtractor`, `ImageDownloader`, and `ScraperController`.

- **🪵 Robust Logging**  
  Dual-output logger with both file and console logging (`CustomLogger`).

- **⏳ Terminal Spinner**  
  CLI spinner feedback during long-running tasks (`Spinner` utility).

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/overdozzze/web-scrapper-vita.git
cd Web-Scrapper-Vita
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r config/requirements.txt
```

### 4. Configure Environment Variables

Copy the sample config:

```bash
cp config/.env.sample .env
```

Then, fill in your credentials and URLs in `.env`:

```env
USER_AGENT=your-user-agent
PAGE_URL=https://example.com/page=
LOGIN_URL=https://example.com/login
BASE_URL=https://example.com
LOGIN_USERNAME=your_username
PASSWORD=your_password

* Original web-site is now shown, contact me directly get the link
```

---

## 🧪 Running the Scraper

### From Command Line:

```bash
python main.py
```

This will:

1. Authenticate and retrieve the total number of paginated pages.
2. Start multiple threads (configurable) to download images.
3. Log all activity into `logs.txt`.
4. Save image metadata into `config/data.xlsx`.

---

## 🔍 Example Log Output

```
2025-04-23 01:45:23 - Thread-1 - INFO - Started downloading from https://example.com/page=1
2025-04-23 01:45:24 - Thread-1 - INFO - Downloaded https://example.com/images/img1.jpg
2025-04-23 01:45:25 - Thread-1 - INFO - Finished downloading from https://example.com/page=1
```

---

## 🧰 Extending Functionality

- ➕ Add image metadata scraping (e.g., `alt`, dimensions).
- ➕ Implement retry logic on download failures.
- 🔄 Switch to `asyncio` + `aiohttp` for IO-bound performance boost.
- 🧪 Write tests in `tests.py` using `unittest` or `pytest`.

---

## 🧹 Cleanup & Maintenance

Make sure to `.gitignore` any sensitive or generated files. This project already ignores:

```bash
venv/
.env
__pycache__/
*.log
config/data.xlsx
```

---

## 👨‍💻 Author

**Nurdan** – Data Science student and aspiring Machine Learning Engineer  
📍 Winnipeg, Canada  
🧠 Python | Web Scraping | Multithreading | Data Analytics  
