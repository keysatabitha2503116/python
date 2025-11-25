import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Konfigurasi Gaya & Header ---
st.set_page_config(
    page_title="Virtual Lab Statistika Dasar",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOR_PRIMARY = "#8B008B"  # Dark Magenta (Elegan)
COLOR_ACCENT = "#FFD700"   # Gold (Aksen)
COLOR_TEXT = "#333333"

st.markdown(f"""
    <style>
    h1 {{color: {COLOR_PRIMARY}; text-align: center;}}
    .metric-box {{
        background-color: #F8F8FF; /* Ghost White */
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_ACCENT};
        margin-bottom: 10px;
        height: 120px;
    }}
    .stTextArea, .stButton {{
        font-size: 18px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Virtual Lab: Statistik Deskriptif & Visualisasi")
st.markdown("Eksplorasi Mean, Median, Modus, dan Distribusi Data.")

# --- Fungsi Perhitungan Statistik ---

def calculate_mode(data_list):
    """Menghitung modus (bisa lebih dari satu)."""
    if not data_list:
        return "N/A"
    
    counts = {}
    for item in data_list:
        counts[item] = counts.get(item, 0) + 1
    
    max_count = max(counts.values())
    modes = [key for key, value in counts.items() if value == max_count]
    
    return ", ".join(map(str, modes)) if modes else "N/A"

# --- Bagian 1: Input Data ---
col_input, col_example = st.columns([2, 1])

with col_input:
    st.subheader("1. Masukkan Data Numerik")
    st.info("Pisahkan angka dengan koma atau spasi. Contoh: 5, 8, 12, 12, 15")
    
    data_input = st.text_area(
        "Data Anda:",
        "5, 8, 12, 12, 15, 17, 20, 21, 25, 30, 30, 30",
        height=100
    )

with col_example:
    st.subheader("Contoh Data")
    if st.button("Data Nilai Ujian"):
        data_input = "70, 75, 80, 80, 85, 90, 90, 90, 95, 100"
        st.session_state.data_input_key = data_input
        st.experimental_rerun()
    if st.button("Data Gaji (Jutaan)"):
        data_input = "3, 3, 4, 5, 6, 7, 10, 15"
        st.session_state.data_input_key = data_input
        st.experimental_rerun()


# Parsing Data
try:
    # Mengganti koma dengan spasi, lalu memisahkan berdasarkan spasi
    data_list_str = data_input.replace(',', ' ').split()
    data = [float(item) for item in data_list_str if item.strip()]
    data.sort() # Urutkan untuk median
    is_valid = bool(data)
except Exception:
    data = []
    is_valid = False

# --- Bagian 2: Hasil Perhitungan ---
st.markdown("---")
st.header("2. Hasil Statistik Deskriptif")

if is_valid:
    data_np = np.array(data)
    
    # Perhitungan
    n = len(data)
    mean = np.mean(data_np)
    median = np.median(data_np)
    mode = calculate_mode(data)
    range_data = np.max(data_np) - np.min(data_np)
    std_dev = np.std(data_np)

    col_mean, col_median, col_mode, col_range, col_std = st.columns(5)
    
    with col_mean:
        st.markdown(f'<div class="metric-box"><h4>Mean (Rata-rata):</h4> <h3>{mean:.2f}</h3></div>', unsafe_allow_html=True)
    with col_median:
        st.markdown(f'<div class="metric-box"><h4>Median (Nilai Tengah):</h4> <h3>{median:.2f}</h3></div>', unsafe_allow_html=True)
    with col_mode:
        st.markdown(f'<div class="metric-box"><h4>Modus (Nilai Sering Muncul):</h4> <h3>{mode}</h3></div>', unsafe_allow_html=True)
    with col_range:
        st.markdown(f'<div class="metric-box"><h4>Jangkauan (Range):</h4> <h3>{range_data:.2f}</h3></div>', unsafe_allow_html=True)
    with col_std:
        st.markdown(f'<div class="metric-box"><h4>Std Deviasi (Sebaran):</h4> <h3>{std_dev:.2f}</h3></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Penjelasan Konsep
    st.subheader("💡 Interpretasi Sentral Tendensi")
    st.info(f"""
    * **Mean:** Rata-rata hitung data. Sering dipengaruhi oleh nilai ekstrem (outlier).
    * **Median:** Nilai tengah setelah data diurutkan. Lebih stabil terhadap outlier.
    * **Modus:** Nilai yang paling sering muncul. Berguna untuk data kategorikal atau melihat puncak distribusi.
    """)

    # --- Bagian 3: Visualisasi Data ---
    st.header("3. Visualisasi Distribusi Data")
    
    vis_type = st.selectbox(
        "Pilih Jenis Grafik",
        ('Histogram', 'Box Plot (Diagram Kotak Garis)')
    )
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if vis_type == 'Histogram':
        bins = st.slider("Jumlah Kelas (Bins) Histogram", min_value=3, max_value=15, value=5)
        ax.hist(data_np, bins=bins, edgecolor='black', color=COLOR_PRIMARY, alpha=0.7)
        ax.set_title("Histogram Data")
        ax.set_xlabel("Nilai Data")
        ax.set_ylabel("Frekuensi")
        ax.axvline(mean, color=COLOR_ACCENT, linestyle='dashed', linewidth=2, label=f'Mean: {mean:.2f}')
        ax.axvline(median, color=COLOR_PRIMARY, linestyle='dotted', linewidth=2, label=f'Median: {median:.2f}')
        ax.legend()
        st.caption("Histogram menunjukkan bentuk dan sebaran data. Mean dan Median ditandai.")

    elif vis_type == 'Box Plot (Diagram Kotak Garis)':
        ax.boxplot(data_np, vert=False, patch_artist=True, 
                   boxprops=dict(facecolor=COLOR_PRIMARY, alpha=0.5), 
                   medianprops=dict(color=COLOR_ACCENT, linewidth=2))
        ax.set_title("Box Plot Data")
        ax.set_xlabel("Nilai Data")
        st.caption("Box Plot menunjukkan kuartil (Q1, Q2/Median, Q3) dan potensi outlier.")
    
    st.pyplot(fig)
    plt.close(fig) # Penting untuk membebaskan memori
    
else:
    st.warning("Mohon masukkan data numerik yang valid di kolom input.")


st.markdown("---")
st.caption("Dibuat dengan Python Streamlit untuk pembelajaran Statistika Interaktif.")
