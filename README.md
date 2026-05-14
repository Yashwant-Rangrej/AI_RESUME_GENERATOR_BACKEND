# 📄 AI Resume Builder - Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A robust, FastAPI-powered backend engine that transforms user conversations into professional, recruiter-ready resumes. This service handles multi-step session management, rule-based data processing, and dynamic PDF generation.

---

## ✨ Key Features

- **🧠 Intelligent Chatbot Engine**: A structured, session-based flow that guides users through the resume-building process.
- **📄 High-Fidelity PDF Generation**: Precision-engineered PDF templates using `ReportLab` for professional formatting.
- **🛠️ Automated Data Enhancement**: Built-in services that refine project descriptions and synthesize professional summaries.
- **⚡ RESTful API Architecture**: Highly optimized endpoints for seamless integration with frontend frameworks like Next.js.
- **🔒 Secure Session Management**: Robust handling of concurrent user sessions and temporary data storage.
- **🌍 CORS Ready**: Pre-configured for cross-origin requests, ready for modern web deployments.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **FastAPI** | High-performance web framework for building APIs. |
| **ReportLab** | Industry-standard library for programmatic PDF creation. |
| **Pydantic** | Strict data validation and settings management. |
| **Uvicorn** | Lightning-fast ASGI server implementation. |
| **Python-Dotenv** | Secure environment variable management. |

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9 or higher
- `pip` or `poetry`

### 2. Installation & Setup
```bash
# Clone the repository
git clone https://github.com/Yashwant-Rangrej/AI_RESUME_GENERATOR_BACKEND.git
cd AI_RESUME_GENERATOR_BACKEND

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Unix/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000
```

### 4. Running the Server
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. You can access the interactive Swagger documentation at `http://localhost:8000/docs`.

---

## 📡 API Reference

### Resume Session Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/resume/start` | Initializes a new resume session. |
| `GET` | `/resume/question` | Retrieves the current active question for a session. |
| `POST` | `/resume/answer` | Submits an answer and moves to the next step. |
| `POST` | `/resume/generate` | Processes collected data and triggers PDF generation. |
| `GET` | `/resume/download` | Serves the generated PDF file. |
| `POST` | `/resume/direct-generate` | Generates a PDF instantly from raw JSON input. |

---

## 📂 Project Structure

```text
app/
├── chatbot/       # Core engine logic & session flow management
├── models/        # Pydantic schemas for request/response validation
├── pdf/           # ReportLab templates & layout definitions
├── routes/        # API endpoint definitions (FastAPI Routers)
├── services/      # Logic for summary generation & data enhancement
├── utils/         # Reusable utility functions and helpers
└── main.py        # Application entry point & configuration
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the PDF templates, chatbot logic, or API efficiency:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Yashwant Rangrej**
- GitHub: [@Yashwant-Rangrej](https://github.com/Yashwant-Rangrej)
- LinkedIn: [Yashwant Rangrej](https://www.linkedin.com/in/yashwant-rangrej-0856993a8/)

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.