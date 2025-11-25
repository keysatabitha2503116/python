import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Gaya & Header ---
st.set_page_config(
    page_title="Virtual Lab Fungsi Eksponensial",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOR_PRIMARY = "#8A2BE2"  # Blue Violet
COLOR_ACCENT = "#FFA500"   # Orange
COLOR_TEXT = "#333333"

st.markdown(f"""
    <style>
    h1 {{color: {COLOR_PRIMARY}; text-align: center;}}
    .metric-box {{
        background-color: #F0F8FF; /* Alice Blue */
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_ACCENT};
        margin-bottom: 10px;
    }}
    .stSlider {{
        font-size: 18px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Lab: Fungsi Eksponensial $f(x) = c \cdot a^x$")
st.markdown("Eksplorasi Peran Basis ($a$) dan Koefisien ($c$) dalam Grafik Fungsi Eksponensial.")

# --- Bagian 1: Input dan Pengaturan (Sidebar) ---
st.sidebar.header("⚙️ Pengaturan Fungsi")

# Input Basis (a)
st.sidebar.subheader("1. Basis Eksponen (a)")
a = st.sidebar.slider(
    "Pilih nilai basis a (a > 0, a ≠ 1)",
    min_value=0.1,
    max_value=3.0,
    value=1.5,
    step=0.1,
    key="basis_a"
)

# Input Koefisien (c)
st.sidebar.subheader("2. Koefisien (c)")
c = st.sidebar.slider(
    "Pilih nilai koefisien c (c ≠ 0)",
    min_value=-2.0,
    max_value=2.0,
    value=1.0,
    step=0.1,
    key="koefisien_c"
)

# Fungsi Matematika
def f(x, a, c):
    """Menghitung f(x) = c * a^x"""
    return c * (a ** x)

# --- Bagian 2: Visualisasi Grafik ---
col_viz, col_info = st.columns([2, 1])

with col_viz:
    st.header("📈 Grafik Fungsi Eksponensial")

    # Buat Plot Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))

    # Batas X dan Y
    x_vals = np.linspace(-4, 4, 400)
    y_vals = f(x_vals, a, c)

    # Plot fungsi
    ax.plot(x_vals, y_vals, label=f'$f(x) = {c:.1f} \cdot {a:.1f}^x$', color=COLOR_PRIMARY, linewidth=3)
    
    # Plot Garis Asimtot Horizontal (y=0)
    ax.axhline(0, color=COLOR_ACCENT, linestyle='--', label='Asimtot y=0')

    # Pengaturan Grid dan Axis
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle=':', alpha=0.7)
    
    # Label Axis dan Title
    ax.set_xlabel("x")
