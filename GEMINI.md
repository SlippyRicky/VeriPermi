# Directory Overview: Driving License Evaluation

This directory contains preparation and reference materials for the French practical driving test ("Permis de conduire" - Category B).

## Structure

*   **`App/`**: Subdirectory containing the interactive Flashcard application.
    *   `app.py`: Streamlit application (Google Material Design version).
    *   `driving_questions.csv`: Database of 300 questions (100 groups).
    *   `requirements.txt`: Python dependencies.
    *   `grille-d-evaluation-du-permis-city-zen.jpg`: Evaluation grid.
*   **`banque-verifications-23_01_2023.pdf`**: Official PDF document with all questions.
*   **`Launch_Permis_App.command`**: Double-click this file to automatically start the app server and open it in Microsoft Edge.

## Usage

1.  **Direct Study**: Open the PDF to review questions manually.
2.  **Interactive Study**: Double-click `Launch_Permis_App.command`. This will:
    *   Start the Streamlit server if it's not already running.
    *   Open Microsoft Edge at `http://localhost:8501`.
3.  **Application Features**:
    *   Search by Group ID (last 2 digits of odometer).
    *   Filter by topic (Technical, Safety, First Aid).
    *   "I'm Feeling Lucky" button for randomized study.
