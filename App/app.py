import streamlit as st
import pandas as pd
import random
import os

# Material Design Dark Theme Colors
PRIMARY_BLUE = "#8AB4F8"
SURFACE_DARK = "#202124"
CARD_DARK = "#292A2D"
TEXT_PRIMARY = "#E8EAED"
TEXT_SECONDARY = "#9AA0A6"
DIVIDER = "#3C4043"
SUCCESS_GREEN = "#81C995"
ERROR_RED = "#F28B82"

# Set page config
st.set_page_config(
    page_title="Permis de Conduire - Flashcards",
    page_icon="🚗",
    layout="wide"  # Use wide layout for better list view
)

# Comprehensive CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* Main Background */
.stApp {{
    background-color: {SURFACE_DARK} !important;
    font-family: 'Roboto', sans-serif;
}}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 24px;
}}
.stTabs [data-baseweb="tab"] {{
    color: {TEXT_SECONDARY};
    background-color: transparent;
    padding-top: 10px;
    padding-bottom: 10px;
    font-size: 1.1rem;
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    color: {PRIMARY_BLUE} !important;
    border-bottom-color: {PRIMARY_BLUE} !important;
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
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
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

.btn-success > button {{
    color: {SUCCESS_GREEN} !important;
    border-color: {SUCCESS_GREEN} !important;
}}
.btn-success > button:hover {{
    background-color: rgba(129, 201, 149, 0.1) !important;
}}

.btn-danger > button {{
    color: {ERROR_RED} !important;
    border-color: {ERROR_RED} !important;
}}
.btn-danger > button:hover {{
    background-color: rgba(242, 139, 130, 0.1) !important;
}}

.stProgress > div > div > div > div {{
    background-color: {PRIMARY_BLUE};
}}
/* Sidebar and Inputs */
[data-testid="stSidebar"] {{
    background-color: {CARD_DARK} !important;
}}

/* Unified Input Styling (Pill shape) */
.stTextInput div[data-baseweb="input"],
.stTextInput div[data-baseweb="input"] > div,
.stTextInput input {{
    border-radius: 28px !important;
    border: none !important;
}}

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

/* List View Styling */
.list-item {{
    background-color: {CARD_DARK};
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    border-left: 5px solid {DIVIDER};
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}
.cat-tech {{ border-left-color: {PRIMARY_BLUE}; }}
.cat-safe {{ border-left-color: #F8BC45; }} /* Google Yellow variant */
.cat-first {{ border-left-color: {SUCCESS_GREEN}; }}

.list-q {{ font-size: 1.2rem; color: {TEXT_PRIMARY}; font-weight: 500; margin-bottom: 10px; }}
.list-a {{ font-size: 1rem; color: {TEXT_SECONDARY}; margin-bottom: 10px; }}
.list-meta {{ font-size: 0.8rem; color: {TEXT_SECONDARY}; text-transform: uppercase; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# Load Data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "driving_questions.csv")

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path): return None
    try:
        df = pd.read_csv(file_path, quotechar='"', encoding='utf-8')
        
        # Validation for expected columns
        expected_cols = ['Category', 'Group_ID', 'Question', 'Reponse Attendue', 'Context Info']
        for col in expected_cols:
            if col not in df.columns:
                st.error(f"Fichier CSV invalide. Colonne manquante: {col}")
                return None
                
        # Create a unique ID for tracking scores
        df['UID'] = df.index
        return df
    except: return None

df = load_data(CSV_FILE)
if df is None:
    st.error("Base de données manquante ou corrompue.")
    st.stop()

# State Management
if 'card_index' not in st.session_state: st.session_state.card_index = 0
if 'show_answer' not in st.session_state: st.session_state.show_answer = False
if 'scores' not in st.session_state: st.session_state.scores = {} # Dict mapping UID -> True (Right) / False (Wrong)
if 'active_view' not in st.session_state: st.session_state.active_view = "🃏 Mode Flashcards"
if 'exam_mode_active' not in st.session_state: st.session_state.exam_mode_active = False
if 'exam_group_id' not in st.session_state: st.session_state.exam_group_id = None

# Exam Mode Callback
def start_exam():
    st.session_state.scores = {}
    st.session_state.active_view = "🃏 Mode Flashcards"
    st.session_state.card_index = 0
    st.session_state.show_answer = False
    
    # Pick a random group from 0 to 99
    valid_groups = df['Group_ID'].unique()
    exam_group = int(random.choice(valid_groups))
    
    st.session_state.exam_mode_active = True
    st.session_state.exam_group_id = exam_group

# View Switch Callback
def switch_to_card(index):
    st.session_state.active_view = "🃏 Mode Flashcards"
    st.session_state.card_index = index
    st.session_state.show_answer = False

# Card Navigation Callbacks
def next_card_cb(total):
    st.session_state.card_index = (st.session_state.card_index + 1) % total
    st.session_state.show_answer = False

def prev_card_cb(total):
    st.session_state.card_index = (st.session_state.card_index - 1) % total
    st.session_state.show_answer = False

def toggle_answer_cb():
    st.session_state.show_answer = not st.session_state.show_answer

def eval_card_cb(uid, correct, total):
    st.session_state.scores[uid] = correct
    next_card_cb(total)
    
# Remove Exam Mode if user interacts with sidebar filters
def reset_exam_mode():
    st.session_state.exam_mode_active = False

# Sidebar
with st.sidebar:
    st.header("Filtres")
    categories = ["Tous"] + sorted(df['Category'].unique().tolist())
    
    # Force filters if Exam Mode is active
    if st.session_state.exam_mode_active:
        selected_category = st.selectbox("Sujet", categories, index=0, on_change=reset_exam_mode)
        group_id_search = st.text_input("Derniers chiffres compteur (00-99)", value=str(st.session_state.exam_group_id), on_change=reset_exam_mode)
        st.success("🎓 EXAMEN BLANC EN COURS")
    else:
        selected_category = st.selectbox("Sujet", categories, on_change=reset_exam_mode)
        group_id_search = st.text_input("Derniers chiffres compteur (00-99)", placeholder="Ex: 42", on_change=reset_exam_mode)
    
    # Filtering logic - Must happen before buttons that use filtered_df
    filtered_df = df
    if selected_category != "Tous":
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if group_id_search:
        try:
            val = int(group_id_search)
            filtered_df = filtered_df[filtered_df['Group_ID'] == val]
        except ValueError:
            st.error("Veuillez entrer un nombre valide (ex: 42).")

    st.markdown("---")
    st.button("🎓 Lancer un Examen Blanc", on_click=start_exam, use_container_width=True, type="primary")
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🔀 Tirage Aléatoire", use_container_width=True):
        if not filtered_df.empty:
            st.session_state.card_index = random.randint(0, len(filtered_df)-1)
            st.session_state.show_answer = False
        
    st.markdown("---")
    st.header("Navigation")
    view_selection = st.radio("Mode d'affichage", ["🃏 Mode Flashcards", "📋 Mode Liste Colorée"], 
                             key="active_view", 
                             label_visibility="collapsed")

    st.markdown("---")
    st.header("Statistiques")
    known = sum(1 for v in st.session_state.scores.values() if v)
    unknown = sum(1 for v in st.session_state.scores.values() if not v)
    st.write(f"✅ Acquises : **{known}**")
    st.write(f"❌ À revoir : **{unknown}**")
    if st.button("🔄 Réinitialiser les scores"):
        st.session_state.scores = {}
        st.rerun()
    
    st.markdown("---")
    st.caption("Version 1.0.2")

if filtered_df.empty:
    st.warning("Aucun résultat pour cette recherche. Veuillez modifier vos filtres dans le menu latéral.")
    st.stop()
    
# Reset index if out of bounds
if st.session_state.card_index >= len(filtered_df):
    st.session_state.card_index = 0

# Ensure view_selection is defined from session state if radio wasn't triggered
view_selection = st.session_state.active_view

if view_selection == "🃏 Mode Flashcards":
    # Card Display
    row = filtered_df.iloc[st.session_state.card_index]
    uid = row['UID']
    cat_tag = f"{row['Category']} | GROUPE {str(row['Group_ID']).zfill(2)}"
    
    # Status indicator
    status_icon = ""
    if uid in st.session_state.scores:
        status_icon = " ✅" if st.session_state.scores[uid] else " ❌"
    
    q_text = str(row['Question'])
    a_text = str(row['Reponse Attendue'])
    c_text = str(row['Context Info'])

    card_html = f'<div class="card"><div><div class="category-tag">{cat_tag}{status_icon}</div><div class="question">{q_text}</div></div>'
    if st.session_state.show_answer:
        card_html += f'<div><div class="divider"></div><div style="display: flex; flex-direction: column; gap: 20px;"><div class="answer-container"><div style="font-size: 0.85rem; font-weight: bold; color: {PRIMARY_BLUE}; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Réponse Attendue</div><div class="answer">{a_text}</div></div><div class="context-container" style="background-color: rgba(255, 255, 255, 0.03); border-left: 4px solid {TEXT_SECONDARY}; padding: 20px; border-radius: 4px;"><div style="font-size: 0.85rem; font-weight: bold; color: {TEXT_SECONDARY}; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">💡 Contexte & Astuce</div><div style="font-size: 1.05rem; color: {TEXT_PRIMARY}; line-height: 1.5; font-style: italic;">{c_text}</div></div></div></div>'
    card_html += '</div>'

    st.markdown(card_html, unsafe_allow_html=True)

    # Core Navigation Buttons
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        st.button("← Précédent", on_click=prev_card_cb, args=(len(filtered_df),), use_container_width=True)
    with c2:
        label = "Masquer la réponse" if st.session_state.show_answer else "Afficher la réponse"
        st.button(label, key=f"btn_toggle", on_click=toggle_answer_cb, use_container_width=True)
    with c3:
        st.button("Suivant →", on_click=next_card_cb, args=(len(filtered_df),), use_container_width=True)
            
    # Self-Evaluation Buttons (Only visible when answer is shown)
    if st.session_state.show_answer:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col_eval1, col_eval2, col_eval3, col_eval4 = st.columns([1, 1, 1, 1])
        with col_eval2:
            st.markdown('<div class="btn-success">', unsafe_allow_html=True)
            st.button("✅ J'avais bon", key=f"btn_correct_{uid}", on_click=eval_card_cb, args=(uid, True, len(filtered_df)), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_eval3:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            st.button("❌ J'avais faux", key=f"btn_false_{uid}", on_click=eval_card_cb, args=(uid, False, len(filtered_df)), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Progress
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress((st.session_state.card_index + 1) / len(filtered_df))
    st.caption(f"Question {st.session_state.card_index + 1} sur {len(filtered_df)}")


elif view_selection == "📋 Mode Liste Colorée":
    st.markdown("### Liste Complète des Questions")
    st.caption("Filtrez via le menu latéral pour afficher uniquement le groupe désiré.")
    
    # Iterate dynamically to create buttons inline
    for local_index, (_, item) in enumerate(filtered_df.iterrows()):
        cat = str(item['Category']).lower()
        if "vérification" in cat: border_class = "cat-tech"
        elif "sécurité" in cat: border_class = "cat-safe"
        else: border_class = "cat-first"
        
        status = ""
        uid = item['UID']
        if uid in st.session_state.scores:
            status = " <span style='color:#81C995;'>✅</span>" if st.session_state.scores[uid] else " <span style='color:#F28B82;'>❌</span>"
            
        c1, c2 = st.columns([6, 1])
        with c1:
            html = f'<div class="list-item {border_class}" style="margin-bottom: 0px;"><div class="list-meta">{item["Category"]} | GROUPE {str(item["Group_ID"]).zfill(2)}{status}</div><div class="list-q">{item["Question"]}</div><div class="list-a"><strong>Rép:</strong> {item["Reponse Attendue"]}</div></div>'
            st.markdown(html, unsafe_allow_html=True)
        with c2:
            st.button("🃏 Étudier", key=f"btn_{uid}", on_click=switch_to_card, args=(local_index,), use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
