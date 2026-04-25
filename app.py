import streamlit as st
import requests

# --- CONFIGURARE ---
st.set_page_config(page_title="CineRating Intelligence", page_icon="🎬", layout="wide")

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN MODERN & CURAT ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-container { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .rating-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.03);
    }
    .rating-label { font-size: 0.75rem; color: #666; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; }
    .rating-value { font-size: 1.3rem; font-weight: 800; color: #222; }
    .movie-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 0; color: #1a1a1a; }
    .movie-meta { color: #555; font-size: 1rem; margin-bottom: 20px; }
    .legend-section { background: #f9f9f9; padding: 20px; border-radius: 10px; margin-top: 30px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- REZOLVARE CĂUTARE INTELIGENTĂ ---
def get_best_movie(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"query": query, "language": "ro-RO"}
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    res = requests.get(url, headers=headers, params=params).json()
    
    if not res.get('results'): return None
    # Sortăm după popularitate ca să evităm documentarele sau "Special Features"
    sorted_movies = sorted(res['results'], key=lambda x: x.get('popularity', 0), reverse=True)
    return sorted_movies[0]

# --- UI PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>🎬 CineRating Intelligence</h1>", unsafe_allow_html=True)
query = st.text_input("", placeholder="Introdu numele filmului (ex: Back to the Future, Gladiator)...")

if query:
    movie = get_best_movie(query)
    
    if movie:
        m_id = movie['id']
        headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
        data = requests.get(f"https://api.themoviedb.org/3/movie/{m_id}?append_to_response=release_dates,credits&language=ro-RO", headers=headers).json()
        
        # --- ZONA DINAMICĂ (STÂNGA: POSTER | DREAPTA: INFO & RATINGS) ---
        col_poster, col_info = st.columns([1, 2.2])
        
        with col_poster:
            st.image(f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}", use_container_width=True)
            st.markdown(f'<a href="http://cnc.gov.ro/registrul-cinematografiei/" target="_blank" style="display:block; text-align:center; background:#10B981; color:white; padding:10px; border-radius:8px; text-decoration:none; font-weight:bold;">🔍 Verifică la CNC România</a>', unsafe_allow_html=True)

        with col_info:
            st.markdown(f"<div class='movie-title'>{data.get('title')}</div>", unsafe_allow_html=True)
            regizor = ", ".join([c['name'] for c in data.get('credits', {}).get('crew', []) if c['job'] == 'Director'])
            st.markdown(f"<div class='movie-meta'>🗓️ {data.get('release_date')[:4]} | ⏱️ {data.get('runtime')} min | 🎬 Regia: {regizor}</div>", unsafe_allow_html=True)
            st.write(data.get('overview'))
            
            st.write("### 🌍 Clasificări pe țări")
            
            # Configurăm țările cerute
            target_countries = {
                'RO': '🇷🇴 RO', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 'FR': '🇫🇷 FR', 
                'DE': '🇩🇪 DE', 'IT': '🇮🇹 IT', 'ES': '🇪🇸 ES', 'CA': '🇨🇦 CA', 
                'AU': '🇦🇺 AU', 'JP': '🇯🇵 JP'
            }
            
            # Extragere date
            ratings = {}
            for r in data.get('release_dates', {}).get('results', []):
                if r['iso_3166_1'] in target_countries:
                    ratings[r['iso_3166_1']] = r['release_dates'][0]['certification']

            # Afișare în grilă compactă (2 rânduri de câte 5)
            r_col = st.columns(5)
            country_codes = list(target_countries.keys())
            for i in range(10):
                with r_col[i % 5]:
                    code = country_codes[i]
                    val = ratings.get(code, "N/A")
                    st.markdown(f"""
                        <div class="rating-card">
                            <div class="rating-label">{target_countries[code]}</div>
                            <div class="rating-value">{val if val else 'N/A'}</div>
                        </div>
                    """, unsafe_allow_html=True)

        # --- LEGENDA PROFESIONALĂ JOS ---
        st.markdown("<div class='legend-section'>", unsafe_allow_html=True)
        st.markdown("### 📖 Legenda Clasificărilor Internaționale")
        leg1, leg2, leg3 = st.columns(3)
        
        with leg1:
            st.markdown("**🇪🇺 Europa (RO, FR, IT, ES, DE)**")
            st.caption("AG/U/T: General | 12: Peste 12 ani | 15/16: Peste 15/16 ani | 18: Interzis minorilor")
            st.markdown("**🇬🇧 UK (BBFC)**")
            st.caption("U: General | PG: Parental Guidance | 12A/12: Peste 12 ani | 15: Peste 15 ani | 18: Adulti")
            
        with leg2:
            st.markdown("**🇺🇸 America (USA - MPAA / CA)**")
            st.caption("G: General | PG: Parental Guidance | PG-13: Peste 13 ani | R: Sub 17 cu adult | NC-17: 18+")
            st.markdown("**🇦🇺 Australia (ACB)**")
            st.caption("G: General | PG: Peste 12 recomandat | M: Peste 15 recomandat | MA15+: Restricționat 15+")

        with leg3:
            st.markdown("**🇯🇵 Japonia (EIRIN)**")
            st.caption("G: General | PG12: Peste 12 ani | R15+: Peste 15 ani | R18+: Peste 18 ani")
            st.markdown("**ℹ️ Notă Tehnică**")
            st.caption("Dacă apare N/A, datele nu au fost încă raportate în baza globală pentru acea regiune.")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("Nu am găsit acest film. Te rugăm să încerci titlul original în engleză dacă cel în română nu apare.")
