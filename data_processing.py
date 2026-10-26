import os

def build_district_data(df):
    df = df.copy()
    df['district'] = df['district'].astype(str).str.strip()
    df = df.set_index('district')

    district_data = {}
    for district, row in df.iterrows():
        avg_temp = float(row.get('avg_temperature', 0))
        avg_oxygen = float(row.get('avg_oxygen', 0))
        avg_ndvi = float(row.get('avg_ndvi', 0))
        avg_green_density = float(row.get('avg_green_density', 0))

        district_data[district] = {
            'temp': round(avg_temp, 1),
            'oxygen': round(avg_oxygen, 1),
            'ndvi': round(avg_ndvi, 3),
            'green': int(round(avg_green_density)),
            'cooling_factor': max(0.08, min(0.18, 0.12 + (0.35 - avg_ndvi) * 0.1)),
            'oxygen_factor': max(0.07, min(0.16, 0.1 + (0.35 - avg_ndvi) * 0.08))
        }

    return district_data

# Mapping ảnh NDVI cho từng quận (dùng ảnh hiện có trong thư mục pictures_greenvision)
district_image_map = {
    "Ba Dinh": "pictures_greenvision/z8067458746312_284fa5b7914860615b00058ffd4782e7.jpg",
    "Cau Giay": "pictures_greenvision/z8067458755412_d4ea8ea76083562dd1454ed04e579f62.jpg",
    "Dong Anh": "pictures_greenvision/z8067458755781_7dc28295ce8d7aab2ca310ee4a40daee.jpg",
    "Dong Da": "pictures_greenvision/z8067458758893_730fd87ff1b75bcf4f8aec6bf177c101.jpg",
    "Gia Lam": "pictures_greenvision/z8067458768058_84af7183769437c8e2a9aa792cdeba94.jpg",
    "Hai Ba Trung": "pictures_greenvision/z8067458777233_fab8c59b133957c16f8f218d6721f057.jpg",
    "Hoan Kiem": "pictures_greenvision/z8067458798250_574d02762124c7fc08271d415dbd71b1.jpg",
    "Hoang Mai": "pictures_greenvision/z8067458798672_fb2bf1111a3c853df8cd40cdb3e64d0b.jpg",
    "Long Bien": "pictures_greenvision/z8067458803102_fbaeeb5d90f65b0f9db1b3559418b9e2.jpg",
    "Soc Son": "pictures_greenvision/z8067458827986_ed5cbd9b4ed2e506d2a6ae915160fb43.jpg",
    "Tay Ho": "pictures_greenvision/z8067458829039_51797f55da6d0b124ace75529d8bb60b.jpg",
    "Thanh Tri": "pictures_greenvision/z8067458842131_ce693633a37e945c642b104187335d20.jpg",
    "Thanh Xuan": "pictures_greenvision/z8067458847772_3cbbaaec8c3470e2dc367852c6b19c05.jpg",
    "Tu Lien": "pictures_greenvision/z8067458852643_6fdf8ca00feae2264f5bdf7df0a2f655.jpg",
}

default_district_image = "pictures_greenvision/z8067458909067_a58c022548c89b1053fad1be6a02af15.jpg"

def get_district_image_path(district_name):
    image_path = district_image_map.get(district_name, default_district_image)
    if isinstance(image_path, str) and image_path.startswith("http"):
        return image_path
    if os.path.exists(image_path):
        return image_path
    return default_district_image
