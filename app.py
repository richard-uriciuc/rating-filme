import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="CineRating Pro", page_icon="🎬", layout="wide")

# --- CHEIA TA API ---
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN PERSONALIZAT (CSS AVANSAT) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp { background-color: #F3F4F6; font-family: 'Inter', sans-serif; }
    
    /* Efect de sticlă pentru carduri */
    .glass-card {
        background: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }
    
    .landing-header {
        text-align: center;
        padding: 100px 20px 50px 20px;
    }
    
    .rating-badge {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        padding: 12px;
        border-radius: 16px;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .rating-badge:hover { transform: translateY(-5px); border-color: #3B82F6; }
    
    .cnc-btn {
        background-color: #10B981;
        color: white !important;
        padding: 12px 24px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin-top: 20px;
    }
    
    .legend-box {
        font-size: 0.85rem;
        background: #EFF6FF;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3B82F6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DE LEGENDĂ ---
legenda = {
    "RO": {"AG": "Toate vârstele", "AP-12": "Acordul părinților (sub 12)", "N-15": "Nerecomandat sub 15 ani", "18": "Interzis minorilor"},
    "US": {"G": "General", "PG": "Acordul părinților", "PG-13": "Peste 13 ani", "R": "Restricționat (sub 17 cu adult)", "NC-17": "Strict peste 18"},
    "ES": {"A / TP": "Toate vârstele", "7": "Peste 7 ani", "12": "Peste 12 ani", "16": "Peste 16 ani", "18": "Interzis minorilor"},
    "DE": {"0": "General", "6": "Peste 6 ani", "12": "Peste 12 ani", "16": "Peste 16 ani", "18": "Peste 18 ani"},
    "FR": {"U": "Toate vârstele", "12": "Peste 12 ani", "16": "Peste 16 ani", "18": "Peste 18 ani"}
}

# --- PAGINA DE ÎNTÂMPINARE SAU CĂUTARE ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

def trigger_search():
    st.session_state.search_query = st.session_state.temp_query

if not st.session_state.search_query:
    # LANDING PAGE
    st.markdown('<div class="landing-header"><h1>🎬 CineRating Global</h1><p>Descoperă cum este catalogat filmul tău preferat în jurul lumii.</p></div>', unsafe_allow_html=True)
    st.text_input("Ce film vrei să verifici?", key="temp_query", on_change=trigger_search, placeholder="Introdu titlul aici (ex: Inception)...")
else:
    # PAGINA DE REZULTATE
    st.text_input("Caută alt film:", key="temp_query", on_change=trigger_search)
    
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"query": st.session_state.search_query, "language": "ro-RO"}
    
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200 and res.json().get('results'):
        movie = res.json()['results'][0]
        m_id = movie['id']
        
        # Detalii complete
        d_res = requests.get(f"https://api.themoviedb.org/3/movie/{m_id}?append_to_response=release_dates,credits&language=ro-RO", headers=headers).json()
        
        # AFIȘARE CURSIVĂ
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(f"https://image.tmdb.org/t/p/w500{d_res.get('poster_path')}", use_container_width=True)
        
        with col2:
            st.title(d_res.get('title'))
            st.markdown(f"**Regia:** {', '.join([c['name'] for c in d_res.get('credits', {}).get('crew', []) if c['job'] == 'Director'])}")
            st.write(d_res.get('overview'))
            st.markdown(f'<a href="http://cnc.gov.ro/registrul-cinematografiei/" target="_blank" class="cnc-btn">🔍 Verifică oficial la CNC România</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECȚIUNE RATING-URI
        st.subheader("🌍 Catalogare Internațională")
        countries = {'RO': '🇷🇴 România', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 'DE': '🇩🇪 Germania', 'FR': '🇫🇷 Franța', 'ES': '🇪🇸 Spania'}
        
        ratings_data = {}
        for r in d_res.get('release_dates', {}).get('results', []):
            if r['iso_3166_1'] in countries:
                ratings_data[r['iso_3166_1']] = r['release_dates'][0]['certification']

        c_cols = st.columns(len(countries))
        for i, (code, name) in enumerate(countries.items()):
            with c_cols[i]:
                val = ratings_data.get(code, "N/A")
                st.markdown(f"""
                    <div class="rating-badge">
                        <small>{name}</small><br>
                        <span style="font-size:1.5rem; font-weight:bold;">{val}</span>
                    </div>
                """, unsafe_allow_html=True)

        # LEGENDA (Ceea ce ai cerut)
        with st.expander("📖 Vezi legenda și semnificația simbolurilor"):
            l_col1, l_col2 = st.columns(2)
            with l_col1:
                st.markdown("**🇷🇴 România / 🇺🇸 USA**")
                for k, v in legenda['RO'].items(): st.write(f"**{k}:** {v}")
                for k, v in legenda['US'].items(): st.write(f"**{k}:** {v}")
            with l_col2:
                st.markdown("**🇪🇸 Spania / 🇩🇪 Germania**")
                for k, v in legenda['ES'].items(): st.write(f"**{k}:** {v}")
                for k, v in legenda['DE'].items(): st.write(f"**{k}:** {v}")

    else:
        st.error("Nu am găsit filmul. Te rugăm să verifici titlul.")
        if st.button("Înapoi la pornire"):
            st.session_state.search_query = ""
            st.rerun()
