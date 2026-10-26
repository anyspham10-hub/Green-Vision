import streamlit as st
import pandas as pd
from load_data import load_dashboard
from translations import get_text
from styles import inject_styles
from data_processing import build_district_data, get_district_image_path
from sidebar import render_sidebar
from page_manager import render_overview, render_ndvi, render_analysis

dashboard = load_dashboard()

st.set_page_config(
    page_title="GREEN VISION",
    page_icon="🌳",
    layout="wide"
)

inject_styles()

try:
    district_data = build_district_data(dashboard)
except Exception as e:
    st.error(f"Lỗi khi đọc dữ liệu dashboard: {e}")
    district_data = {}

selected, district = render_sidebar(get_text, district_data)

if selected in [get_text("menu_overview"), "Đánh giá của AI"]:
    render_overview(get_text, district_data, district, get_district_image_path)
elif selected == get_text("menu_ndvi"):
    render_ndvi(get_text)
elif selected == get_text("menu_analysis"):
    render_analysis(get_text, district_data)
elif selected == get_text("menu_settings"):
    st.title(get_text("settings_title"))

    st.subheader(get_text("language"))

    selected_language = st.selectbox(
        get_text("language"),
        [get_text("vietnamese"), get_text("english")],
        index=0 if st.session_state.language == 'vi' else 1,
        key="language_selector",
    )

    if selected_language == get_text("english"):
        st.session_state.language = 'en'
    else:
        st.session_state.language = 'vi'

    if selected_language == get_text("english"):
        st.success("✅ Language changed to English")
    else:
        st.success("✅ Ngôn ngữ đã thay đổi thành Tiếng Việt")

    st.info("💡 Trang web sẽ cập nhật ngôn ngữ ngay lập tức / The website will update the language immediately")
elif selected == get_text("menu_report"):
    st.title(get_text("report_title"))
    report_df = pd.DataFrame({
        get_text("district"): list(district_data.keys()),
        get_text("temperature"): [district_data[d]["temp"] for d in district_data],
    })
    st.dataframe(report_df)
    csv = report_df.to_csv(index=False)
    st.download_button(get_text("download_report"), csv, "report.csv", "text/csv")
