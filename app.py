import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="CineRating Global", page_icon="🎬", layout="centered")

# --- CHEIA TA API (Rămâne aceeași) ---
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN PERSONALIZAT (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Fundalul general */
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Poppins', sans-serif;
    }}

    /* Containerul principal */
    .main-container {{
        background-color: rgba(255, 255, 255, 0.7);
        padding: 30px;
        border-radius: 25px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}

    /* Titlul */
    .main-title {{
        color: #2D3748;
        text-align: center;
        font-weight: 600;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }}

    /* Cardul filmului */
    .movie-card {{
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        border-left: 10px solid #FFD1DC;
        margin-top: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
    }}

    /* Rating-uri colorate */
    .rating-box {{
        display: inline-block;
        padding: 8px 15px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        margin: 5px;
        text-align: center;
        min-width: 60px;
    }}
    .rating-ag {{ background-color: #7ed6df; }}
    .rating-12 {{ background-color: #f9ca24; }}
    .rating-15 {{ background-color: #f0932b; }}
    .rating-18 {{ background-color: #eb4d4b; }}
    .rating-default {{ background-color: #95afc0; }}

    /* Input box */
    .stTextInput>div>div>input {{
        border-radius: 15px;
        border: 2px solid #FFD1DC;
        padding: 10px 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ANTET ---
st.markdown('<p class="main-title">🎞️ CineRating Global 🎥</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#718096;">Ghidează-te prin lumea filmului cu stil</p>', unsafe_allow_html=True)

# --- CĂUTARE ---
query = st.text_input("", placeholder="Scrie numele unui film...")

if query:
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    search_res = requests.get(f"https://api.themoviedb.org/3/search/multi?query={query}&language=ro-RO", headers=headers).json()
    
    if search_res.get('results'):
        item = search_res['results'][0]
        item_id = item['id']
        media_type = item.get('media_type', 'movie')

        details_url = f"https://api.themoviedb.org/3/{media_type}/{item_id}?append_to_response=release_dates,content_ratings,credits&language=ro-RO"
        data = requests.get(details_url, headers=headers).json()

        # Date film
        titlu = data.get('title') or data.get('name')
        titlu_orig = data.get('original_title') or data.get('original_name')
        descriere = data.get('overview', 'Povestea acestui film este încă un mister...')
        poster = f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}"
        durata = data.get('runtime') or "N/A"
        regie = "Necunoscut"
        if 'credits' in data:
            for p in data['credits']['crew']:
                if p['job'] == 'Director': regie = p['name']; break

        # AFIȘARE
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.image(poster, use_container_width=True)
            
        with col2:
            st.markdown(f"## {titlu}")
            st.markdown(f"*({titlu_orig})*")
            st.write(f"🎬 **Regia:** {regie}")
            st.write(f"⏱️ **Durata:** {durata} min")
            st.write(descriere)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # RATING-URI
        st.write("### 🌍 Recomandări de vârstă:")
        
        ratings = {}
        target_countries = {'RO': '🇷🇴 România', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 'DE': '🇩🇪 DE', 'FR': '🇫🇷 FR'}
        
        # Extragere logică rating
        if 'release_dates' in data:
            for r in data['release_dates']['results']:
                if r['iso_3166_1'] in target_countries:
                    ratings[r['iso_3166_1']] = r['release_dates'][0]['certification']
        elif 'content_ratings' in data:
            for r in data['content_ratings']['results']:
                if r['iso_3166_1'] in target_countries:
                    ratings[r['iso_3166_1']] = r['rating']

        # Afișare stilizată rating-uri
        row = st.columns(len(target_countries))
        for i, (code, name) in enumerate(target_countries.items()):
            val = ratings.get(code, "?")
            
            # Alegem culoarea în funcție de rating
            css_class = "rating-default"
            v = str(val).upper()
            if any(x in v for x in ['AG', 'G', 'U', 'ALL']): css_class = "rating-ag"
            elif any(x in v for x in ['12', 'PG13', 'PG']): css_class = "rating-12"
            elif any(x in v for x in ['15', '16', 'R', 'MA']): css_class = "rating-15"
            elif any(x in v for x in ['18', 'NC17', 'X']): css_class = "rating-18"

            with row[i]:
                st.markdown(f"<div style='text-align:center; font-size:0.8rem;'>{name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='rating-box {css_class}'>{val}</div>", unsafe_allow_html=True)

    else:
        st.warning("Nu am găsit nimic. Încearcă alt titlu!")
