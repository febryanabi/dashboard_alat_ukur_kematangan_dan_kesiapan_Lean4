import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os
from PIL import Image

# Judul aplikasi
st.title('Alat Ukur Kematangan dan Kesiapan Lean 4.0 Dengan Sustainability untuk Perusahaan Bahan Kimia')

# Input nama dan nama perusahaan
nama = st.text_input('Nama')
nama_perusahaan = st.text_input('Nama Perusahaan')

# Contoh struktur pertanyaan baru: list of dict per dimensi
DIMENSI = {
    'Proses': [
        {
            'judul': 'A1. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pemahaman penerapan Lean"',
            'definisi': 'Definisi: Perusahaan mengetahui dan memiliki strategi dalam penerapan Lean dalam proses bisnis'
        },
        {
            'judul': 'A2. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Evaluasi dan pemantauan OEE"',
            'definisi': 'Definisi: Pengukuran, pemantauan, dan evaluasi terhadap OEE dilakukan secara rutin untuk mengefisiensikan produksi'
        },
        {
            'judul': 'A3. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pengimplementasian Lean Tools"',
            'definisi': 'Definisi: Penerapan Lean tools seperti 5S, kaizen, VSM, poka yoke untuk meningkatkan proses bisnis perusahaan'
        },
        {
            'judul': 'A4. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pengendalian Mutu Kualitas Produk"',
            'definisi': 'Definisi: Penjaminan produk yang dihasilkan memenuhi kualitas, keamanan lingkungan, dan spesifikasi yang ditentukan'
        },
        {
            'judul': 'A5. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Dilakukannya Continuous Improvement"',
            'definisi': 'Definisi: Penerapan perbaikan berkelanjutan dalam semua aspek proses bisnis untuk meningkatkan kinerja'
        },
        {
            'judul': 'A6. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Evaluasi terhadap pengimplemenasian Lean"',
            'definisi': 'Definisi: Evaluasi terhadap penerapan lean tools (VSM, 5S, Poka Yoke, Heijunka, etc) dilakukan untuk melihat pengembangan terhadap penggunaan.'
        },
        {
            'judul': 'A7. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Identifikasi dan monitoring Downtime"',
            'definisi': 'Definisi: Tingkat sensitivitas sistem perusahaan dalam mengenali dan memantau waktu downtime pada proses produksi'
        },
        {
            'judul': 'A8. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Level Produk Cacat"',
            'definisi': 'Definisi: Usaha mengecilkan kemungkinan cacat pada produk dengan penjaminan proses produksi'
        },
        {
            'judul': 'A9. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Identifikasi dan Monitoring Waste"',
            'definisi': 'Definisi: Perusahaan melakukan pemantauan, pengendalian, dan pengevaluasian berkala terhadap segala pemborosan (waktu, produksi, inventory, proses, emisi)'
        },
        {
            'judul': 'A10. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pengendalian Penggunaan Bahan Baku"',
            'definisi': 'Definisi: Pengawasan dan kontrol terhadap produksi untuk menghindari kelebihan pemrosesan bahan kimia'
        }
    ],
    'Teknologi': [
        {
            'judul': 'B1. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Otomasi proses produksi"',
            'definisi': 'Definisi: Proses produksi dilakukan oleh perusahaan secara otomatis baik full maupun sebagian untuk mengurangi campur tangan manusia'
        },
        {
            'judul': 'B2. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Cyber security"',
            'definisi': 'Definisi: Diterapkannya keamanan siber terhadap integrasi teknologi dan data perusahaan baik untuk internal maupun eksternal'
        },
        {
            'judul': 'B3. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Penggunaan Data Analytics"',
            'definisi': 'Definisi: Perusahaan menggunakan data analytics untuk membantu melakukan real time decision making'
        },
        {
            'judul': 'B4. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Implementasi Industri 4.0"',
            'definisi': 'Definisi: Adanya visi dan goals dalam penerapan industri 4.0 pada perusahaan'
        },
        {
            'judul': 'B5. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Penggunaan Teknologi Monitoring Proses"',
            'definisi': 'Definisi: Perusahaan memanfaatkan teknologi untuk monitoring real time kegiatan produksi dan operasional dalam perusahaan'
        },
        {
            'judul': 'B6. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Kompetensi Pekerja dalam Penggunaan Teknologi Digital"',
            'definisi': 'Definisi: Pekerja secara aktif dipersiapkan untuk melakukan pengoperasian menggunakan teknologi berbasis digital'
        }
    ],
    'Environment': [
        {
            'judul': 'C1. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Penggunaan Energi"',
            'definisi': 'Definisi: Pemantauan terhadap penggunaan energi untuk melakukan pengelolaan konsumsi energi selama proses produksi sebagai upaya penerapan pengurangan dampak terhadap lingkungan dan pemborosan'
        },
        {
            'judul': 'C2. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pemantauan Penggunaan Air"',
            'definisi': 'Definisi: Perusahaan melakukan pemantauan terhadap pengolahaan ulang air dan pengendalian konsumsi untuk menilai dampak pada penggunaan'
        },
        {
            'judul': 'C3. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pengukuran Green House Gasses"',
            'definisi': 'Definisi: Green Houses Gasses secara rutin dilakukan pengukuran  untuk menilai dampak terhadap lingkungan'
        },
        {
            'judul': 'C4. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pengendalian bahaya terhadap lingkungan"',
            'definisi': 'Definisi: Penerapan pengurangan waste akibat proses produksi terhadap linkungan sekitar'
        },
        {
            'judul': 'C5. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Environmental report"',
            'definisi': 'Definisi: Dilakukannya pembuatan laporan dari hasil pengukuran emisi yang diproduksi oleh perusahaan'
        }
    ],
    'Sosial': [
        {
            'judul': 'D1. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Monitoring dampak proses kimia terhadap lingkungan diluar area pabrik"',
            'definisi': 'Definisi : Melakukan identifikasi dan evaluasi potensi dan dampak dari proses kimia yang dilakukan terhadap lingkungan sekitar'
        },
        {
            'judul': 'D2. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Pemantauan keselematan pekerja"',
            'definisi': 'Definisi : Keselamatan dan kesehatan pekerja pada kegiatan operasional produksi dipantau dan dievaluasi secara berkala'
        },
        {
            'judul': 'D3. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Employee training and development"',
            'definisi': 'Definisi : Pelatihan dan pengembangan terhadap karwayan dilakukan secara berkala'
        }
    ],
    'Ekonomi': [
        {
            'judul': 'E1. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Operation Profit"',
            'definisi': 'Definisi : Monitoring terhadap implementasi teknologi dalam meningkatkan produktivitas proses, kualitas output, dan penghematan biaya, sehingga menambah profitabilitas operasional'
        },
        {
            'judul': 'E2. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Investasi terhadap teknologi"',
            'definisi': 'Definisi : Perusahaan mengalokasikan dalam pengadaan dan implementasi teknologi digital dan arsitektur untuk menerapkan Industri 4.0'
        },
        {
            'judul': 'E3. Berapa level kematangan dan kesiapan perusahaan anda dalam melakukan "Operational cost"',
            'definisi': 'Definisi : Pengelolaan dan pemantauan biaya pada kegiatan operasional baik produksi maupun non produksi'
        }
    ]
}

# Bobot indikator per pertanyaan (dalam persen, urut sesuai DIMENSI)
BOBOT = {
    'Proses': [4.44, 3.88, 6.22, 7.77, 10.36, 5.18, 15.54, 31.08, 10.36, 5.18],
    'Teknologi': [19.74, 9.87, 39.47, 7.89, 9.87, 13.16],
    'Environment': [10.81, 32.43, 16.22, 8.11, 32.43],
    'Sosial': [54.55, 18.18, 27.27],
    'Ekonomi': [27.27, 18.18, 54.55]
}

# Input jawaban untuk setiap pertanyaan per dimensi
st.header('Isi Penilaian')
with st.form('form_penilaian'):
    jawaban = {}
    for dim, pertanyaans in DIMENSI.items():
        st.subheader(dim)
        scores = []
        for i, q in enumerate(pertanyaans):
            st.markdown(f"**{q['judul']}**")
            st.markdown(f"<span style='font-size: 0.9em; color: #555;'>{q['definisi']}</span>", unsafe_allow_html=True)
            score = st.slider('Jawaban (1-5)', 1, 5, 3, key=f'{dim}_score_{i}')
            img_path = f"{dim}_{i}.png"
            if os.path.exists(img_path):
                st.image(Image.open(img_path), caption=f'Penjelasan Level untuk pertanyaan ini', use_container_width=True)
            scores.append(score)
        jawaban[dim] = scores
    submitted = st.form_submit_button('Submit')

if 'submitted' in locals() and submitted:
    # Hitung skor per dimensi dengan rumus baru
    dimensi_scores = {}
    for dim, scores in jawaban.items():
        bobot = BOBOT[dim]
        n = len(scores)
        nilai_dimensi = sum([s * (b/100) / n for s, b in zip(scores, bobot)])
        dimensi_scores[dim] = nilai_dimensi * n  # agar skala tetap 1-5 jika semua skor 5
    # Radar chart
    categories = list(dimensi_scores.keys())
    values = list(dimensi_scores.values())
    values += values[:1]  # close the loop
    categories += categories[:1]
    fig = go.Figure(
        data=[go.Scatterpolar(r=values, theta=categories, fill='toself', name='Nilai')],
        layout=go.Layout(
            polar=dict(radialaxis=dict(visible=True, range=[1,5])),
            showlegend=False
        )
    )
    st.plotly_chart(fig)
    # Penjelasan rumus spider chart
    st.markdown("""
    **Rumus Perhitungan Spider Chart:**
    
    Untuk setiap indikator pada suatu dimensi:
    
    nilai_indikator = skala × (bobot / 100) ÷ jumlah pertanyaan dimensi
    
    - **skala**: nilai input user (1-5)
    - **bobot**: bobot indikator (dalam persen)
    - **jumlah pertanyaan dimensi**: banyaknya indikator pada dimensi tersebut
    
    Nilai dimensi adalah penjumlahan seluruh nilai_indikator pada dimensi tersebut:
    
    nilai_dimensi = jumlah seluruh nilai_indikator pada dimensi
    
    Dimana n adalah jumlah indikator pada dimensi tersebut.
    """)
    # Dimensi terendah dan tertinggi
    min_dim = min(dimensi_scores, key=dimensi_scores.get)
    max_dim = max(dimensi_scores, key=dimensi_scores.get)
    st.success(f'Dimensi dengan nilai terendah: {min_dim} ({dimensi_scores[min_dim]:.2f})')
    st.info(f'Dimensi dengan nilai tertinggi: {max_dim} ({dimensi_scores[max_dim]:.2f})')
