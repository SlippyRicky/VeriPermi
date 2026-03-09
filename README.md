# 🚗 Permis de Conduire - Flashcard App

This is a comprehensive, interactive Flashcard Application designed to help you prepare for the oral examination of the French driving license (**Permis B**). It includes all **100 groups of questions** covering Technical Verifications, Road Safety, and First Aid, complete with the expected answers and highly specific, contextual tips.

## ✨ Features
*   **Complete Official Database**: All 300 questions extracted directly from the official examiner's bank.
*   **Smart Search**: Filter questions by the **Group ID** (the last 2 digits of your vehicle's odometer), simulating the exact condition of your real exam.
*   **"Contexte & Astuce"**: Custom-generated context notes for each question to help you understand *why* the question is asked, not just what the answer is.
*   **Dark Mode Material Design**: A clean, professional, and eye-friendly interface.
*   **Cross-Platform Auto-Setup**: Ready to run out of the box on Windows, macOS, and Linux.

---

## 🛠️ Installation & Usage

This project is designed to be as "plug-and-play" as possible. You do not need to manually install dependencies or set up environments; the provided launcher scripts handle everything automatically.

### Prerequisites
*   You must have **Python 3.8+** installed on your system.
    *   *Windows*: Download from [python.org](https://www.python.org/downloads/) (Make sure to check "Add Python to PATH" during installation).
    *   *macOS/Linux*: Usually pre-installed, or can be installed via `brew install python` / `apt install python3`.

### 🍎 For macOS & 🐧 Linux Users
1.  Open your Terminal.
2.  Navigate to this project folder.
3.  Run the launcher script:
    ```bash
    ./run_app.sh
    ```
*Note: The script will automatically create a secure virtual environment, install dependencies, and open the app in your default web browser.*

### 🪟 For Windows Users
1.  Open this project folder in File Explorer.
2.  **Double-click** the `run_app.bat` file.
*Note: A command prompt will appear to show the setup progress, and then your browser will automatically open the application.*

---

## 📂 Project Structure

*   `run_app.sh` / `run_app.bat`: Cross-platform launcher scripts.
*   `requirements.txt`: Python dependency list (Streamlit, Pandas).
*   **`App/`**:
    *   `app.py`: The main Streamlit web application.
    *   `driving_questions.csv`: The complete, 300-question database.
*   **`banque-verifications-23_01_2023.pdf`**: The official Ministry of Interior document source.

---
*Created to guarantee you secure those 3 essential points on your practical exam! Bonne chance!* 🚦
