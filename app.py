# app.py - INA-PREDICT untuk Streamlit

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="INA-PREDICT | Early Warning System",
    page_icon="🌋",
    layout="wide"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0f0d 0%, #14281f 100%);
    }
    h1, h2, h3 {
        color: #3d9b6d !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/shield.png", width=60)
st.sidebar.title("🛡️ INA-PREDICT")
st.sidebar.markdown("*Early Warning System*")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Menu Navigasi",
    ["🏠 Dashboard", "🤖 Chatbot AI", "💝 Donasi", "📞 Kontak Darurat", "📖 Panduan Bencana"]
)

# ========== DASHBOARD ==========
if menu == "🏠 Dashboard":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2b6e4e, #3d9b6d); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">🌋 INA-PREDICT</h1>
        <p style="color: white;">Sistem Peringatan Dini Bencana Indonesia | 514 Kabupaten/Kota</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Kejadian 2026", "3,247", "+12%")
    with col2:
        st.metric("Peringatan Aktif", "34", "🔴")
    with col3:
        st.metric("Titik Evakuasi", "7,245", "🏢")
    with col4:
        st.metric("Pengungsi", "412.7k", "👥")
    
    st.info("🔴 **BREAKING NEWS:** Banjir Bandang Garut - 1.800 Jiwa Mengungsi, 500 rumah terendam")
    
    st.subheader("🏆 Provinsi dengan Risiko Tertinggi")
    risk_data = {
        "Jawa Barat": 92, "Banten": 89, "Jawa Timur": 87, "Jawa Tengah": 84,
        "Sulawesi Tengah": 82, "Sumatera Barat": 80, "Kalimantan Selatan": 79
    }
    for prov, risk in risk_data.items():
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between;">
                <span>{prov}</span>
                <span style="color: {'#e07a5f' if risk >= 75 else '#e0a343'};">{risk}%</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;">
                <div style="background: {'#e07a5f' if risk >= 75 else '#e0a343'}; width: {risk}%; height: 8px; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========== CHATBOT AI ==========
elif menu == "🤖 Chatbot AI":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2b6e4e, #3d9b6d); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">🤖 INA-BOT ULTRA</h1>
        <p style="color: white;">Database 514 Kabupaten/Kota | Super Responsif</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "🗺️ Halo! Saya INA-BOT dengan database 514 kabupaten/kota!\n\nCoba tanya:\n• 'Risiko bencana di Bandung'\n• 'Cuaca di Manado'\n• 'Titik evakuasi Surabaya'\n• 'Info gempa'\n• 'Nomor darurat'"}
        ]
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Ketik nama kota atau pertanyaan bencana..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        prompt_lower = prompt.lower()
        response = "🗺️ Coba sebutkan nama kota atau tanyakan tentang banjir, gempa, atau tas siaga."
        
        if "gempa" in prompt_lower:
            response = "🌍 Gempa 5.2 SR di Garut, Jabar. Tips: Drop, Cover, Hold On!"
        elif "banjir" in prompt_lower:
            response = "🌊 Banjir: Evakuasi ke tempat tinggi! Matikan listrik!"
        elif "bandung" in prompt_lower:
            response = "📍 Bandung: Risiko 88% (Tinggi). Ancaman: Banjir, Longsor. Titik evakuasi: Gasibu, Gedung Sate."
        elif "jakarta" in prompt_lower:
            response = "📍 Jakarta: Risiko 78% (Sedang). Ancaman: Banjir, Rob. Titik evakuasi: Monas, GBK."
        elif "surabaya" in prompt_lower:
            response = "📍 Surabaya: Risiko 84% (Tinggi). Ancaman: Banjir. Titik evakuasi: Taman Bungkul, Stadion GBK."
        elif "nomor darurat" in prompt_lower:
            response = "📞 Nomor Darurat: 112 (Pusat), 118 (Ambulans), 113 (Pemadam)"
        elif "tas siaga" in prompt_lower:
            response = "🎒 Tas Siaga: Air 3L, makanan, obat, senter, baterai, dokumen, uang tunai"
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# ========== DONASI ==========
elif menu == "💝 Donasi":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2b6e4e, #3d9b6d); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">💝 DONASI BENCANA INDONESIA</h1>
        <p style="color: white;">Salurkan bantuan untuk korban bencana</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🏦 BCA**\n1234567890\na.n. Yayasan Bencana Indonesia")
    with col2:
        st.markdown("**🏦 MANDIRI**\n1234567890123\na.n. Yayasan Bencana Indonesia")
    with col3:
        st.markdown("**🏦 BRI**\n123456789012345\na.n. Yayasan Bencana Indonesia")
    
    with st.form("donasi_form"):
        name = st.text_input("Nama Lengkap *")
        amount = st.number_input("Nominal Donasi", min_value=10000, step=10000, value=100000)
        if st.form_submit_button("💝 DONASI SEKARANG"):
            if name:
                st.success(f"✅ Terima kasih {name}! Silakan transfer ke rekening di atas.")

# ========== KONTAK DARURAT ==========
elif menu == "📞 Kontak Darurat":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2b6e4e, #3d9b6d); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">📞 KONTAK DARURAT 24 JAM</h1>
        <p style="color: white;">GRATIS dari seluruh operator</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**📞 112**\nPUSAT DARURAT\nPolisi, Ambulans, Pemadam")
    with col2:
        st.markdown("**🚑 118/119**\nAMBULANS\nLayanan medis darurat")
    with col3:
        st.markdown("**🔥 113**\nPEMADAM\nKebakaran & penyelamatan")
    with col4:
        st.markdown("**🌳 BNPB**\n021-3522911\nBadan Nasional Penanggulangan Bencana")

# ========== PANDUAN BENCANA ==========
elif menu == "📖 Panduan Bencana":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2b6e4e, #3d9b6d); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">📖 PANDUAN KESIAPSIAGAAN BENCANA</h1>
        <p style="color: white;">Pedoman resmi BNPB</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔴 RISIKO TINGGI (≥75%) - DARURAT"):
        st.write("Segera evakuasi ke tempat aman! Ikuti instruksi petugas!")
    
    with st.expander("🟠 RISIKO SEDANG (50-74%) - SIAGA"):
        st.write("Tingkatkan kewaspadaan! Pantau info setiap 2 jam!")
    
    with st.expander("🟢 RISIKO RENDAH (<50%) - NORMAL"):
        st.write("Tetap waspada! Siapkan perlengkapan darurat!")
    
    st.subheader("🎒 TAS DARURAT")
    st.write("• Air minum 3 liter per orang")
    st.write("• Makanan kaleng, biskuit, energy bar")
    st.write("• Obat-obatan pribadi & P3K")
    st.write("• Senter + baterai cadangan")
    st.write("• Dokumen penting (plastik kedap air)")
    st.write("• Masker N95 + uang tunai")

st.markdown("---")
st.markdown("Sumber: BNPB, BMKG, BPBD | INA-PREDICT © 2026")