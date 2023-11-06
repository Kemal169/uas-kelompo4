import pandas as pd
import altair as alt
import streamlit as st
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

def show_Forbes():
    df = pd.read_csv('forbes_2640_billionaires.csv')

    menu = st.sidebar.selectbox('Menu', ['Tampilkan Data'])
    if menu == 'Tampilkan Data' :
        # Menampilkan data awal
        st.write('Data Awal Para Billionaires :')
        st.write(df)
        category = st.selectbox("Pilih Kategori", ["Age", "Industry", "Country"])
        if category == "Age":
            # Mengkonversi kolom 'Age' menjadi tipe data numerik
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
            # Menghitung jumlah orang terkaya per umur
            data_count = df['Age'].value_counts().reset_index()
            data_count.columns = ['Age', 'Count']
            chart_title = "Berdasarkan Umur"
            xaxis_name = "Age"
        elif category == "Industry":
            # Menghitung jumlah orang terkaya per industri
            data_count = df['industry'].value_counts().reset_index()
            data_count.columns = ['Industry', 'Count']
            chart_title = "Berdasarkan Industri"
            xaxis_name = "Industry"
        else:
            # Menghitung jumlah orang terkaya per negara
            data_count = df['country'].value_counts().reset_index()
            data_count.columns = ['Country', 'Count']
            chart_title = "Berdasarkan Negara"
            xaxis_name = "Country"
            # Membuat Bar chart
        bar = (
            Bar()
            .add_xaxis(data_count[xaxis_name].tolist())
            .add_yaxis("Jumlah Orang Terkaya", data_count['Count'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title=chart_title),
                xaxis_opts=opts.AxisOpts(name=xaxis_name),
                yaxis_opts=opts.AxisOpts(name="Jumlah Orang Terkaya"),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="right")
            )
        )
            # Menampilkan chart menggunakan st_pyecharts
        st_pyecharts(bar)

        with st.expander("Penjelasan Singkat"):
            # Menambahkan st.metric
            st1, st2, st3= st.columns(3)
            st1.metric("Total", data_count['Count'].sum())
            st2.metric("Maksimum", data_count['Count'].max())
            st3.metric("Minimum", data_count['Count'].min())

        # Menambahkan MultiSelect untuk memilih industri
        selected_industries = st.multiselect("Pilih Industri Yang Ingin Ditampilkan", df['industry'].unique())

        # Filter data berdasarkan industri yang dipilih
        filtered_data = df[df['industry'].isin(selected_industries)]

        # Membuat Scatter Plot
        scatter_chart = alt.Chart(filtered_data).mark_circle().encode(
            x=alt.X("Self-Made Score:Q", title="Self-Made Score"),
            y=alt.Y("Philanthropy Score:Q", title="Philanthropy Score"),
            color=alt.Color("industry:N", title="Industri")
        ).properties(
            width=800,
            height=500
        )
        # Menampilkan Scatter Plot
        st.altair_chart(scatter_chart)

        with st.expander("Penjelasan Singkat"):
            for industry in selected_industries:
                st.metric(label=industry, value=filtered_data[filtered_data['industry'] == industry].shape[0])
        
        # Menambahkan widget Selectbox untuk memilih status marital
        selected_marital_status = st.selectbox("Pilih Status Marital", df['Marital Status'].unique())

        # Filter data berdasarkan status marital yang dipilih
        filtered_data = df[df['Marital Status'] == selected_marital_status]

        # Menghitung jumlah pendidikan per kategori (Bachelor, Master, Doctorate, Drop Out)
        education_counts = filtered_data[['Bachelor', 'Master', 'Doctorate', 'Drop Out']].sum()

        # Membuat Bar Chart
        bar = (
            Bar()
            .add_xaxis(education_counts.index.tolist())
            .add_yaxis("Jumlah Orang Terkaya", education_counts.tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"Pendidikan Status ({selected_marital_status})"),
                xaxis_opts=opts.AxisOpts(name="Pendidikan"),
                yaxis_opts=opts.AxisOpts(name="Jumlah Orang Terkaya"),
                toolbox_opts=opts.ToolboxOpts(orient="vertical", pos_left="right")
            )
        )
        # Menampilkan Bar Chart
        st_pyecharts(bar)

        with st.expander("Penjelasan Singkat"):
             # Menampilkan metrik untuk setiap kategori pendidikan
            st.metric("Bachelor", education_counts['Bachelor'])
            st.metric("Master", education_counts['Master'])
            st.metric("Doctorate", education_counts['Doctorate'])
            st.metric("Drop Out", education_counts['Drop Out'])
