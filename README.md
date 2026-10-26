# Green-Vision

🌿 Dashboard phân tích không gian xanh đô thị Hà Nội từ ảnh vệ tinh Landsat 8 (2022–2025). Tính NDVI, mật độ cây xanh, nhiệt độ bề mặt và mô phỏng tác động của phủ xanh đến nhiệt độ bằng mô hình AI (Extra Trees + Google Earth Engine + Streamlit).

## Giới thiệu

Dự án sử dụng ảnh vệ tinh Landsat 8 (qua Google Earth Engine) để:
- Tính chỉ số thực vật **NDVI** cho từng quận/huyện
- Ước lượng **% diện tích cây xanh**
- Phân tích **nhiệt độ bề mặt** và **nồng độ oxy**
- **Mô phỏng** ảnh hưởng của việc tăng cây xanh đến nhiệt độ
  bằng mô hình học máy (Extra Trees Regressor)

## Nguồn dữ liệu

- **Vệ tinh:** Landsat 8 Collection 2 Tier 1 Level 2
- **Bộ lọc:** `FAO/GAUL/2015/level2` – ranh giới hành chính Hà Nội
- **Chu kỳ:** 92 chu kỳ × 16 ngày (01/01/2022 → 27/12/2025)
- **Quận/huyện:** Ba Đình, Cầu Giấy, Đông Anh, Đống Đa, Gia Lâm,
  Hai Bà Trưng, Hoàn Kiếm, Hoàng Mai, Long Biên, Sóc Sơn,
  Tây Hồ, Thanh Trì, Thanh Xuân, Từ Liêm

## Cấu trúc dự án
├── data.py # Script GEE extract dữ liệu Landsat
├── process_data.py # Xử lý file Excel → CSV
├── data_processing.py # Chuẩn hóa dữ liệu theo quận
├── load_data.py # Hàm load dữ liệu
├── page_manager.py # Giao diện Streamlit
├── rf_temperature_model.pkl # Model AI dự đoán nhiệt độ
├── hanoi_database.csv # Dữ liệu đầy đủ theo chu kỳ
├── dashboard_data.csv # Dữ liệu tổng hợp theo quận
├── Bao_Cao_HaNoi_Landsat8_2022_2025.xlsx
└── pictures_greenvision/ # Ảnh NDVI minh họa theo từng quận


## Cài đặt

```bash
# Clone repo
git clone https://github.com/[TÊN_BẠN]/[TÊN_REPO].git
cd [TÊN_REPO]

# Cài đặt thư viện
pip install -r requirements.txt

## requirements.txt:

text
streamlit
pandas
numpy
plotly
scikit-learn
joblib
earthengine-api

## Cách chạy: streamlit run app.py

## Các chỉ số chính
Chỉ số |	Mô tả
NDVI | Normalized Difference Vegetation Index (−1 → 1)
% Cây xanh |	Tỉ lệ diện tích thực vật trên tổng diện tích
Nhiệt độ | Nhiệt độ bề mặt (°C) từ band ST_B10
Oxy	| Hàm lượng oxy ước lượng (%)

## Model ExtraTreesRegressor được huấn luyện với các đặc trưng:

green_density, ndvi, oxygen, cycle

sin_day, cos_day, green_ndvi_ratio

One-hot encoding theo quận

Mục tiêu: dự đoán nhiệt độ bề mặt khi thay đổi mật độ cây xanh.

## Author
Phạm Minh Ánh - anyspham2703@gmail.com
Trần Duy Quang - tranduyquang260@gmail.com
Đặng Bùi Minh Hiếu - danghieu05062006@gmail.com

MIT License
