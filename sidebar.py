import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar(get_text, district_data):
    with st.sidebar:
        st.title("🌳 " + get_text("app_title"))
        st.caption(get_text("app_description"))

        selected = option_menu(
            menu_title=None,
            options=[
                get_text("menu_overview"),
                get_text("menu_ndvi"),
                get_text("menu_analysis"),
                get_text("menu_settings"),
                get_text("menu_report")
            ],
            icons=[
                "house",
                "map",
                "bar-chart",
                "gear",
                "file-earmark"
            ],
            default_index=0
        )

        st.divider()

        district = st.selectbox(
            get_text("select_district"),
            list(district_data.keys())
        )

        st.divider()

        st.subheader(get_text("current_metrics"))

        st.metric("🌱 NDVI", district_data[district]["ndvi"])
        st.metric("🌳 " + get_text("avg_density"), f"{district_data[district]['green']}%")
        st.metric("🌡️ " + get_text("temperature"), f"{district_data[district]['temp']}°C")
        st.metric("🫧 O₂", f"{district_data[district]['oxygen']}%")

    return selected, district
