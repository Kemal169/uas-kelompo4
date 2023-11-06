import streamlit as st
from Forbes import show_Forbes
from Mpl_s10 import show_Mpl_s10
from shopping import show_shopping
from mlbb_heroes import show_mlbb_heroes
from streamlit_option_menu import option_menu

# Konfigurasi halaman
st.set_page_config(
    page_title="Ulangan Akhir Semester",
    page_icon=":bar_chart:",
)

# Judul aplikasi
st.title('Aplikasi Kelompok 4 (Kiw kiw)')

with st.sidebar:
    selected = option_menu(
        menu_title = "Pilih Data :",
        menu_icon="list",
        options=["Mobile Legend Heroes", "MPL ID S10", "Shopping Trends", "Forbes Billionaires"],
        icons=["person", "trophy-fill", "bag-check-fill", "currency-dollar", "gear"]
    )

if selected == "Mobile Legend Heroes":
    show_mlbb_heroes()

elif selected == "MPL ID S10":
    show_Mpl_s10()

elif selected == "Shopping Trends":
    show_shopping()

elif selected == "Forbes Billionaires":
    show_Forbes()
