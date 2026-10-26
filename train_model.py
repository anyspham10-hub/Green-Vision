import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error
)

def train_and_save_model():
    # 1. Đọc dữ liệu
    df = pd.read_csv("hanoi_database.csv")

    # 2. Làm sạch nhiễu cảm biến vệ tinh
    df_clean = df[(df['temperature'] >= 10.0) & (df['temperature'] <= 45.0)].copy()

    # 3. Trích xuất thuộc tính thời gian
    df_clean['date_str'] = df_clean['period'].str.extract(r'\((.*?)\)')
    df_clean['datetime'] = pd.to_datetime(df_clean['date_str'], format='%d/%m/%Y', errors='coerce')
    df_clean['dayofyear'] = df_clean['datetime'].dt.dayofyear
    df_clean['cycle'] = df_clean['period'].str.extract(r'Chu kỳ (\d+)').astype(int)

    # Chu kỳ thời tiết
    df_clean['sin_day'] = np.sin(2 * np.pi * df_clean['dayofyear'] / 365.25)
    df_clean['cos_day'] = np.cos(2 * np.pi * df_clean['dayofyear'] / 365.25)

    # Feature Engineering
    df_clean['green_ndvi_ratio'] = df_clean['green_density'] / (df_clean['ndvi'] + 0.001)

    # 4. Mã hóa Quận
    df_encoded = pd.get_dummies(df_clean, columns=['district'], drop_first=False)

    # 5. Danh sách thuộc tính
    feature_cols = [
        'green_density', 'ndvi', 'oxygen', 'cycle',
        'sin_day', 'cos_day', 'green_ndvi_ratio'
    ] + [c for c in df_encoded.columns if c.startswith('district_')]

    X = df_encoded[feature_cols]
    y = df_encoded['temperature']

    # 6. Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 7. Huấn luyện mô hình ExtraTreesRegressor tối ưu tham số
    model = ExtraTreesRegressor(
        n_estimators=500,
        max_depth=None,
        min_samples_split=2,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 8. Đánh giá đầy đủ 4 chỉ số
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100

    print(f"--- KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH ---")
    print(f"1. MAE  (Sai số tuyệt đối TB): {mae:.4f} °C")
    print(f"2. MSE  (Bình phương sai số TB): {mse:.4f}")
    print(f"3. RMSE (Căn bình phương sai số): {rmse:.4f} °C")
    print(f"4. R² Score (Hệ số xác định): {r2:.4f} ({r2*100:.2f}%)")
    print(f"5. MAPE (Sai số phần trăm TB): {mape:.2f}%")
    print(f"6. Độ chính xác tương đối: {100 - mape:.2f}%")
    # 9. Lưu mô hình
    joblib.dump({'model': model, 'features': feature_cols}, "rf_temperature_model.pkl")
    print("✅ Đã lưu mô hình vào 'rf_temperature_model.pkl'!")

if __name__ == "__main__":
    train_and_save_model()