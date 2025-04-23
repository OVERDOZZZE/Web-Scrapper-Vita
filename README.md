```markdown
# 🕷️ Multithreaded Image Scraper & Data Extractor

A fully modular, multithreaded, and production-ready web scraping system in Python. It is designed to **log in to a website**, **extract paginated image content**, **download images concurrently**, and **log all activity** while also **exporting structured product data to Excel**.

> ⚙️ Designed for extensibility, performance, and clarity.

---

## 📌 Features

✅ Authenticated scraping with CSRF token support  
✅ Thread-safe image downloading with locking and semaphores  
✅ Pagination-aware URL generation  
✅ Real-time console logging + log file creation  
✅ Config-based architecture using `.env` for credentials  
✅ Structured data export to Excel via `xlsxwriter`  
✅ CLI loading spinner for user feedback

---

## 📁 Project Structure

```
.
├── scrapper/                # Core scraping logic
│   ├── config.py            # Configuration loader
│   ├── session_manager.py   # Login and session management
│   ├── extractor.py         # Image URL extraction logic
│   ├── downloader.py        # Image downloader using threading
│   ├── controller.py        # Central runner with thread orchestration
│
├── utils/                   # Utility tools
│   ├── excel_writer.py      # Excel export handler
│   ├── spinner.py           # CLI spinner
│
├── logs.txt                 # Output log file
├── .env                     # Configuration secrets
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🔧 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/image-scraper.git
cd image-scraper
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure your `.env` file**

```env
USER_AGENT=your_user_agent
BASE_URL=https://example.com
LOGIN_URL=https://example.com/login
PAGE_URL=https://example.com/page=
LOGIN_USERNAME=your_username
PASSWORD=your_password
```

---

## 🚀 Running the App

```bash
python controller.py
```

This will:
- Log in to the website
- Extract image URLs from each page
- Download all images concurrently to `_images/`
- Export product data to `config/data.xlsx`
- Output logs to `logs.txt`

---

## 📊 Excel Output Example

Your extracted data is saved as an Excel file with the following structure:

| Name       | Code     | Image URL                 |
|------------|----------|---------------------------|
| Product 1  | #A32KLS  | https://example.com/1.jpg |
| Product 2  | #8FJK1D  | https://example.com/2.jpg |

---

## 🧠 Tech Stack

- `requests` + `BeautifulSoup4` — HTTP & HTML parsing
- `threading`, `Lock`, `Semaphore` — Concurrency
- `uuid`, `pathlib` — Unique filenames and platform-safe paths
- `xlsxwriter` — Excel export
- `decouple` — Secure configuration management

---

## 💡 Design Philosophy

This scraper is structured with **scalability and reusability** in mind. You can easily adapt it to:
- Extract other types of content (e.g., text, metadata)
- Integrate with databases or cloud storage
- Convert it to use `asyncio + aiohttp` for async scraping

---

## 📌 Future Enhancements

- 🔄 Replace `threading` with `asyncio` for I/O-bound performance
- 💾 Add support for SQLite/CSV exports
- 📸 Use `Pillow` for validating image formats after download
- 🛡️ Retry logic & CAPTCHA detection bypass

---

## 🧑‍💻 Author

**Nurdan**  
Data Science undergraduate @ University of Manitoba  
💼 Career goal: Machine Learning Engineer  
📫 Contact: [your email or GitHub profile]

---

