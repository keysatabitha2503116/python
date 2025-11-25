import streamlit as st
import math

# --- Konfigurasi Gaya & Header ---
st.set_page_config(
    page_title="Virtual Lab Bangun Ruang 3D",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOR_PRIMARY = "#20B2AA"  # Light Sea Green (Energi & Segar)
COLOR_ACCENT = "#FF69B4"   # Hot Pink (Menarik)
COLOR_TEXT = "#333333"
PHI = 3.14159 # Nilai pi

st.markdown(f"""
    <style>
    h1 {{color: {COLOR_PRIMARY}; text-align: center;}}
    .metric-box {{
        background-color: #F0F8FF; /* Alice Blue */
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_ACCENT};
        margin-bottom: 10px;
        height: 120px; /* Seragamkan tinggi kotak */
    }}
    .metric-box h4 {{color: {COLOR_TEXT}; margin-bottom: 5px;}}
    .stSlider {{
        font-size: 18px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🧊 Virtual Lab: Luas Permukaan & Volume Bangun Ruang")
st.markdown("Eksplorasi dimensi, Luas Permukaan (Lp), dan Volume (V) Kubus, Balok, dan Tabung.")

# --- Bagian 1: Input dan Pengaturan (Sidebar) ---
st.sidebar.header("⚙️ Pilih Bangun Ruang")

shape = st.sidebar.selectbox(
    "Pilih Bentuk 3D",
    ('Kubus', 'Balok', 'Tabung')
)

st.sidebar.markdown("---")
st.sidebar.subheader("Masukkan Dimensi")

Lp = 0
V = 0
image_url = ""
dimensi_dict = {}

# --- Logika Input dan Perhitungan ---

if shape == 'Kubus':
    s = st.sidebar.slider("Sisi (s)", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
    
    Lp = 6 * (s ** 2)
    V = s ** 3
    
    dimensi_dict = {'Sisi (s)': s}
    # URL Gambar Kubus (Placeholder, Streamlit tidak bisa render 3D secara native)
    image_url = "https://cdn-icons-png.flaticon.com/512/32/32386.png" 
    
    st.sidebar.markdown("##### Rumus:")
    st.sidebar.markdown(r"$\text{Lp} = 6 \cdot s^2$")
    st.sidebar.markdown(r"$\text{V} = s^3$")

elif shape == 'Balok':
    p = st.sidebar.slider("Panjang (p)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
    l = st.sidebar.slider("Lebar (l)", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
    t = st.sidebar.slider("Tinggi (t)", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
    
    Lp = 2 * (p * l + p * t + l * t)
    V = p * l * t
    
    dimensi_dict = {'Panjang (p)': p, 'Lebar (l)': l, 'Tinggi (t)': t}
    image_url = "https://cdn-icons-png.flaticon.com/512/32/32371.png"

    st.sidebar.markdown("##### Rumus:")
    st.sidebar.markdown(r"$\text{Lp} = 2(pl + pt + lt)$")
    st.sidebar.markdown(r"$\text{V} = p \cdot l \cdot t$")
    
elif shape == 'Tabung':
    r = st.sidebar.slider("Jari-jari (r)", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
    t = st.sidebar.slider("Tinggi (t)", min_value=1.0, max_value=10.0, value=6.0, step=0.5)
    
    Lp = 2 * PHI * r * (r + t)
    V = PHI * (r ** 2) * t
    
    dimensi_dict = {'Jari-jari (r)': r, 'Tinggi (t)': t}
    image_url = "https://cdn-icons-png.flaticon.com/512/32/32400.png"
    
    st.sidebar.markdown(f"##### Rumus (menggunakan π ≈ {PHI}):")
    st.sidebar.markdown(r"$\text{Lp} = 2\pi r (r + t)$")
    st.sidebar.markdown(r"$\text{V} = \pi r^2 t$")

# --- Bagian 2: Tampilan Hasil (Kolom Utama) ---
st.header(f"Bentuk yang Dipilih: {shape}")
st.markdown("---")

col_dimensi, col_perhitungan = st.columns([1, 2])

with col_dimensi:
    st.subheader("Dimensi")
    st.image(image_url, width=150)
    
    for key, value in dimensi_dict.items():
        st.markdown(f"**{key}:** `{value:.2f}` satuan")
    
    st.markdown("---")
    st.caption("Gambar di atas adalah representasi visual sederhana dari bentuk yang dipilih.")

with col_perhitungan:
    st.subheader("Hasil Perhitungan")
    
    # Tampilkan Luas Permukaan
    st.markdown(f'<div class="metric-box"><h4>Luas Permukaan (Lp):</h4> <h1>{Lp:.2f} satuan²</h1></div>', unsafe_allow_html=True)

    # Tampilkan Volume
    st.markdown(f'<div class="metric-box"><h4>Volume (V):</h4> <h1>{V:.2f} satuan³</h1></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 💡 Konsep Utama:")
    if Lp > 0:
        st.info(f"""
        * **Luas Permukaan:** Total area dari semua sisi yang membentuk bangun ruang. Dalam kasus {shape}, luasnya adalah **{Lp:.2f} satuan²**.
        * **Volume:** Jumlah ruang yang dapat diisi oleh bangun ruang tersebut. Dalam kasus {shape}, volumenya adalah **{V:.2f} satuan³**.
        """)

# --- Visualisasi Sederhana (Grafik) ---
# Untuk membuat lab ini lebih interaktif, kita akan memplot bagaimana Volume berubah 
# jika salah satu dimensi utama diubah (misalnya, Jari-jari untuk Tabung).

st.markdown("---")
st.header("📈 Analisis Perubahan Volume")

try:
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if shape == 'Kubus':
        x_label = "Sisi (s)"
        x_range = np.linspace(1, 10, 50)
        y_volume = x_range ** 3
        
    elif shape == 'Balok':
        x_label = "Panjang (p)"
        x_range = np.linspace(1, 10, 50)
        y_volume = x_range * l * t
        
    elif shape == 'Tabung':
        x_label = "Jari-jari (r)"
        x_range = np.linspace(0.1, 5, 50)
        y_volume = PHI * (x_range ** 2) * t
        
    ax.plot(x_range, y_volume, color=COLOR_ACCENT, linewidth=3)
    
    # Tandai titik saat ini
    current_x = dimensi_dict.get(list(dimensi_dict.keys())[0], 0)
    ax.plot(current_x, V, 'o', color=COLOR_PRIMARY, markersize=8, label='Nilai Saat Ini')
    
    ax.set_title(f"Hubungan antara {x_label} dan Volume {shape}")
    ax.set_xlabel(f"{x_label} (saat dimensi lain tetap)")
    ax.set_ylabel("Volume (V)")
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()
    
    st.pyplot(fig)

except Exception as e:
    st.error("Gagal membuat plot perubahan volume.")
