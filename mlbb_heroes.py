import pandas as pd
import streamlit as st
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

def show_mlbb_heroes():
    df = pd.read_csv('Mlbb_Heroes.csv')

    # Menu Sidebar
    menu = st.sidebar.selectbox('Menu', ['Tampilkan Data'])

    if menu == 'Tampilkan Data':
        # Menampilkan data awal
        st.write('Data Awal MLBB Heroes :')
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

        with st.expander("Penjelasan Singkat"):
            selected_category = st.selectbox('Pilih Kategori', role_counts.index)
            if selected_category:
                selected_count = role_counts[selected_category]
                st.metric("Jumlah Hero", selected_count)

        selected_role = st.sidebar.selectbox('Pilih Role untuk Chart Bar :', ["", "Tank", "Fighter", "Mage", "Assassin", "Support", "Marksman"])

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
                xaxis_opts=opts.AxisOpts(name="Name"),
                yaxis_opts=opts.AxisOpts(name="Esport Wins & Loss"),
            )
        )

        # Menampilkan chart di Streamlit
        st_pyecharts (bar_chart)

        with st.expander("Penjelasan Singkat"):
            if selected_role:
                total_wins = filtered_df['Esport_Wins'].sum()
                total_loss = filtered_df['Esport_Loss'].sum()
                st1, st2= st.columns(2)
                st1.metric(label=f"Total Wins ({selected_role})", value=total_wins)
                st2.metric(label=f"Total Loss ({selected_role})", value=total_loss)

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
            xaxis_opts=opts.AxisOpts(name="Name"),
            yaxis_opts=opts.AxisOpts(name="column"),
        )

        # Menampilkan grafik
        st_pyecharts(bar_chart1)