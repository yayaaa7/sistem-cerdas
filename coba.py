import streamlit as st
import pandas as pd
import numpy as np

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Sistem Pakar Nutrisi - Certainty Factor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# 1. LOAD DATASET
# ----------------------------------------------------
@st.cache_data
def load_data():
    # Membaca dataset dari direktori yang sama
    nutrition = pd.read_csv('standard-nutrition.csv')
    foods = pd.read_csv('foods.csv')
    # Membersihkan kolom Unnamed jika ada
    if 'Unnamed: 0' in nutrition.columns:
        nutrition = nutrition.drop(columns=['Unnamed: 0'])
    if 'Unnamed: 0' in foods.columns:
        foods = foods.drop(columns=['Unnamed: 0'])
    return nutrition, foods

try:
    nutrition_df, foods_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat file dataset. Pastikan 'standard-nutrition.csv' dan 'foods.csv' berada di folder yang sama. Error: {e}")
    st.stop()

# ----------------------------------------------------
# 2. DATA GEJALA & BOBOT PAKAR
# ----------------------------------------------------
# Basis pengetahuan yang menghubungkan gejala medis dengan kekurangan zat gizi tertentu
SYMPTOMS = [
    {"id": "G01", "nama": "Kelelahan ekstrem dan lemas terus-menerus", "nutrisi": "Energy (kJ)", "cf_pakar": 0.8},
    {"id": "G02", "nama": "Penurunan berat badan drastis tanpa sebab jelas", "nutrisi": "Energy (kJ)", "cf_pakar": 0.7},
    {"id": "G03", "nama": "Pertumbuhan tinggi badan terhambat / Gejala Stunting", "nutrisi": "Protein (g)", "cf_pakar": 0.9},
    {"id": "G04", "nama": "Sistem kekebalan tubuh sangat lemah / mudah tertular penyakit", "nutrisi": "Protein (g)", "cf_pakar": 0.6},
    {"id": "G05", "nama": "Kulit terasa sangat kering, kusam, dan bersisik", "nutrisi": "Fat (g)", "cf_pakar": 0.7},
    {"id": "G06", "nama": "Sering mengalami sembelit atau susah buang air besar (BAB)", "nutrisi": "Dietary Fiber (g)", "cf_pakar": 0.8},
    {"id": "G07", "nama": "Rabun senja / kesulitan melihat jelas pada malam hari", "nutrisi": "Vitamin A (mg)", "cf_pakar": 0.9},
    {"id": "G08", "nama": "Gejala penyakit Beri-beri atau pembengkakan abnormal pada kaki", "nutrisi": "Vitamin B1 (mg)", "cf_pakar": 0.85},
    {"id": "G09", "nama": "Kelemahan otot yang disertai dengan sering kesemutan", "nutrisi": "Vitamin B1 (mg)", "cf_pakar": 0.6},
    {"id": "G10", "nama": "Radang, pecah-pecah, atau luka di sudut bibir (Sariawan sudut mulut)", "nutrisi": "Vitamin B2 (mg)", "cf_pakar": 0.8},
    {"id": "G11", "nama": "Gusi mudah berdarah atau sariawan parah yang meluas (Skorbut)", "nutrisi": "Vitamin C (mg)", "cf_pakar": 0.9},
    {"id": "G12", "nama": "Mudah pusing berputar, dehidrasi ringan, dan badan terasa limbung", "nutrisi": "Sodium (mg)", "cf_pakar": 0.7},
    {"id": "G13", "nama": "Detak jantung tidak teratur atau sering berdebar-debar (Aritmia)", "nutrisi": "Potassium (mg)", "cf_pakar": 0.8},
    {"id": "G14", "nama": "Kerapuhan tulang atau gejala pengeroposan tulang (Osteoporosis)", "nutrisi": "Calcium (mg)", "cf_pakar": 0.85},
    {"id": "G15", "nama": "Sering mengalami kram atau kejang otot secara mendadak", "nutrisi": "Magnesium (mg)", "cf_pakar": 0.75},
    {"id": "G16", "nama": "Gigi dan tulang terasa rapuh, keropos, atau mudah patah", "nutrisi": "Phosphorus (mg)", "cf_pakar": 0.7},
    {"id": "G17", "nama": "Anemia parah (pucat, lesu, mata berkunang-kunang)", "nutrisi": "Iron (mg)", "cf_pakar": 0.8},
    {"id": "G18", "nama": "Luka luar pada tubuh yang sangat lambat sembuh atau mengering", "nutrisi": "Zinc (mg)", "cf_pakar": 0.8}
]

# Pilihan tingkat keyakinan user
KEYAKINAN_OPTIONS = {
    0.0: "0.0 | Tidak Tahu / Tidak Mengalami",
    0.2: "0.2 | Sedikit Yakin",
    0.4: "0.4 | Cukup Yakin",
    0.6: "0.6 | Yakin",
    0.8: "0.8 | Sangat Yakin",
    1.0: "1.0 | Pasti / Sangat Pasti"
}

# ----------------------------------------------------
# 3. MANAJEMEN SESSION STATE & LOGIN (HALAMAN 1)
# ----------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔒 Login Sistem Pakar Nutrisi</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Gunakan akun default berikut untuk mencoba:<br><b>Username:</b> admin | <b>Password:</b> admin123</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Masuk Aplikasi", use_container_width=True)
            
            if submitted:
                if username == "admin" and password == "admin123":
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success("Login Berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah. Silakan periksa kembali.")

# ----------------------------------------------------
# 4. HALAMAN 2: DASHBOARD / BERANDA
# ----------------------------------------------------
def dashboard_page():
    st.title("🏠 Dashboard & Ringkasan Data")
    st.markdown("Selamat datang di **Sistem Pakar Diagnosis Defisiensi Nutrisi**. Sistem ini memproses gejala klinis Anda menggunakan metode penalaran *Certainty Factor* (Faktor Kepastian) untuk menyimpulkan jenis zat gizi yang kurang dalam tubuh Anda.")
    
    st.markdown("---")
    # Tampilkan Metrik Penting
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Nutrisi Standar Dipantau", value=f"{len(nutrition_df)} Jenis")
    with col2:
        st.metric(label="Total Menu Makanan di Database", value=f"{len(foods_df)} Menu")
    with col3:
        st.metric(label="Total Gejala dalam Aturan Pakar", value=f"{len(SYMPTOMS)} Gejala")
        
    st.markdown("---")
    
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("📋 Sekilas Data Nutrisi Standar")
        st.dataframe(nutrition_df[['Nutrisi', 'Fungsi Zat', 'Rekomendasi Harian Anak (1-5 tahun)']].head(5), use_container_width=True)
    with col5:
        st.subheader("🍲 Sekilas Data Menu Makanan")
        st.dataframe(foods_df[['Menu', 'Energy (kJ)', 'Protein (g)', 'Fat (g)', 'Carbohydrates (g)']].head(5), use_container_width=True)

# ----------------------------------------------------
# 5. HALAMAN 3: DIAGNOSIS CERTAINTY FACTOR
# ----------------------------------------------------
def diagnosis_page():
    st.title("🧠 Sistem Pakar Diagnosis Defisiensi Nutrisi")
    st.markdown("Silakan pilih tingkat keyakinan Anda untuk masing-masing gejala di bawah ini sesuai dengan kondisi tubuh saat ini.")
    
    user_inputs = {}
    
    st.subheader("Masukkan Kondisi Gejala Anda:")
    
    # Bagi form gejala menjadi dua kolom agar rapi
    col1, col2 = st.columns(2)
    
    for idx, sym in enumerate(SYMPTOMS):
        # Distribusikan gejala secara seimbang ke kolom 1 dan kolom 2
        with col1 if idx % 2 == 0 else col2:
            choice = st.selectbox(
                f"[{sym['id']}] {sym['nama']}",
                options=list(KEYAKINAN_OPTIONS.keys()),
                format_func=lambda x: KEYAKINAN_OPTIONS[x],
                key=f"sym_{sym['id']}"
            )
            user_inputs[sym['id']] = choice
            
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Proses Diagnosis Pakar", type="primary", use_container_width=True):
        # Mengelompokkan gejala berdasarkan zat nutrisi
        grouped_cf = {}
        for sym in SYMPTOMS:
            nutrisi = sym['nutrisi']
            cf_user = user_inputs[sym['id']]
            
            if cf_user > 0:
                # Rumus CF Gejala Tunggal: CF[H,E] = CF[E] * CF[Pakar]
                cf_gejala = cf_user * sym['cf_pakar']
                if nutrisi not in grouped_cf:
                    grouped_cf[nutrisi] = []
                grouped_cf[nutrisi].append(cf_gejala)
                
        if not grouped_cf:
            st.warning("⚠️ Anda tidak memilih gejala apa pun. Silakan ubah tingkat keyakinan pada beberapa gejala di atas.")
            return
            
        # Kombinasikan nilai CF untuk nutrisi yang memiliki gejala lebih dari satu
        final_results = []
        for nutrisi, cf_list in grouped_cf.items():
            cf_comb = cf_list[0]
            for next_cf in cf_list[1:]:
                # Rumus CF Kombinasi: CF_comb = CF_old + CF_new * (1 - CF_old)
                cf_comb = cf_comb + next_cf * (1 - cf_comb)
            final_results.append({'nutrisi': nutrisi, 'cf': cf_comb})
            
        # Urutkan dari nilai CF tertinggi
        final_results = sorted(final_results, key=lambda x: x['cf'], reverse=True)
        
        st.markdown("---")
        st.subheader("📊 Hasil Urutan Kepastian Diagnosis")
        
        # Buat dataframe hasil diagnosis untuk grafik
        res_df = pd.DataFrame(final_results)
        res_df = res_df.rename(columns={'nutrisi': 'Zat Nutrisi', 'cf': 'Faktor Kepastian (CF)'})
        
        # Tampilkan grafik batang terurut
        st.bar_chart(res_df.set_index('Zat Nutrisi'))
        
        # Ambil diagnosis tertinggi
        top_diagnosis = final_results[0]
        top_nutrisi = top_diagnosis['nutrisi']
        top_cf_pct = top_diagnosis['cf'] * 100
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.success(f"### 🎉 Diagnosis Utama: Kekurangan **{top_nutrisi}** dengan tingkat kepastian **{top_cf_pct:.2f}%**")
        
        # Ambil detail informasi dari nutrition_df
        detail_row = nutrition_df[nutrition_df['Nutrisi'] == top_nutrisi]
        if not detail_row.empty:
            detail = detail_row.iloc[0]
            st.markdown(f"**💡 Fungsi Zat Nutrisi:** {detail['Fungsi Zat']}")
            st.markdown(f"**⚠️ Dampak Jika Kekurangan Akut:** {detail['Dampak Kekurangan']}")
            st.markdown(f"**👶 Rekomendasi Harian Anak (1-5 tahun):** {detail['Rekomendasi Harian Anak (1-5 tahun)']}")
            
        # Rekomendasi Makanan Tertinggi Berdasarkan Dataset foods.csv
        st.markdown("---")
        st.subheader(f"🍲 Rekomendasi 5 Makanan Tertinggi Kandungan {top_nutrisi}")
        st.markdown("Berikut adalah daftar menu makanan dari database yang sangat disarankan untuk dikonsumsi guna memulihkan defisiensi zat gizi tersebut:")
        
        # Ambil makanan dengan nilai kandungan gizi tertinggi
        recommended_foods = foods_df.sort_values(by=top_nutrisi, ascending=False).head(5)
        st.dataframe(recommended_foods[['Menu', top_nutrisi]], use_container_width=True)

# ----------------------------------------------------
# 6. HALAMAN 4: DATA NUTRISI STANDAR
# ----------------------------------------------------
def nutrition_page():
    st.title("📊 Tabel Standar Nutrisi Anak & Dampak Medis")
    st.markdown("Halaman ini menyajikan acuan ambang batas kebutuhan gizi harian anak beserta dampak medis kekurangan maupun kelebihan gizi.")
    
    search_query = st.text_input("🔍 Cari Zat Nutrisi berdasarkan nama:")
    
    filtered_df = nutrition_df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['Nutrisi'].str.contains(search_query, case=False, na=False)]
        
    st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# 7. HALAMAN 5: DATA REKOMENDASI MAKANAN
# ----------------------------------------------------
def foods_page():
    st.title("🍲 Eksplorasi Kandungan Gizi Menu Makanan")
    st.markdown("Gunakan halaman ini untuk melihat nilai nutrisi lengkap dari berbagai menu makanan yang tersedia pada database.")
    
    col1, col2 = st.columns(2)
    with col1:
        search_food = st.text_input("🔍 Cari nama menu makanan:")
    with col2:
        selected_sort = st.selectbox("Sortir Berdasarkan Kandungan Nutrisi Tertinggi:", nutrition_df['Nutrisi'].tolist())
        
    display_df = foods_df.copy()
    if search_food:
        display_df = display_df[display_df['Menu'].str.contains(search_food, case=False, na=False)]
        
    display_df = display_df.sort_values(by=selected_sort, ascending=False)
    
    st.dataframe(display_df[['Menu', selected_sort] + [col for col in display_df.columns if col not in ['Menu', selected_sort]]], use_container_width=True)

# ----------------------------------------------------
# 8. HALAMAN 6: TENTANG & BANTUAN TEORI
# ----------------------------------------------------
def about_page():
    st.title("ℹ️ Tentang Sistem & Landasan Teori")
    
    st.subheader("📐 Metode Certainty Factor (Faktor Kepastian)")
    st.markdown(
        """
        Metode *Certainty Factor* (CF) diperkenalkan oleh Shortliffe Buchanan pada tahun 1975 untuk mengakomodasi nilai ketidakpastian pemikiran dari seorang pakar medis.
        
        Formula dasar penentuan nilai kepastian gejala tunggal adalah:
        """
    )
    st.latex(r"CF(H, E) = CF(E) \times CF(Pakar)")
    st.markdown(
        """
        Dimana:
        - $CF(E)$ adalah tingkat keyakinan gejala yang diinput oleh pengguna.
        - $CF(Pakar)$ adalah bobot derajat keyakinan baku yang ditentukan oleh seorang pakar.
        
        Apabila terdapat lebih dari satu gejala yang mengarah pada kesimpulan defisiensi gizi yang sama, maka nilai-nilai kepastian tersebut akan digabungkan secara sekuensial memakai formula kombinasi berikut:
        """
    )
    st.latex(r"CF_{combine}(CF_{old}, CF_{new}) = CF_{old} + CF_{new} \times (1 - CF_{old})")
    
    st.markdown("---")
    st.subheader("👨‍💻 Informasi Aplikasi")
    st.markdown(
        """
        - **Teknologi**: Python, Streamlit Framework, Pandas Dataframes.
        - **Sumber Data**: Dataset Standar Nutrisi Anak (1-5 tahun) & Database Kandungan Gizi Menu Makanan Lokal.
        - **Cara Penggunaan**: Masuk ke halaman **Diagnosis**, isi indikasi gejala fisik tubuh Anda, klik tombol hitung, dan sistem akan langsung merekomendasikan bahan pangan terbaik untuk memulihkan gizi Anda.
        """
    )

# ----------------------------------------------------
# 9. PENGATUR ROUTING SELEKSI HALAMAN (SIDEBAR NAV)
# ----------------------------------------------------
if not st.session_state['logged_in']:
    login_page()
else:
    # Sidebar Kontrol Menu Navigasi setelah Login Sukses
    st.sidebar.title("🧭 Navigasi Menu")
    current_page = st.sidebar.radio(
        "Pilih Halaman Aplikasi:",
        [
            "🏠 Dashboard / Beranda",
            "🧠 Diagnosis (Certainty Factor)",
            "📊 Data Nutrisi Standar",
            "🍲 Data Rekomendasi Makanan",
            "ℹ️ Tentang & Bantuan Teori"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.write(f"Pengguna Aktif: **{st.session_state['username']}**")
    if st.sidebar.button("🚪 Keluar Aplikasi (Logout)", type="secondary", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    # Routing Halaman ke Fungsi Masing-Masing
    if current_page == "🏠 Dashboard / Beranda":
        dashboard_page()
    elif current_page == "🧠 Diagnosis (Certainty Factor)":
        diagnosis_page()
    elif current_page == "📊 Data Nutrisi Standar":
        nutrition_page()
    elif current_page == "🍲 Data Rekomendasi Makanan":
        foods_page()
    elif current_page == "ℹ️ Tentang & Bantuan Teori":
        about_page()
