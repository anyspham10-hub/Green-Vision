import pandas as pd

# ==========================
# ĐỌC DỮ LIỆU THÔ
# ==========================

df = pd.read_excel("Bao_Cao_HaNoi_Landsat8_2022_2025.xlsx")

# Đổi tên cột

df.columns = [
    "period",
    "district",
    "ndvi",
    "green_density",
    "temperature",
    "oxygen"
]

# ==========================
# XÓA DỮ LIỆU RỖNG
# ==========================

df = df.dropna()

# ==========================
# LƯU DATABASE ĐẦY ĐỦ
# ==========================

df.to_csv(
    "hanoi_database.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================
# TỔNG HỢP THEO QUẬN
# ==========================

dashboard = (
    df.groupby("district")
      .agg(
          total_period=("period","count"),

          avg_ndvi=("ndvi","mean"),
          max_ndvi=("ndvi","max"),
          min_ndvi=("ndvi","min"),
          
          avg_green_density=("green_density","mean"),
          max_green_density=("green_density","max"),
          min_green_density=("green_density","min"),
          
          avg_temperature=("temperature","mean"),
          max_temperature=("temperature","max"),
          min_temperature=("temperature","min"),

          avg_oxygen=("oxygen","mean"),
          max_oxygen=("oxygen","max"),
          min_oxygen=("oxygen","min")
      )
      .reset_index()
)

dashboard.to_csv(
    "dashboard_data.csv",
    index=False,
    encoding="utf-8-sig"
)
# Lấy năm từ cột Chu kỳ
df["year"] = df["period"].str.extract(r"(\d{4})").astype(int)

# Tính NDVI trung bình theo năm
ndvi_year = (
    df.groupby("year")["ndvi"]
      .mean()
      .reset_index()
)

print(ndvi_year)
print("Đã tạo xong database.")