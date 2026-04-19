import streamlit as st

st.set_page_config(page_title="Expert System Gaming", page_icon="🎮")
st.title("🎮 Expert System: Rekomendasi Game Mobile")
st.write("Sistem ini menggunakan basis pengetahuan untuk mencocokkan spek dan preferensi kamu dengan game yang tepat.")

# --- SIDEBAR INPUT (USER INTERFACE) ---
st.sidebar.header("Kumpulkan Fakta")
f_spek = st.sidebar.selectbox("Spesifikasi HP:", ["Flagship", "Mid-range", "Kentang"])
f_dana = st.sidebar.radio("Model Bisnis:", ["Gratis (F2P)", "Berbayar (Premium)"])
f_mode = st.sidebar.radio("Mode Bermain:", ["Solo", "Party (Mabar)"])
f_genre = st.sidebar.selectbox("Genre Favorit:", ["Action", "MOBA", "RPG", "Strategy", "Casual"])
f_size = st.sidebar.selectbox("Kapasitas Memori Tersedia:", ["Kecil (< 2GB)", "Sedang (2-10GB)", "Besar (> 10GB)"])

# --- INFERENCE ENGINE ---
def inference_engine(spek, dana, mode, genre, size):
    # Logika Aturan (IF-THEN)
    if spek == "Kentang" and mode == "Party (Mabar)" and genre == "MOBA":
        return "Mobile Legends", "Ringan, stabil, dan komunitas mabar sangat besar untuk HP spek rendah."
    
    elif spek == "Flagship" and genre == "RPG" and size == "Besar (> 10GB)":
        return "Genshin Impact", "Grafik setara konsol butuh chipset flagship dan ruang penyimpanan yang sangat luas."
    
    elif spek == "Kentang" and genre == "Action" and mode == "Party (Mabar)":
        return "Free Fire", "Didesain khusus untuk kompetisi battle royale di perangkat dengan RAM terbatas."
    
    elif spek == "Mid-range" and genre == "Action" and mode == "Party (Mabar)":
        return "Call of Duty Mobile", "Keseimbangan antara grafik tajam dan performa untuk HP kelas menengah."
    
    elif dana == "Berbayar (Premium)" and genre == "RPG" and mode == "Solo":
        return "Stardew Valley", "Salah satu game premium RPG terbaik yang fokus pada pengalaman solo tanpa iklan."
    
    elif spek == "Flagship" and dana == "Berbayar (Premium)" and genre == "Action":
        return "Hitman Blood Money Reprisal", "Memerlukan performa tinggi untuk simulasi stealth yang kompleks."
    
    elif genre == "MOBA" and spek in ["Mid-range", "Flagship"] and mode == "Party (Mabar)":
        return "Honor of Kings / Wild Rift", "Visual lebih HD dan mekanik lebih dalam untuk perangkat yang lebih kuat."
    
    elif genre == "Casual" and size == "Kecil (< 2GB)":
        return "Subway Surfers", "Sangat ringan dan tidak butuh spek atau penyimpanan khusus."
    
    elif genre == "Strategy" and mode == "Party (Mabar)":
        return "Clash of Clans", "Game strategi mabar klasik yang bisa berjalan hampir di semua HP."
    
    elif genre == "Strategy" and mode == "Solo" and dana == "Berbayar (Premium)":
        return "Kingdom Rush Vengeance", "Strategi premium tanpa microtransactions yang mengganggu."
    
    elif size == "Besar (> 10GB)" and genre == "Action" and spek == "Flagship":
        return "Warzone Mobile", "Sangat berat karena render map besar secara real-time, butuh spek paling atas."
    
    elif genre == "RPG" and spek == "Kentang":
        return "Guardian Tales", "RPG bergaya pixel yang ringan namun memiliki cerita yang sangat mendalam."
    
    else:
        return "Roblox", "Platform universal yang menyediakan ribuan jenis game untuk segala kondisi fakta."

# --- OUTPUT (EXPLANATION FACILITY) ---
if st.button("Jalankan Sistem Pakar"):
    hasil, alasan = inference_engine(f_spek, f_dana, f_mode, f_genre, f_size)
    
    st.markdown("---")
    st.subheader("Keputusan Sistem:")
    st.success(f"**Rekomendasi: {hasil}**")
    
    st.info(f"**Analisis Pengetahuan:** {alasan}") # Fasilitas penjelasan 

st.markdown("---")
st.caption("Praktikum 2: Knowledge-Based System - STMIK AMIKOM Surakarta")