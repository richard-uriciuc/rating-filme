import streamlit as st
import requests

# --- CONFIGURARE ---
st.set_page_config(page_title="CineRating Intelligence Pro", page_icon="🎬", layout="wide")

# TOKEN-UL TĂU LUNG AICI
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN ULTRA-PREMIUM (FĂRĂ ERORI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Nunito', sans-serif;
        background-color: #f0f4f8;
    }

    .main-card {
        background: white;
        padding: 40px;
        border-radius: 35px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-top: 20px;
    }

    .movie-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #1a202c;
        line-height: 1;
        margin-bottom: 15px;
    }

    .rating-pill {
        background: #ffffff;
        border: 2px solid #edf2f7;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .rating-pill:hover {
        border-color: #3182ce;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(49, 130, 206, 0.1);
    }

    .rating-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2d3748;
        display: block;
    }

    .cnc-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        padding: 16px 32px;
        border-radius: 18px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2);
        margin-top: 20px;
        font-size: 1.1rem;
    }

    /* Stil pentru Legendă */
    .legend-box {
        background: #ffffff;
        padding: 25px;
        border-radius: 25px;
        border: 1px solid #e2e8f0;
        margin-top: 20px;
    }
    
    .symbol-bold {
        font-weight: 800;
        color: #3182ce;
        font-size: 1.1rem;
        display: inline-block;
        min-width: 65px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_movie_details(query):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    search_url = f"https://api.themoviedb.org/3/search/multi?query={query}&language=ro-RO"
    res = requests.get(search_url, headers=headers).json()
    
    if res.get('results'):
        best = sorted(res['results'], key=lambda x: x.get('popularity', 0), reverse=True)[0]
        m_id = best['id']
        m_type = best['media_type']
        details = requests.get(f"https://api.themoviedb.org/3/{m_type}/{m_id}?append_to_response=release_dates,content_ratings,credits&language=ro-RO", headers=headers).json()
        return details, m_type
    return None, None

# --- INTERFAȚA ---
st.markdown("<h1 style='text-align: center; font-weight: 800; color: #1a202c; padding-top: 30px;'>🎬 CineRating Intelligence</h1>", unsafe_allow_html=True)
query = st.text_input("", placeholder="Introdu numele unui film (ex: Back to the Future, Gladiator)...")

if query:
    data, m_type = get_movie_details(query)
    
    if data:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        col_img, col_txt = st.columns([1, 2.2])
        
        with col_img:
            st.image(f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}", use_container_width=True)
            # Link fix către Registrul CNC (pagina care conține PDF-ul găsit de tine)
            st.markdown(f'<center><a href="https://cnc.gov.ro/clasificare-filme-si-seriale-tv/" target="_blank" class="cnc-btn">📄 Registru Oficial CNC România</a></center>', unsafe_allow_html=True)

        with col_txt:
            st.markdown(f"<div class='movie-title'>{data.get('title', data.get('name'))}</div>", unsafe_allow_html=True)
            an = (data.get('release_date') or data.get('first_air_date', '----'))[:4]
            durata = f"{data.get('runtime')} min" if m_type == 'movie' else f"{data.get('number_of_seasons')} Sezoane"
            regie = "N/A"
            if 'credits' in data:
                regie = ", ".join([c['name'] for c in data['credits']['crew'] if c['job'] in ['Director', 'Executive Producer']][:1])
            
            st.markdown(f"<p style='color: #4a5568; font-size: 1.2rem; font-weight: 600;'>🗓️ {an}  •  ⏱️ {durata}  •  🎬 Regia: {regie}</p>", unsafe_allow_html=True)
            st.write(data.get('overview'))
            
            st.markdown("<h3 style='margin-top: 40px; font-weight: 800;'>🌍 Clasificări Globale</h3>", unsafe_allow_html=True)
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
                    st.markdown(f"""
                        <div class="rating-pill">
                            <div style="font-size: 0.8rem; color: #718096; font-weight: 700; text-transform: uppercase;">{tari[c_code]}</div>
                            <div class="rating-val">{val if val else 'N/A'}</div>
                        </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- LEGENDA PROFESIONALĂ (REPARATĂ) ---
        with st.expander("📖 Legenda Clasificărilor (Semnificație simboluri)"):
            st.markdown("<div class='legend-box'>", unsafe_allow_html=True)
            l1, l2, l3 = st.columns(3)
            
            with l1:
                st.markdown("#### 🇷🇴 România")
                st.markdown("<span class='symbol-bold'>AG</span> — Toate vârstele", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>AP-12</span> — Acordul părinților (sub 12)", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>N-15</span> — Nerecomandat sub 15 ani", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>18</span> — Interzis minorilor", unsafe_allow_html=True)
                
                st.markdown("#### 🇺🇸 USA / 🇨🇦 CA")
                st.markdown("<span class='symbol-bold'>G</span> — General", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>PG</span> — Parental Guidance", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>PG-13</span> — Peste 13 ani", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>R</span> — Restricționat", unsafe_allow_html=True)

            with l2:
                st.markdown("#### 🇪🇺 Europa (IT, ES, FR, DE)")
                st.markdown("<span class='symbol-bold'>T / U</span> — Toate vârstele", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>6 / 7</span> — Peste 6-7 ani", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>12 / 14</span> — Peste 12-14 ani", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>16 / 18</span> — Peste 16-18 ani", unsafe_allow_html=True)
                
                st.markdown("#### 🇬🇧 Marea Britanie")
                st.markdown("<span class='symbol-bold'>U</span> — Universal", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>PG</span> — Parental Guidance", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>12A</span> — Peste 12 ani", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>15 / 18</span> — Peste 15/18 ani", unsafe_allow_html=True)

            with l3:
                st.markdown("#### 🌏 Asia & Australia")
                st.markdown("<span class='symbol-bold'>G</span> — General", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>PG12</span> — Peste 12 recomandat", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>M / 15+</span> — Peste 15 recomandat", unsafe_allow_html=True)
                st.markdown("<span class='symbol-bold'>R18+</span> — Adult", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Nu am găsit rezultate. Verifică ortografia.")
