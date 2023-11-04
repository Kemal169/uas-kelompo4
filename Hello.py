import streamlit as st
import pandas as pd
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.charts import Scatter
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from streamlit_option_menu import option_menu


# Konfigurasi halaman
st.set_page_config(
    page_title="Ulangan Akhir Semester",
    page_icon=":bar_chart:",
)

# Judul aplikasi
st.title('Aplikasi Kelompok 4 (Kiw kiw)')

with st.sidebar:
    selected_data = option_menu("Pilih Data:", ["Mobile Legend Heroes", "MPL ID S10", "Shopping Trends", "Forbes Billionaires"],
                                 icons=["person", "trophy-fill", "bag-check-fill", "currency-dollar", "gear"], menu_icon="list", default_index=0)
    # selected_data = st.selectbox("Pilih Data:", ["Mobile Legend Heroes", "MPL ID S10", "Shopping Trends", "Forbes Billionaires"], format_func=lambda x: "Mobile Legend Heroes" if x == "Mobile Legend Heroes" else x, index=0)

if selected_data == "Mobile Legend Heroes":
    df = pd.read_csv('Mlbb_Heroes.csv')

    # Menu Sidebar
    menu = st.sidebar.selectbox('Menu', ['Tampilkan Data', 'Tentang'])

    if menu == 'Tampilkan Data':
        # Menampilkan data awal
        st.write('Data Awal MLBB Heroes:')
        st.write(df)

        # Menghitung jumlah hero untuk setiap role
        role_counts = df['Primary_Role'].value_counts()

        # Membuat data untuk pie chart
        data = [(role, count) for role, count in zip(role_counts.index, role_counts)]

        # Membuat objek Pie chart
        pie = Pie()
        # Menambahkan judul pie chart
        pie.set_global_opts(title_opts=opts.TitleOpts(title="Role Hero"))

        pie.add("", data)
        # Menampilkan hasil dari pie chart
        st_pyecharts(pie)
#======================================================================================================================
        selected_role = st.sidebar.selectbox('Pilih Role untuk Chart Bar:', ["", "Tank", "Fighter", "Mage", "Assassin", "Support", "Marksman"])

        # Filter data berdasarkan peran (role)
        if selected_role:
            filtered_df = df[df['Primary_Role'] == selected_role]
        else:
            filtered_df = df

        # Membuat objek Bar chart
        bar_chart = (
            Bar()
            .add_xaxis(filtered_df['Name'].tolist())
            .add_yaxis("Esport Wins", filtered_df['Esport_Wins'].tolist())
            .add_yaxis("Esport Loss", filtered_df['Esport_Loss'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Match Esport Heroes"),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                xaxis_opts=opts.AxisOpts(name="Hero Name"),
                yaxis_opts=opts.AxisOpts(name="Esport Wins & Loss"),
            )
        )

         # Menampilkan chart di Streamlit
        st_pyecharts (bar_chart)
#==============================================================================================================================

        # Filter data berdasarkan peran (role)
        if selected_role:
            filtered_df = df[df['Primary_Role'] == selected_role]
        else:
            filtered_df = df

        # Pilih kolom-kolom yang akan ditampilkan di yaxis
        selected_columns = st.multiselect("Pilih Kolom :", ["Hp", "Hp_Regen", "Mana", "Mana_Regen", "Phy_Damage", "Phy_Defence", "Mag_Defence", "Mov_Speed"])

        # Membuat objek Bar chart
        bar_chart1 = Bar()

        # Menambahkan data ke chart
        bar_chart1.add_xaxis(filtered_df['Name'].tolist())
        for column in selected_columns:
            bar_chart1.add_yaxis(column, filtered_df[column].tolist())

        # Konfigurasi chart
        bar_chart1.set_global_opts(
            title_opts=opts.TitleOpts(title="Heroes MLBB"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            xaxis_opts=opts.AxisOpts(name="Hero Name"),
            yaxis_opts=opts.AxisOpts(name="column"),
        )

        # Menampilkan grafik
        st_pyecharts(bar_chart1)

    elif menu == 'Tentang':
        st.write('Aplikasi Streamlit sederhana untuk menampilkan data MLBB Heroes.')

        st.sidebar.header("Pilih Role Hero")
        # Widget untuk pencarian berdasarkan primary_role
        selected_role = st.sidebar.selectbox('Pilih Role:', ["", "Tank", "Fighter", "Mage", "Assassin", "Support", "Marksman"])

        # Widget untuk pencarian berdasarkan lane
        selected_lane = st.sidebar.selectbox('Pilih Lane:', ["", "EXP Lane", "Roamer", "Jungler", "Gold Lane", "Mid"])

        # Widget untuk mengurutkan berdasarkan HP terbanyak
        sort_by_hp = st.sidebar.checkbox('Urutkan berdasarkan HP terbanyak')

        # Cek apakah widget role sudah dipilih
        if selected_role:
            # Filter DataFrame berdasarkan primary_role yang dipilih
            filtered_df = df[df['Primary_Role'] == selected_role]

            # Jika opsi untuk mengurutkan berdasarkan HP terbanyak diaktifkan
            if sort_by_hp:
                filtered_df = filtered_df.sort_values(by='Hp', ascending=False)

            # Tampilkan hasil pencarian
            st.write(f'Data dengan Primary Role: {selected_role}')
            st.write(filtered_df)

        # Cek apakah widget lane sudah terisi
        if selected_lane:
            # Filter DataFrame berdasarkan lane yang dipilih
            if selected_role:
                filtered_df = filtered_df[filtered_df['Lane'] == selected_lane]
            else:
                filtered_df = df[df['Lane'] == selected_lane]

            # Jika opsi untuk mengurutkan berdasarkan HP terbanyak diaktifkan
            if sort_by_hp:
                filtered_df = filtered_df.sort_values(by='Hp', ascending=False)

            # Tampilkan hasil pencarian
            st.write(f'Data dengan Lane: {selected_lane}')
            st.write(filtered_df)
