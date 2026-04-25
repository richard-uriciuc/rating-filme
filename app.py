import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="CineRating Global", page_icon="🎬", layout="wide")

# AICI LIPESTE CODUL TAU CEL LUNG (API Read Access Token)
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- STILIZARE PASTEL (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #F0F4F8; }
    .stButton>button { background-color: #FFD1DC; border-radius: 20px; border: none; }
    .movie-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1 { color: #4A5568; font-family: 'Segoe UI', sans-serif; }
    .rating-badge { padding: 5px 10px; border-radius: 8px; font-weight: bold; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ANTET CU DECORAȚIUNI ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1: st.write("🎞️") # Rola de film (stânga)
with col2: st.title("🎬 CineRating Global")
with col3: st.write("🎥") # Camera de filmat (dreapta)

st.write("---")

# --- CAUTARE ---
query = st.text_input("Ce film sau serial cauți?", placeholder="Ex: Gladiator, Wednesday...")

if query:
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    
    # 1. Căutăm filmul
    search_res = requests.get(f"https://api.themoviedb.org/3/search/multi?query={query}&language=ro-RO", headers=headers).json()
    
    if search_res.get('results'):
        item = search_res['results'][0]
        item_id = item['id']
        media_type = item['media_type'] # movie sau tv

        # 2. Luăm detaliile complete (rating-uri, regie, durată)
        details_url = f"https://api.themoviedb.org/3/{media_type}/{item_id}?append_to_response=release_dates,content_ratings,credits&language=ro-RO"
        data = requests.get(details_url, headers=headers).json()

        # Pregătim datele
        titlu = data.get('title') or data.get('name')
        titlu_orig = data.get('original_title') or data.get('original_name')
        descriere = data.get('overview', 'Fără descriere disponibilă.')
        poster = f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}"
        durata = data.get('runtime') or (data.get('episode_run_time', [0])[0] if data.get('episode_run_time') else 0)
        
        # Extragem Regizorul (doar pentru filme)
        regie = "Informație indisponibilă"
        if 'credits' in data:
            for person in data['credits']['crew']:
                if person['job'] == 'Director':
                    regie = person['name']
                    break

        # --- AFIȘARE REZULTAT ---
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.image(poster, use_container_width=True)
            
        with c2:
            st.subheader(f"{titlu}")
            st.caption(f"Titlu original: {titlu_orig}")
            st.write(f"⏱️ **Durată:** {durata} min | 🎬 **Regie:** {regie}")
            st.info(descriere)
            
            st.write("### 🌍 Clasificări pe țări:")
            
            # Extragem rating-urile
            ratings = {}
            # Pentru filme
            if 'release_dates' in data:
                for entry in data['release_dates']['results']:
                    tara = entry['iso_3166_1']
                    if tara in ['RO', 'US', 'DE', 'FR', 'GB', 'ES']:
                        cert = entry['release_dates'][0]['certification']
                        if cert: ratings[tara] = cert
            # Pentru seriale
            elif 'content_ratings' in data:
                for entry in data['content_ratings']['results']:
                    tara = entry['iso_3166_1']
                    if tara in ['RO', 'US', 'DE', 'FR', 'GB', 'ES']:
                        if entry['rating']: ratings[tara] = entry['rating']

            # Afișăm tabelul cu steaguri
            cols = st.columns(len(ratings) if ratings else 1)
            steaguri = {"RO": "🇷🇴 RO", "US": "🇺🇸 US", "DE": "🇩🇪 DE", "FR": "🇫🇷 FR", "GB": "🇬🇧 UK", "ES": "🇪🇸 ES"}
            
            if ratings:
                for i, (tara, val) in enumerate(ratings.items()):
                    with cols[i % len(cols)]:
                        st.metric(label=steaguri.get(tara, tara), value=val)
            else:
                st.warning("Nu am găsit clasificări oficiale pentru acest titlu în baza de date.")

    else:
        st.error("Hopa! Nu am găsit niciun film cu acest nume.")