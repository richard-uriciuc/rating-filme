import streamlit as st
import requests

# --- CONFIGURARE ---
st.set_page_config(page_title="CineRating Intelligence", page_icon="🎬", layout="wide")

# TOKEN-UL TĂU LUNG AICI
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Nunito', sans-serif; background-color: #f4f7f9; }
    .main-card { background: white; padding: 40px; border-radius: 30px; box-shadow: 0 15px 40px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }
    .movie-title { font-size: 3rem; font-weight: 800; color: #1a202c; line-height: 1.1; }
    .rating-pill { background: #ffffff; border: 2px solid #edf2f7; border-radius: 20px; padding: 15px; text-align: center; margin-bottom: 10px; }
    .rating-val { font-size: 1.7rem; font-weight: 800; color: #2d3748; }
    .cnc-btn { background: #10b981; color: white !important; padding: 15px 30px; border-radius: 15px; text-decoration: none; font-weight: 700; display: inline-block; margin-top: 20px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2); }
    .disclaimer-box { background-color: #fff5f5; border-left: 6px solid #feb2b2; padding: 15px; border-radius: 10px; color: #c53030; margin-bottom: 20px; font-size: 0.95rem; line-height: 1.5; }
    .sym-bold { font-weight: 800; color: #3182ce; min-width: 75px; display: inline-block; }
    .legend-card { background: white; padding: 30px; border-radius: 30px; border: 1px solid #e2e8f0; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

def search_movie(query):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&language=ro-RO"
    res = requests.get(url, headers=headers).json()
    if res.get('results'):
        best = sorted(res['results'], key=lambda x: x.get('popularity', 0), reverse=True)[0]
        m_id = best['id']
        details = requests.get(f"https://api.themoviedb.org/3/movie/{m_id}?append_to_response=release_dates,credits&language=ro-RO", headers=headers).json()
        return details
    return None

# --- UI ---
st.markdown("<h1 style='text-align:center; font-weight:800; padding: 20px;'>🎬 CineRating Intelligence</h1>", unsafe_allow_html=True)
query = st.text_input("", placeholder="Scrie numele filmului (ex: Fălci, Gladiatorul)...", key="search")

if query:
    data = search_movie(query)
    if data:
        # DISCLAIMER
        st.markdown("""
            <div class="disclaimer-box">
                ⚠️ <b>NOTĂ IMPORTANTĂ:</b> Datele pentru România (RO) sunt preluate din baze de date globale și pot conține erori. 
                Dacă observați clasificări neobișnuite (ex: '18' la filme de aventură), vă rugăm să <b>comparați cu USA/UK</b> 
                sau să accesați <b>Registrul Oficial CNC</b> de mai jos.
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        c_img, c_txt = st.columns([1, 2.2])
        
        with c_img:
            st.image(f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}", use_container_width=True)
            # LINK-UL TĂU PDF DIRECT
            st.markdown(f'''
                <center>
                    <a href="https://cnc.gov.ro/wp-content/uploads/2026/04/1-filme_21_Apr.pdf" target="_blank" class="cnc-btn">
                        📄 Tabel Oficial CNC (PDF)
                    </a>
                </center>
            ''', unsafe_allow_html=True)

        with c_txt:
            st.markdown(f"<div class='movie-title'>{data.get('title')}</div>", unsafe_allow_html=True)
            an = (data.get('release_date') or '----')[:4]
            durata = f"{data.get('runtime')} min"
            regie = ", ".join([c['name'] for c in data.get('credits',{}).get('crew',[]) if c['job'] == 'Director'][:1])
            st.markdown(f"<p style='color:#718096; font-size:1.2rem;'>🗓️ {an}  •  ⏱️ {durata}  •  🎬 Regia: {regie}</p>", unsafe_allow_html=True)
            st.write(data.get('overview'))
            
            st.markdown("<h3 style='margin-top:30px; font-weight:800;'>🌍 Clasificări pe țări</h3>", unsafe_allow_html=True)
            tari = {'RO': '🇷🇴 RO', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 'FR': '🇫🇷 FR', 'DE': '🇩🇪 DE', 'IT': '🇮🇹 IT', 'ES': '🇪🇸 ES', 'CA': '🇨🇦 CA', 'AU': '🇦🇺 AU', 'JP': '🇯🇵 JP'}
            
            ratings = {}
            for r in data.get('release_dates', {}).get('results', []):
                if r['iso_3166_1'] in tari:
                    ratings[r['iso_3166_1']] = r['release_dates'][0]['certification']

            r_cols = st.columns(5)
            codes = list(tari.keys())
            for i in range(10):
                with r_cols[i % 5]:
                    c_code = codes[i]
                    val = ratings.get(c_code, "N/A")
                    st.markdown(f'<div class="rating-pill"><small style="color:#718096; font-weight:700;">{tari[c_code]}</small><br><span class="rating-val">{val if val else "N/A"}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # LEGENDA DESCHISĂ
        st.markdown("<div class='legend-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-weight:800; margin-bottom:20px;'>📖 Semnificația simbolurilor</h3>", unsafe_allow_html=True)
        l1, l2, l3 = st.columns(3)
        with l1:
            st.markdown("#### 🇷🇴 RO / 🇺🇸 USA")
            st.markdown("<span class='sym-bold'>AG/G</span> — Toate vârstele<br><span class='sym-bold'>AP-12/PG</span> — Acord părinți<br><span class='sym-bold'>N-15/P13</span> — Peste 13-15 ani<br><span class='sym-bold'>18/R</span> — Restricționat", unsafe_allow_html=True)
        with l2:
            st.markdown("#### 🇪🇺 Europa")
            st.markdown("<span class='sym-bold'>T / U</span> — Toate vârstele<br><span class='sym-bold'>6 / 7</span> — Peste 6-7 ani<br><span class='sym-bold'>12 / 14</span> — Peste 12-14 ani<br><span class='sym-bold'>16 / 18</span> — Peste 16-18 ani", unsafe_allow_html=True)
        with l3:
            st.markdown("#### 🇬🇧 UK / 🌏 Asia")
            st.markdown("<span class='sym-bold'>U</span> — Universal<br><span class='sym-bold'>12A/PG12</span> — Peste 12 ani<br><span class='sym-bold'>15/R15+</span> — Peste 15 ani<br><span class='sym-bold'>18/R18+</span> — Adult", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Film negăsit. Verificați titlul.")
