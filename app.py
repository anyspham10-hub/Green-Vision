"""
Green Vision – Dashboard phân tích không gian xanh Hà Nội
Entry point: streamlit run app.py
"""
import streamlit as st

from load_data import load_dashboard
from data_processing import build_district_data, get_district_image_path
from page_manager import render_overview, render_ndvi, render_analysis


# ============================================================
# 1. CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="Green Vision – Hà Nội",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. ĐA NGÔN NGỮ (VI / EN)
# ============================================================
TEXTS = {
    "vi": {
        "app_title": "🌿 Green Vision – Hà Nội",
        "language": "Ngôn ngữ",
        "menu": "Danh mục",
        "overview": "Tổng quan",
        "ndvi_map": "Bản đồ NDVI",
        "analysis": "Phân tích",
        "select_district": "Chọn quận/huyện",
        # Dashboard
        "dashboard_title": "Dashboard Không gian xanh Hà Nội",
        "updated": "Cập nhật:",
        "ndvi_map_title": "Bản đồ NDVI",
        "red_zone": "Vùng đỏ: NDVI thấp, ít cây xanh – cần ưu tiên phủ xanh.",
        "analysis_title": "Phân tích theo quận/huyện",
        "district": "Quận/Huyện",
        "temperature": "Nhiệt độ (°C)",
        "oxygen": "Oxy (%)",
        # Simulation
        "simulate_planning": "Mô phỏng quy hoạch",
        "increase_green": "Tăng mật độ cây xanh (%)",
        "current_temp": "Nhiệt độ hiện tại",
        "predicted_temp": "Nhiệt độ dự báo",
        "simulation_result": "Khi tăng",
        "percent_temp_decrease": "% mật độ cây xanh, nhiệt độ giảm khoảng",
        # AI
        "ai_evaluation": "Đánh giá AI",
        "ai_description": "Mô hình AI (Extra Trees) dự đoán nhiệt độ dựa trên "
                          "mật độ cây xanh, NDVI và oxy của quận.",
        "ai_good": "✅ Hiệu quả tốt – nhiệt độ giảm đáng kể.",
        "ai_medium": "ℹ️ Hiệu quả trung bình – có thể cân nhắc thêm.",
        "ai_warning": "⚠️ Hiệu quả thấp – cần tăng mạnh diện tích cây xanh.",
        # Sidebar metrics
        "ndvi_trend": "Xu hướng NDVI 2022–2025",
        "ndvi_decrease": "NDVI giảm",
        "avg_density": "Mật độ xanh TB",
        "avg_temp": "Nhiệt độ TB",
        "lacking_green": "Thiếu xanh nhất",
    },
    "en": {
        "app_title": "🌿 Green Vision – Hanoi",
        "language": "Language",
        "menu": "Menu",
        "overview": "Overview",
        "ndvi_map": "NDVI Map",
        "analysis": "Analysis",
        "select_district": "Select district",
        "dashboard_title": "Hanoi Green Space Dashboard",
        "updated": "Updated:",
        "ndvi_map_title": "NDVI Map",
        "red_zone": "Red zone: low NDVI, lacking green space – priority for planting.",
        "analysis_title": "District Analysis",
        "district": "District",
        "temperature": "Temperature (°C)",
        "oxygen": "Oxygen (%)",
        "simulate_planning": "Simulate Planning",
        "increase_green": "Increase green density (%)",
        "current_temp": "Current temperature",
        "predicted_temp": "Predicted temperature",
        "simulation_result": "Increasing",
        "percent_temp_decrease": "% green density reduces temperature by",
        "ai_evaluation": "AI Evaluation",
        "ai_description": "AI model (Extra Trees) predicts temperature based on "
                          "green density, NDVI and oxygen of the district.",
        "ai_good": "✅ Good effect – significant temperature drop.",
        "ai_medium": "ℹ️ Medium effect – consider adding more.",
        "ai_warning": "⚠️ Low effect – need much more green area.",
        "ndvi_trend": "NDVI trend 2022–2025",
        "ndvi_decrease": "NDVI drop",
        "avg_density": "Avg green density",
        "avg_temp": "Avg temperature",
        "lacking_green": "Least green",
    },
}


# ============================================================
# 3. CSS TÙY BIẾN (dùng class .card / .metric-card)
# ============================================================
st.markdown(
    """
    <style>
    .card {
        background: #f8fafc;
        padding: 10px 16px;
        border-radius: 10px;
        border-left: 4px solid #16a34a;
        margin-bottom: 8px;
    }
    .card h4 {
        margin: 4px 0;
        color: #14532d;
        font-size: 16px;
    }
    .metric-card {
        background: #ffffff;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. LOAD DỮ LIỆU (cache)
# ============================================================
@st.cache_data
def _load_district_data():
    df = load_dashboard()
    return build_district_data(df)


district_data = _load_district_data()

if not district_data:
    st.error("❌ Không tải được dữ liệu. Kiểm tra `dashboard_data.csv`.")
    st.stop()

districts = sorted(district_data.keys())


# ============================================================
# 5. SIDEBAR – ngôn ngữ + menu + chọn quận
# ============================================================
with st.sidebar:
    st.markdown(f"## {TEXTS['vi']['app_title']}")

    lang_label = st.radio(
        TEXTS["vi"]["language"],
        ["Tiếng Việt", "English"],
        horizontal=True,
        key="lang_selector",
    )
    lang = "vi" if lang_label == "Tiếng Việt" else "en"

    def get_text(key: str) -> str:
        return TEXTS[lang].get(key, key)

    st.markdown("---")
    st.markdown(f"### {get_text('menu')}")

    page_key = st.radio(
        get_text("menu"),
        options=["overview", "ndvi_map", "analysis"],
        format_func=lambda k: get_text(k),
        label_visibility="collapsed",
        key="page_selector",
    )

    st.markdown("---")
    district = st.selectbox(
        get_text("select_district"),
        districts,
        key="district_selector",
    )

    st.markdown("---")
    st.caption(f"{get_text('updated')} 00/06/2026")


# ============================================================
# 6. ROUTING
# ============================================================
if page_key == "overview":
    render_overview(
        get_text=get_text,
        district_data=district_data,
        district=district,
        get_district_image_path=get_district_image_path,
    )
elif page_key == "ndvi_map":
    render_ndvi(get_text=get_text)
else:
    render_analysis(get_text=get_text, district_data=district_data)