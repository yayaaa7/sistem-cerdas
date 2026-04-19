import streamlit as st

# Bagian Header Aplikasi
st.title("📱 Sistem Rekomendasi HP Sederhana")
st.write("Sistem Cerdas berbasis Rule (IF-ELSE)")

# Pilihan Input dari Pengguna
budget = st.selectbox(
    "Pilih Budget Anda:",
    ["< 5 juta", "5 - 10 juta", "> 10 juta"]
)

kebutuhan = st.selectbox(
    "Pilih Kebutuhan Utama:",
    ["Kamera", "Gaming"]
)

# Tombol untuk mengeksekusi logika sistem cerdas
if st.button("Dapatkan Rekomendasi"):
    
    # --- LOGIKA IF-ELSE ---
    if budget == "< 5 juta":
        if kebutuhan == "Kamera":
            st.success("Rekomendasi: Fokus pada HP dengan resolusi kamera baik dan fitur OIS. Contoh: Samsung Galaxy A36 dan Redmi Note 15 Pro.")
        elif kebutuhan == "Gaming":
            st.success("Rekomendasi: Cari chipset kencang di kelasnya (seperti Mediatek Dimensity atau Snapdragon 7 series). Contoh: POCO X7 pro dan IQOO Neo 10")
            
    elif budget == "5 - 10 juta":
        if kebutuhan == "Kamera":
            st.success("Rekomendasi: Mid-range ke atas dengan kualitas kamera setara flagship. Contoh: Vivo V70, Xiaomi 15T, Samsung Galaxy S25 FE, atau iPhone 13/14/15.")
        elif kebutuhan == "Gaming":
            st.success("Rekomendasi: HP performa tinggi alias 'Flagship Killer'. Contoh: POCO F7, iQOO 15R, Realme GT7 atau Xiaomi 15T pro.")
            
    elif budget == "> 10 juta":
        if kebutuhan == "Kamera":
            st.success("Rekomendasi: HP Flagship premium dengan lensa periskop dan komputasi AI terbaik. Contoh: Samsung Galaxy S26 Ultra, iPhone 17 Pro Max, atau Vivo X300 Pro.")
        elif kebutuhan == "Gaming":
            st.success("Rekomendasi: HP khusus gaming atau flagship super kencang dengan sistem pendingin mumpuni. Contoh: ROG Phone 9, RedMagic 9 Pro, atau iPhone 17 Pro Max.")