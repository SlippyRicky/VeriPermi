# 🚗 VeriPermi - Application de Flashcards pour le Permis B

**Version 1.1.0 - Release Officielle**

> **TL;DR (Pour les Recruteurs / Développeurs)**
> VeriPermi est une application Python full-stack construite avec Streamlit et Pandas. Elle démontre la gestion de cache (`@st.cache_data`), le state management interactif (`st.session_state`), le filtrage dynamique de données (CSV), et l'intégration de CSS Material Design via des composants HTML customs. L'architecture est conçue pour être "Plug-and-Play" sur tous les OS via des scripts d'auto-amorçage.
VeriPermi est une application interactive complète conçue pour vous aider à préparer l'épreuve orale de l'examen pratique du permis de conduire français (**Permis B**). Elle regroupe l'intégralité des **100 groupes de questions officielle**, couvrant les vérifications techniques, la sécurité routière et les premiers secours.

## ✨ Caractéristiques
*   **Base de Données Officielle Complète** : Les 300 questions (100 séries de 3) extraites directement de la banque d'examen du Ministère de l'Intérieur.
*   **Auto-Évaluation** : Marquez vos réponses comme correctes ou fausses pour suivre votre progression.
*   **Mode Liste Colorée** : Visualisez l'ensemble des questions avec un code couleur par catégorie.
*   **Recherche Intelligente** : Filtrez les questions par **ID de Groupe** (correspondant aux 2 derniers chiffres de votre compteur kilométrique).
*   **Contexte & Astuces** : Chaque question est accompagnée d'un encadré pédagogique pour comprendre l'enjeu de la question.
*   **Design Material Dark** : Une interface moderne, épurée et optimisée pour l'étude.
*   **Fenêtre Dédiée** : Lancement automatique dans une fenêtre épurée (style application native).
*   **Auto-Installation Multi-Plateforme** : Prêt à l'emploi sur Windows, macOS et Linux.

---

## 🛠️ Installation et Utilisation

Ce projet est conçu pour être "Plug-and-Play". Les scripts de lancement s'occupent de tout : création de l'environnement virtuel, installation des dépendances et lancement de l'application.

### Prérequis
*   Avoir **Python 3.8+** installé sur votre système.
    *   *Windows* : Téléchargez sur [python.org](https://www.python.org/downloads/) (Cochez bien "Add Python to PATH" lors de l'installation).
    *   *macOS/Linux* : Généralement pré-installé, ou via `brew install python`.

### 🍎 Pour macOS & 🐧 Linux
1.  Ouvrez votre Terminal (ou le Finder sur macOS).
2.  Accédez au dossier du projet.
3.  Lancez le script :
    *   **macOS** : Double-cliquez directement sur le fichier `Launch_Permis_App.command` depuis le Finder.
    *   **Linux** : Exécutez `./run_app.sh` dans votre terminal.
*Note : Le script ouvrira automatiquement l'application dans votre navigateur par défaut.*

### 🪟 Pour Windows
1.  Ouvrez le dossier du projet dans l'Explorateur de fichiers.
2.  **Double-cliquez** sur le fichier `run_app.bat`.
*Note : Une fenêtre de commande s'ouvrira pour configurer l'application, puis votre navigateur lancera l'interface.*

---

## 📂 Structure du Projet

*   `run_app.sh` / `run_app.bat` : Scripts de lancement automatique.
*   `requirements.txt` : Liste des dépendances (Streamlit, Pandas).
*   **`App/`** :
    *   `app.py` : Code source de l'application web.
    *   `driving_questions.csv` : Base de données complète des 300 questions.
    *   `grille-d-evaluation-du-permis-city-zen.jpg` : Grille officielle d'évaluation d'un inspecteur type.
*   **`banque-verifications-23_01_2023.pdf`** : Document officiel source du Ministère.

---
*Développé pour vous garantir les 3 points faciles de l'examen oral. Bonne chance !* 🚦
