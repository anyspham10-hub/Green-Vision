import os
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_resource
def load_ai_model():
    model_path = "rf_temperature_model.pkl"
    if os.path.exists(model_path):
        try:
            return joblib.load(model_path)
        except Exception as e:
            st.error(f"Lỗi khi load model AI: {e}")
    return None


ai_model_data = load_ai_model()


def render_overview(get_text, district_data, district, get_district_image_path):
    st.markdown(
        f"<div style='text-align:center;margin-bottom:6px'><h1"
        f" style='margin:0;color:#14532d'>{get_text('dashboard_title')}</h1></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div"
        " style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'><div></div><div"
        f" style='color:#6b7280;font-size:14px'>{get_text('updated')}"
        " 00/06/2026</div></div>",
        unsafe_allow_html=True,
    )

    main_left, main_right = st.columns([2, 1.4])

    with main_left:
        st.markdown(
            f"<div class='card'><h4>{get_text('ndvi_map')}</h4></div>",
            unsafe_allow_html=True,
        )
        selected_image = get_district_image_path(district)
        st.image(
            selected_image,
            caption=f"{get_text('ndvi_map')} - {district}",
            use_container_width=True,
        )
        st.markdown(
            "<div"
            " style='display:flex;justify-content:space-between;align-items:center;padding:12px"
            " 0'><span style='font-weight:600;color:#374151'>LOW</span><span"
            " style='font-size:12px;color:#6b7280'>NDVI</span><span"
            " style='font-weight:600;color:#374151'>HIGH</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div"
            " style='height:12px;border-radius:6px;background:linear-gradient(90deg,#d32f2f,#f59e0b,#facc15,#4ade80,#16a34a)'></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='height:12px'></div>", unsafe_allow_html=True
        )

        sim_left, sim_right = st.columns([1, 1])
        with sim_left:
            st.markdown(
                f"<div"
                f" class='card'><h4>{get_text('simulate_planning')}</h4></div>",
                unsafe_allow_html=True,
            )

            # Thanh trượt từ 0% đến 20%
            increase = st.slider(
                get_text("increase_green"),
                min_value=0,
                max_value=20,
                value=10,
                step=1,
                key="overview_slider",
            )

            cur_t = round(float(district_data[district]["temp"]), 1)

            # --- DỰ BÁO BẰNG MODEL AI NẾU CÓ ---
            if ai_model_data:
                model = ai_model_data["model"]
                feature_cols = ai_model_data["features"]

                base_green = district_data[district]["green"]
                base_ndvi = district_data[district]["ndvi"]
                base_oxygen = district_data[district]["oxygen"]

                # Cập nhật thông số biến đổi theo % tăng
                new_green = base_green + increase
                new_ndvi = base_ndvi + (increase * 0.005)
                green_ndvi_ratio = new_green / (new_ndvi + 0.001)

                input_data = {
                    "green_density": new_green,
                    "ndvi": new_ndvi,
                    "oxygen": base_oxygen,
                    "cycle": 1,
                    "sin_day": 0.0,
                    "cos_day": 1.0,
                    "green_ndvi_ratio": green_ndvi_ratio,
                }

                for col in feature_cols:
                    if col.startswith("district_"):
                        dist_name = col.replace("district_", "")
                        input_data[col] = 1 if dist_name == district else 0

                input_df = pd.DataFrame([input_data])[feature_cols]
                predicted_raw = float(model.predict(input_df)[0])

                # Tính mức giảm thực tế và nhiệt độ mới
                new_t = round(predicted_raw, 1)
                reduction = round(cur_t - new_t, 1)

                # Bảo đảm không bị lệch âm bất hợp lý khi slider = 0
                if increase == 0:
                    new_t = cur_t
                    reduction = 0.0
            else:
                # Công thức chuẩn fallback theo cooling_factor của từng quận
                k_t = district_data[district]["cooling_factor"]
                reduction = round(increase * k_t, 1)
                new_t = round(cur_t - reduction, 1)

            st.markdown(
                f"<div"
                " style='display:flex;justify-content:space-between;align-items:center'><div><div"
                " style='color:#6b7280;font-size:12px'>"
                f"{get_text('current_temp')}</div><div"
                " style='font-size:32px;font-weight:700;color:#dc2626'>"
                f"{cur_t:.1f}°C</div></div><div><div"
                " style='color:#6b7280;font-size:12px'>"
                f"{get_text('predicted_temp')}</div><div"
                " style='font-size:32px;font-weight:700;color:#16a34a'>"
                f"{new_t:.1f}°C</div></div></div>",
                unsafe_allow_html=True,
            )

            # --- FIX LỖI 2 DẤU % VÀ FIX DỰ BÁO LẠI ĐÂY ---
            # Xóa dấu % thừa sau {increase}
            st.markdown(
                f"<div style='margin-top:12px;color:#111827'>"
                f"{get_text('simulation_result')} {increase}"
                f" {get_text('percent_temp_decrease')} <span"
                f" style='font-weight:700'>{reduction:.1f}°C</span>.</div>",
                unsafe_allow_html=True,
            )

        with sim_right:
            st.markdown(
                f"<div class='card'><h4>{get_text('ai_evaluation')}</h4></div>",
                unsafe_allow_html=True,
            )
            st.caption(get_text("ai_description"))

        if reduction > 1.5:
            st.success(get_text("ai_good"))
        elif reduction > 0.5:
            st.info(get_text("ai_medium"))
        else:
            st.warning(get_text("ai_warning"))

    with main_right:
        st.markdown(
            f"<div class='card'><h4>{get_text('ndvi_trend')}</h4></div>",
            unsafe_allow_html=True,
        )
        chart_df = pd.DataFrame({
            "year": [2022, 2023, 2024, 2025],
            "NDVI": [0.139158, 0.138037, 0.138251, 0.130112],
        })
        fig = px.line(chart_df, x="year", y="NDVI", markers=True)
        fig.update_traces(line_color="#15807c")
        fig.update_layout(
            height=320,
            margin={"l": 0, "r": 0, "t": 10, "b": 10},
            xaxis=dict(tickmode="linear"),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            "<div style='margin-top:10px'></div>", unsafe_allow_html=True
        )
        metric_row1, metric_row2 = st.columns(2)
        with metric_row1:
            st.markdown(
                f"<div class='metric-card'><div"
                " style='font-size:10px;color:#6b7280'>"
                f"{get_text('ndvi_decrease')}</div><div"
                " style='font-size:20px;font-weight:700;color:#dc2626'>-44.8%</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='metric-card' style='margin-top:10px'><div"
                " style='font-size:10px;color:#6b7280'>"
                f"{get_text('avg_density')}</div><div"
                " style='font-size:20px;font-weight:700;color:#15803d'>21.3%</div></div>",
                unsafe_allow_html=True,
            )
        with metric_row2:
            st.markdown(
                f"<div class='metric-card'><div"
                " style='font-size:10px;color:#6b7280'>"
                f"{get_text('avg_temp')}</div><div"
                " style='font-size:20px;font-weight:700;color:#dc2626'>35.6°C</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='metric-card' style='margin-top:10px'><div"
                " style='font-size:10px;color:#6b7280'>"
                f"{get_text('lacking_green')}</div><div"
                " style='font-size:20px;font-weight:700;color:#b91c1c'>Hai"
                " Bà Trưng</div></div>",
                unsafe_allow_html=True,
            )


def render_ndvi(get_text):
    st.title(get_text("ndvi_map_title"))
    st.image(
        "pictures_greenvision/z8067458909067_a58c022548c89b1053fad1be6a02af15.jpg",
        use_container_width=True,
    )
    st.info(get_text("red_zone"))


def render_analysis(get_text, district_data):
    st.title(get_text("analysis_title"))

    if not district_data:
        st.warning("Không có dữ liệu quận để phân tích.")
        return

    district_df = pd.DataFrame({
        get_text("district"): list(district_data.keys()),
        get_text("temperature"): [district_data[d]["temp"] for d in district_data],
        "NDVI": [district_data[d]["ndvi"] for d in district_data],
        get_text("oxygen"): [district_data[d]["oxygen"] for d in district_data],
    })

    fig = px.bar(
        district_df,
        x=get_text("district"),
        y=get_text("temperature"),
        color=get_text("temperature"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(district_df)