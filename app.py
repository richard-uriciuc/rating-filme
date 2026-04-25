import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="CineRating Global", page_icon="🎬", layout="wide")

# --- CHEIA TA API ---
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-"

# --- DESIGN PROFESIONIST (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-card { background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .rating-container { display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 20px; }
    .rating-box { 
        background: #F1F5F9; 
        padding: 15px; 
        border-radius: 12px; 
        text-align: center; 
        min-width: 110px;
        margin: 5px;
        border-bottom: 4px solid #CBD5E1;
    }
    .rating-value { font-size: 1.6rem; font-weight: bold; color: #1E293B; }
    .cnc-button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #D1FAE5; /* Mentă pastel */
        color: #065F46;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        margin-top: 15px;
        transition: 0.3s;
    }
    .cnc-button:hover { background-color: #A7F3D0; }
    </style>
    """, unsafe_allow_html=True)

# --- ANTET ---
st.title("🎞️ CineRating Global")
st.markdown("<p style='color: #64748B;'>Comparație internațională a clasificărilor de vârstă</p>", unsafe_allow_html=True)

query = st.text_input("Introdu numele filmului:", placeholder="Ex: Gladiator, Joker, Braveheart...")

if query:
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    search_res = requests.get(f"https://api.themoviedb.org/3/search/multi?query={query}&language=ro-RO", headers=headers).json()
    
    if search_res.get('results'):
        item = search_res['results'][0]
        item_id = item['id']
        media_type = item.get('media_type', 'movie')

        # Cerem datele complete
        details_url = f"https://api.themoviedb.org/3/{media_type}/{item_id}?append_to_response=release_dates,content_ratings,credits&language=ro-RO"
        data = requests.get(details_url, headers=headers).json()

        # Secțiunea de detalii
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2.5])
        
        with col1:
            poster = f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}"
            st.image(poster, use_container_width=True)
        
        with col2:
            st.header(data.get('title', data.get('name')))
            st.write(data.get('overview', "Descriere indisponibilă."))
            
            # BUTONUL CNC
            st.markdown(f"""
                <a href="http://cnc.gov.ro/clasificare-filme/" target="_blank" class="cnc-button">
                    🔍 Verifică oficial la CNC România
                </a>
                <p style="font-size: 0.8rem; color: #94A3B8; margin-top: 5px;">
                    (Se va deschide pagina oficială de căutare a clasificărilor)
                </p>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # TABELUL DE RATING-URI
        st.write("---")
        st.subheader("🌍 Clasificări pe regiuni")
        
        countries = {
            'RO': '🇷🇴 România', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 
            'DE': '🇩🇪 Germania', 'FR': '🇫🇷 Franța', 'IT': '🇮🇹 Italia', 
            'ES': '🇪🇸 Spania', 'AU': '🇦🇺 Australia'
        }
        
        found_ratings = {}
        if 'release_dates' in data:
            for r in data['release_dates']['results']:
                if r['iso_3166_1'] in countries:
                    found_ratings[r['iso_3166_1']] = r['release_dates'][0]['certification']
        elif 'content_ratings' in data:
            for r in data['content_ratings']['results']:
                if r['iso_3166_1'] in countries:
                    found_ratings[r['iso_3166_1']] = r['rating']

        # Afișare estetică
        cols = st.columns(len(countries))
        for i, (code, name) in enumerate(countries.items()):
            with cols[i]:
                val = found_ratings.get(code, "N/A")
                st.markdown(f"""
                    <div class="rating-box">
                        <div style="font-size:0.7rem; color: #64748B;">{name}</div>
                        <div class="rating-value">{val}</div>
                    </div>
                """, unsafe_allow_html=True)

    else:
        st.warning("Nu am găsit rezultate. Verifică ortografia!")

st.markdown("<br><hr><center style='color: #94A3B8; font-size: 0.8rem;'>Date furnizate de TMDB API. Butonul 'Verifică' te trimite la sursa guvernamentală RO.</center>", unsafe_allow_html=True)
