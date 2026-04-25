import streamlit as st
import requests

# --- CONFIGURARE ---
st.set_page_config(page_title="CineRating Intelligence Pro", page_icon="🎬", layout="wide")

# TOKEN-UL TĂU LUNG AICI
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN ULTRA-PREMIUM (CURĂȚAT DE ERORI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Nunito', sans-serif;
        background-color: #f4f7f9;
    }

    .main-card {
        background: white;
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 30px;
    }

    .movie-title {
        font-size: 3rem;
        font-weight: 800;
        color: #1a202c;
        line-height: 1.1;
    }

    .rating-pill {
        background: #ffffff;
        border: 2px solid #edf2f7;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }

    .rating-val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #2d3748;
    }

    .cnc-btn {
        background: #10b981;
        color: white !important;
        padding: 15px 30px;
        border-radius: 15px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }

    .legend-container {
        background: white;
        padding: 30px;
        border-radius: 30px;
        border: 1px solid #e2e8f0;
        margin-top: 10px;
    }

    .sym-bold {
        font-weight: 800;
        color: #3182ce;
        min-width: 70px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

def search_movie(query):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    url = f"https://api.themoviedb.org/3/search/multi?query={query}&language=ro-RO"
    res = requests.get(url, headers=headers).json()
    if res.get('results'):
        best = sorted(res['results'], key=lambda x: x.get('popularity', 0), reverse=True)[0]
        m_id, m_type = best['id'], best['media_type']
        details = requests.get(f"https://api.themoviedb.org/3/{m_type}/{m_id}?append_to_response=release_dates,content_ratings,credits&language=ro-RO", headers=headers).json()
        return details, m_type
    return None, None

# --- INTERFAȚĂ ---
st.markdown("<h1 style='text-align:center; font-weight:800;'>🎬 CineRating Intelligence</h1>", unsafe_allow_html=True)
query = st.text_input("", placeholder="Caută un film sau serial...", key="main_search")

if query:
    data, m_type = search_movie(query)
    if data:
        # --- ZONA FILM ---
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        c_img, c_txt = st.columns([1, 2.2])
        
        with c_img:
            st.image(f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}", use_container_width=True)
            # Link CNC re-actualizat
            st.markdown(f'<center><a href="https://cnc.gov.ro/clasificare-filme-si-seriale-tv/" target="_blank" class="cnc-btn">🔍 Verifică la CNC România</a></center>', unsafe_allow_html=True)

        with c_txt:
            st.markdown(f"<div class='movie-title'>{data.get('title', data.get('name'))}</div>", unsafe_allow_html=True)
            an = (data.get('release_date') or data.get('first_air_date', '----'))[:4]
            durata = f"{data.get('runtime')} min" if m_type == 'movie' else f"{data.get('number_of_seasons')} Sezoane"
            regie = ", ".join([c['name'] for c in data.get('credits',{}).get('crew',[]) if c['job'] in ['Director','Executive Producer']][:1])
            st.markdown(f"<p style='color:#718096; font-size:1.2rem;'>🗓️ {an}  •  ⏱️ {durata}  •  🎬 Regia: {regie}</p>", unsafe_allow_html=True)
            st.write(data.get('overview'))
            
            st.markdown("<h3 style='margin-top:30px; font-weight:800;'>🌍 Clasificări pe țări</h3>", unsafe_allow_html=True)
            tari = {'RO': '🇷🇴 RO', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 'FR': '🇫🇷 FR', 'DE': '🇩🇪 DE', 'IT': '🇮🇹 IT', 'ES': '🇪🇸 ES', 'CA': '🇨🇦 CA', 'AU': '🇦🇺 AU', 'JP': '🇯🇵 JP'}
            ratings = {}
            if m_type == 'movie':
                for r in data.get('release_dates', {}).get('results', []):
                    if r['iso_3166_1'] in tari: ratings[r['iso_3166_1']] = r['release_dates'][0]['certification']
            else:
                for r in data.get('content_ratings', {}).get('results', []):
                    if r['iso_3166_1'] in tari: ratings[r['iso_3166_1']] = r['rating']

            r_cols = st.columns(5)
            codes = list(tari.keys())
            for i in range(10):
                with r_cols[i % 5]:
                    c_code = codes[i]
                    val = ratings.get(c_code, "N/A")
                    st.markdown(f'<div class="rating-pill"><small style="color:#718096; font-weight:700;">{tari[c_code]}</small><br><span class="rating-val">{val if val else "N/A"}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- LEGENDA DESCHISĂ AUTOMAT ---
        st.markdown("<div class='legend-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-weight:800; margin-bottom:20px;'>📖 Semnificația simbolurilor</h3>", unsafe_allow_html=True)
        l1, l2, l3 = st.columns(3)
        
        with l1:
            st.markdown("#### 🇷🇴 România")
            st.markdown("<span class='sym-bold'>AG</span> — Toate vârstele", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>AP-12</span> — Acordul părinților (sub 12)", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>N-15</span> — Nerecomandat sub 15 ani", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>18</span> — Interzis minorilor", unsafe_allow_html=True)
            
            st.markdown("#### 🇺🇸 USA / 🇨🇦 Canada")
            st.markdown("<span class='sym-bold'>G</span> — General", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>PG</span> — Parental Guidance", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>PG-13</span> — Peste 13 ani", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>R</span> — Restricționat", unsafe_allow_html=True)

        with l2:
            st.markdown("#### 🇪🇺 Europa (IT, ES, FR, DE)")
            st.markdown("<span class='sym-bold'>T / U</span> — Toate vârstele", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>6 / 7</span> — Peste 6-7 ani", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>12 / 14</span> — Peste 12-14 ani", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>16 / 18</span> — Peste 16-18 ani", unsafe_allow_html=True)
            
            st.markdown("#### 🇬🇧 Marea Britanie")
            st.markdown("<span class='sym-bold'>U</span> — Universal", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>PG</span> — Parental Guidance", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>12A</span> — Peste 12 ani", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>15 / 18</span> — Peste 15/18 ani", unsafe_allow_html=True)

        with l3:
            st.markdown("#### 🌏 Asia & Australia")
            st.markdown("<span class='sym-bold'>G</span> — General", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>PG12</span> — Peste 12 recomandat", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>M / 15+</span> — Peste 15 recomandat", unsafe_allow_html=True)
            st.markdown("<span class='sym-bold'>R18+</span> — Adult", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Film negăsit. Încearcă un alt nume.")
