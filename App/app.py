import streamlit as st
import pandas as pd
import random

# Material Design Dark Theme Colors
PRIMARY_BLUE = "#8AB4F8"
SURFACE_DARK = "#202124"
CARD_DARK = "#292A2D"
TEXT_PRIMARY = "#E8EAED"
TEXT_SECONDARY = "#9AA0A6"
DIVIDER = "#3C4043"

# Set page config
st.set_page_config(
    page_title="Permis de Conduire - Flashcards",
    page_icon="🚗",
    layout="centered"
)

# Comprehensive CSS for a modern Dark Mode Material Design look
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* Main Background */
.stApp {{
    background-color: {SURFACE_DARK} !important;
    font-family: 'Roboto', sans-serif;
}}

/* Card Style */
.card {{
    background: {CARD_DARK};
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    padding: 40px;
    margin-top: 2rem;
    margin-bottom: 2rem;
    min-height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border: 1px solid {DIVIDER};
}}

.category-tag {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
    color: {PRIMARY_BLUE};
    margin-bottom: 16px;
}}

.question {{
    font-size: 1.8rem;
    font-weight: 400;
    color: {TEXT_PRIMARY};
    line-height: 1.5;
    margin-bottom: 24px;
}}

.divider {{
    height: 1px;
    background-color: {DIVIDER};
    margin: 24px 0;
}}

.answer-container {{
    background-color: rgba(138, 180, 248, 0.05);
    border-left: 4px solid {PRIMARY_BLUE};
    padding: 24px;
    border-radius: 4px;
    margin-top: 15px;
}}

.answer {{
    font-size: 1.3rem;
    color: {TEXT_PRIMARY};
    line-height: 1.6;
}}

.hidden-answer {{
    font-style: italic;
    color: {TEXT_SECONDARY};
    font-size: 1rem;
    text-align: center;
    width: 100%;
    margin-top: 20px;
}}

/* Streamlit Component Overrides */
.stButton > button {{
    background-color: transparent !important;
    color: {PRIMARY_BLUE} !important;
    border-radius: 24px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important;
    border: 1px solid {DIVIDER} !important;
    transition: all 0.2s !important;
}}

.stButton > button:hover {{
    background-color: rgba(138, 180, 248, 0.08) !important;
    border-color: {PRIMARY_BLUE} !important;
}}

.stProgress > div > div > div > div {{
    background-color: {PRIMARY_BLUE};
}}
/* Sidebar and Inputs */
[data-testid="stSidebar"] {{
    background-color: {CARD_DARK} !important;
}}

/* Unified Input Styling (Pill shape) */
/* Target the container and all internal wrappers used by Streamlit/BaseWeb */
.stTextInput div[data-baseweb="input"],
.stTextInput div[data-baseweb="input"] > div,
.stTextInput input {{
    border-radius: 28px !important;
    border: none !important;
}}

/* Apply border and background only to the outermost wrapper */
.stTextInput div[data-baseweb="input"] {{
    background-color: {SURFACE_DARK} !important;
    border: 1px solid {DIVIDER} !important;
}}

.stTextInput input {{
    color: {TEXT_PRIMARY} !important;
    padding: 10px 20px !important;
    background-color: transparent !important;
}}

.stTextInput div[data-baseweb="input"]:focus-within {{
    border-color: {PRIMARY_BLUE} !important;
    box-shadow: 0 0 0 1px {PRIMARY_BLUE} !important;
}}
</style>

""", unsafe_allow_html=True)

# Load Data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "driving_questions.csv")

@st.cache_data
def load_data():
    if not os.path.exists(CSV_FILE): return None
    try:
        # Load with explicit quoting handling
        df = pd.read_csv(CSV_FILE, quotechar='"')
        return df
    except: return None

df = load_data()
if df is None:
    st.error("Base de données manquante ou corrompue.")
    st.stop()

# State Management
if 'card_index' not in st.session_state: st.session_state.card_index = 0
if 'show_answer' not in st.session_state: st.session_state.show_answer = False

# Sidebar
with st.sidebar:
    st.header("Filtres")
    categories = ["Tous"] + sorted(df['Category'].unique().tolist())
    selected_category = st.selectbox("Sujet", categories)
    group_id_search = st.text_input("Derniers chiffres compteur (00-99)", placeholder="Ex: 42")
    
    st.markdown("---")
    if st.button("🔀 Tirage Aléatoire"):
        st.session_state.card_index = random.randint(0, len(df)-1)
        st.session_state.show_answer = False

# Filtering logic
filtered_df = df.copy()
if selected_category != "Tous":
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]
if group_id_search:
    try:
        val = int(group_id_search)
        filtered_df = filtered_df[filtered_df['Group_ID'] == val]
    except: pass

if filtered_df.empty:
    st.warning("Aucun résultat pour cette recherche.")
    st.stop()

# Reset index if out of bounds
if st.session_state.card_index >= len(filtered_df):
    st.session_state.card_index = 0

# Card Display
row = filtered_df.iloc[st.session_state.card_index]
cat_tag = f"{row['Category']} | GROUPE {str(row['Group_ID']).zfill(2)}"
q_text = row['Question'].replace("'", "&#39;")
a_text = row['Reponse Attendue'].replace("'", "&#39;")
c_text = row['Context Info'].replace("'", "&#39;")

card_html = f'<div class="card"><div><div class="category-tag">{cat_tag}</div><div class="question">{q_text}</div></div>'
if st.session_state.show_answer:
    card_html += f"""
    <div>
        <div class="divider"></div>
        <div style="display: flex; flex-direction: column; gap: 20px;">
            <div class="answer-container">
                <div style="font-size: 0.85rem; font-weight: bold; color: {PRIMARY_BLUE}; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Réponse Attendue</div>
                <div class="answer">{a_text}</div>
            </div>
            <div class="context-container" style="background-color: rgba(255, 255, 255, 0.03); border-left: 4px solid {TEXT_SECONDARY}; padding: 20px; border-radius: 4px;">
                <div style="font-size: 0.85rem; font-weight: bold; color: {TEXT_SECONDARY}; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">💡 Contexte & Astuce</div>
                <div style="font-size: 1.05rem; color: {TEXT_PRIMARY}; line-height: 1.5; font-style: italic;">{c_text}</div>
            </div>
        </div>
    </div>
    """
else:
    card_html += '<div class="hidden-answer">Cliquez sur &#39;Afficher la réponse&#39; pour voir la solution</div>'
card_html += '</div>'

st.markdown(card_html, unsafe_allow_html=True)

# Progress
st.progress((st.session_state.card_index + 1) / len(filtered_df))
st.caption(f"Question {st.session_state.card_index + 1} sur {len(filtered_df)}")

# Buttons
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.button("← Précédent", use_container_width=True):
        st.session_state.card_index = (st.session_state.card_index - 1) % len(filtered_df)
        st.session_state.show_answer = False
        st.rerun()
with c2:
    label = "Masquer la réponse" if st.session_state.show_answer else "Afficher la réponse"
    if st.button(label, use_container_width=True):
        st.session_state.show_answer = not st.session_state.show_answer
        st.rerun()
with c3:
    if st.button("Suivant →", use_container_width=True):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(filtered_df)
        st.session_state.show_answer = False
        st.rerun()
