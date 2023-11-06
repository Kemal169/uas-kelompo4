import pandas as pd
import streamlit as st
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts


def show_shopping():
    
    df = pd.read_csv('shopping_trends_updated.csv')

    menu = st.sidebar.selectbox('Menu', ['Tampilkan Data'])

    if menu == 'Tampilkan Data':

        # Menampilkan data awal
        st.write('Data Awal Shopping Trends :')
        st.write(df)

        category = st.selectbox("Pilih Kategori", ["Age", "Category", "Shipping Type"])
        if category == "Age":
            # Mengkonversi kolom 'Age' menjadi tipe data numerik
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
            # Menghitung jumlah orang terkaya per umur
            data_count = df['Age'].value_counts().reset_index()
            data_count.columns = ['Age', 'Count']
            chart_title = "Berdasarkan Umur"
            xaxis_name = "Age"

        elif category == "Category":
            # Menghitung jumlah orang terkaya per category
            data_count = df['Category'].value_counts().reset_index()
            data_count.columns = ['Category', 'Count']
            chart_title = "Berdasarkan Category"
            xaxis_name = "Category"

        else:
            # Menghitung jumlah orang terkaya per Shipping Type
            data_count = df['Shipping Type'].value_counts().reset_index()
            data_count.columns = ['Shipping Type', 'Count']
            chart_title = "Berdasarkan Shipping Type"
            xaxis_name = "Shipping Type"

        bar = (
            Bar()
            .add_xaxis(data_count[xaxis_name].tolist())
            .add_yaxis("Jumlah", data_count['Count'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title=chart_title),
                xaxis_opts=opts.AxisOpts(name=xaxis_name),
                yaxis_opts=opts.AxisOpts(name="Jumlah"),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
            )
        )
            
        st_pyecharts(bar)

        # Menampilkan metrik
        with st.expander("Penjelasan Singkat"):
            col1, col2, col3= st.columns(3)
            col1.metric(label="Total Data", value=data_count['Count'].sum())
            col2.metric(label="Jumlah Minimum Data", value=data_count['Count'].min())
            col3.metric(label="Jumlah Maximum Data", value=data_count['Count'].max())
        st.markdown("<br>", unsafe_allow_html=True)

        # Membuat Pie Chart untuk metode pembayaran
        payment_data = df['Payment Method'].value_counts().reset_index()
        payment_data.columns = ['Payment Method', 'Count']

        c = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(payment_data['Payment Method'], payment_data['Count'])],
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Pie Chart: Metode Pembayaran"),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="25%", pos_left="2%"),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
        )
        st_pyecharts(c)
        
        with st.expander("Penjelasan Singkat"):
            col4, col5, col6= st.columns(3)
            total_count = payment_data['Count'].sum()
            max_payment_method = payment_data['Payment Method'].iloc[0]
            max_payment_count = payment_data['Count'].iloc[0]
            min_payment_method = payment_data['Payment Method'].iloc[-1]
            min_payment_count = payment_data['Count'].iloc[-1]
            col4.metric("Total Transaksi", total_count)
            col5.metric("Metode Pembayaran Terpopuler", max_payment_method, f"{max_payment_count} transaksi")
            col6.metric("Metode Pembayaran Tidak Populer", min_payment_method, f"{min_payment_count} transaksi")
        