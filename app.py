import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="CineRating Global", page_icon="🎬", layout="wide")

# --- CHEIA TA API (Verifică să fie cea LUNGĂ) ---
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-card { background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .rating-box { background: #F1F5F9; padding: 15px; border-radius: 12px; text-align: center; min-width: 110px; margin: 5px; border-bottom: 4px solid #CBD5E1; }
    .rating-value { font-size: 1.6rem; font-weight: bold; color: #1E293B; }
    .cnc-button { display: inline-block; padding: 10px 20px; background-color: #D1FAE5; color: #065F46; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎞️ CineRating Global")

query = st.text_input("Introdu numele filmului:", placeholder="Ex: Back to the Future, Gladiator...")

if query:
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}", "Content-Type": "application/json"}
    
    # Căutare îmbunătățită (gestionează spațiile corect)
    url_search = "https://api.themoviedb.org/3/search/movie"
    params = {"query": query, "language": "ro-RO"}
    
    response = requests.get(url_search, headers=headers, params=params)
    
    if response.status_code == 200:
        search_res = response.json()
        if search_res.get('results'):
            item = search_res['results'][0]
            item_id = item['id']

            # Detalii film
            details_url = f"https://api.themoviedb.org/3/movie/{item_id}"
            params_details = {"append_to_response": "release_dates,credits", "language": "ro-RO"}
            data = requests.get(details_url, headers=headers, params=params_details).json()

            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 2.5])
            with c1:
                st.image(f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}", use_container_width=True)
            with c2:
                st.header(data.get('title'))
                st.write(data.get('overview'))
                st.markdown(f'<a href="http://cnc.gov.ro/clasificare-filme/" target="_blank" class="cnc-button">🔍 Verifică oficial la CNC România</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Ratinguri
            st.write("---")
            st.subheader("🌍 Clasificări internaționale")
            countries = {'RO': '🇷🇴 RO', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 'DE': '🇩🇪 DE', 'FR': '🇫🇷 FR', 'IT': '🇮🇹 IT', 'ES': '🇪🇸 ES'}
            
            ratings = {}
            for r in data.get('release_dates', {}).get('results', []):
                if r['iso_3166_1'] in countries:
                    ratings[r['iso_3166_1']] = r['release_dates'][0]['certification']

            cols = st.columns(len(countries))
            for i, (code, name) in enumerate(countries.items()):
                with cols[i]:
                    val = ratings.get(code, "N/A")
                    st.markdown(f'<div class="rating-box"><div style="font-size:0.7rem;">{name}</div><div class="rating-value">{val}</div></div>', unsafe_allow_html=True)
        else:
            st.warning("Nu am găsit rezultate. Verifică ortografia!")
    elif response.status_code == 401:
        st.error("❌ Eroare: Cheia ta API (Token-ul) nu este corectă. Asigură-te că ai copiat tot codul cel LUNG.")
    else:
        st.error(f"❌ Problemă tehnică: Serverul a răspuns cu eroarea {response.status_code}")
