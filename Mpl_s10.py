import pandas as pd
import streamlit as st
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

def show_Mpl_s10():
    df = pd.read_csv('MPL_ID_S10.csv')

    menu = st.sidebar.selectbox('Menu', ['Tampilkan Data'])

    st.sidebar.header("Pilih Hero Terlebih Dahulu MPL ID S10")

    mpl_heroes = df['Hero'].unique()

    if menu == 'Tampilkan Data':

        # Menampilkan data awal
        st.write('Data Awal MPL ID S10:')
        st.write(df)

        
        st1,st2= st.columns(2)
        # Widget Hero dengan banned terbanyak
        most_banned_hero = df[df['Hero_banned'] == df['Hero_banned'].max()]['Hero'].iloc[0]
        st1.metric("Hero dengan banned terbanyak", most_banned_hero)
        
        # Widget Hero dengan banned tersedikit
        least_banned_hero = df[df['Hero_banned'] == df['Hero_banned'].min()]['Hero'].iloc[0]
        st2.metric("Hero dengan banned tersedikit", least_banned_hero)

        st.markdown("<br>", unsafe_allow_html=True)

        bar_chart = (
            Bar()
            .add_xaxis(df['Hero'].tolist())
            .add_yaxis("Rs_won", df['Rs_won'].tolist())
            .add_yaxis("Rs_lost", df['Rs_lost'].tolist())
            .add_yaxis("Bs_won", df['Bs_won'].tolist())
            .add_yaxis("Bs_lost", df['Bs_lost'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Match Esport"),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                xaxis_opts=opts.AxisOpts(name="Name"),
                yaxis_opts=opts.AxisOpts(name="Esport Won & Lost"),
                toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="right")
            )
        )
        # Menampilkan chart di Streamlit
        st_pyecharts (bar_chart)

        with st.expander("Penjelasan Singkat"):
            total_rs_won = df['Rs_won'].sum()
            total_rs_lost = df['Rs_lost'].sum()
            total_bs_won = df['Bs_won'].sum()
            total_bs_lost = df['Bs_lost'].sum()

            col1, col2, col3, col4= st.columns(4)
            col1.metric("Total Ranked Wins", total_rs_won)
            col2.metric("Total Ranked Losses", total_rs_lost)
            col3.metric("Total Brawl Wins", total_bs_won)
            col4.metric("Total Brawl Losses", total_bs_lost)
            
        st.markdown("<br>", unsafe_allow_html=True)

        pie = (
            Pie(init_opts=opts.InitOpts(theme='shine'))
            .add(
                series_name="Hero_picked",
                data_pair=list(zip(df['Hero'], df['Hero_picked'])),
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False),)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Hero Picked",pos_top="10%", pos_bottom="10%"),
                legend_opts=opts.LegendOpts(type_="scroll" ),
            )
        )
        
        # Menampilkan grafik menggunakan st_pyecharts
        st_pyecharts(pie)

        with st.expander("Penjelasan Singkat"):
            col5, col6, col7= st.columns(3)
            total_heroes = len(mpl_heroes)
            col5.metric("Total Hero", total_heroes)
            total_matches = len(df)
            col6.metric("Total Match", total_matches)
            most_picked_hero = df['Hero'].value_counts().idxmax()
            col7.metric("Hero Sering Digunakan", most_picked_hero)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Widget Multi-select untuk memilih Hero
        selected_heroes = st.sidebar.multiselect("Pilih Hero:", df['Hero'].unique())

        # Filter data berdasarkan Hero yang dipilih
        filtered_df = df[df['Hero'].isin(selected_heroes)]
        
        bar_chart1 = (
            Bar()
            .add_xaxis(filtered_df['Hero'].tolist())
            .add_yaxis("T Wins", filtered_df['T_wins'].tolist())
            .add_yaxis("T Lose", filtered_df['T_lose'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Match Esport Heroes"),
                xaxis_opts=opts.AxisOpts(name="Name"),
                yaxis_opts=opts.AxisOpts(name="Esport Won & Lost"),
                toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="right")
            )
        )
        
        # Menampilkan chart di Streamlit
        st_pyecharts(bar_chart1)
