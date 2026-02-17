# 🛡️ PhishGuard - AI-Powered Phishing URL Detector

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

PhishGuard is a real-time tool that analyzes URLs to detect phishing attempts. It combines a sleek web interface with a handy Chrome extension, using a rule-based scoring system to identify threats with high confidence.

## ✨ Key Features

*   **🚀 Real-time Analysis**: Instantly check any URL for phishing indicators.
*   **📊 Confidence Scoring**: Get a clear confidence score (0-100%) for every URL.
*   **⚠️ Detailed Reasons**: Understand *why* a URL is flagged (e.g., "Uses IP address", "Suspicious word: login").
*   **🦊 Chrome Extension**: Check URLs directly from your browser toolbar.
*   **🎨 Modern Web Interface**: User-friendly design with example buttons for quick testing.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **Frontend**: HTML, CSS, JavaScript
*   **Browser Extension**: Chrome Extensions API (Manifest V3)

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/frankline10281/phishguard.git
    cd phishguard
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install flask
    ```

4.  **Run the Flask application**
    ```bash
    python app.py
    ```

5.  **Open your browser** and go to `http://localhost:5000`

## 🦊 Loading the Chrome Extension

1.  Open Chrome and go to `chrome://extensions/`.
2.  Enable **"Developer mode"** (toggle in the top right).
3.  Click **"Load unpacked"**.
4.  Select the `extension` folder inside the `phishguard` project.
5.  The PhishGuard icon will appear in your toolbar.

## 🎯 How It Works

PhishGuard analyzes URLs based on multiple rules, assigning a score for each suspicious feature (e.g., IP address use, missing HTTPS, suspicious keywords). A total score over a threshold classifies the URL as **phishing**.

## 👨‍💻 Author

**Mustafa** - [GitHub Profile](https://github.com/mustafah10281)

## 📄 License

This project is licensed under the MIT License.