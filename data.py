import ee

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# 1. Lấy ranh giới hành chính Hà Nội
hanoi_districts = ee.FeatureCollection('FAO/GAUL/2015/level2') \
    .filter(ee.Filter.Or(
        ee.Filter.eq('ADM1_NAME', 'Ha Noi'),
        ee.Filter.eq('ADM1_NAME', 'Hà Nội'),
        ee.Filter.eq('ADM1_NAME', 'Ha Noi City')
    ))

# 2. Tạo dummy image phòng trường hợp chu kỳ không có ảnh Landsat
sample_img = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
    .filterBounds(hanoi_districts) \
    .filterDate('2022-01-01', '2025-12-31') \
    .first() \
    .select(['SR_B4', 'SR_B5', 'ST_B10'])

dummy_image = sample_img.updateMask(ee.Image.constant(0))

# 3. Thiết lập thời gian (92 chu kỳ 16 ngày từ 01/01/2022)
start_date = ee.Date('2022-01-01')
total_periods = 92
period_sequence = ee.List.sequence(0, total_periods - 1)

# 4. Hàm lọc mây vệ tinh (Bitmask QA_PIXEL)
def mask_l8_sr(image):
    qa = image.select('QA_PIXEL')
    mask = qa.bitwiseAnd(1 << 3).eq(0).And(qa.bitwiseAnd(1 << 5).eq(0))
    return image.updateMask(mask)

# 5. Hàm xử lý từng chu kỳ 16 ngày
def process_period(period_offset):
    offset_num = ee.Number(period_offset)
    start = start_date.advance(offset_num.multiply(16), 'day')
    end = start.advance(16, 'day')
    
    date_str = start.format('dd/MM/yyyy')
    period_label = ee.String('Chu kỳ ') \
        .cat(offset_num.add(1).int().format()) \
        .cat(' (') \
        .cat(date_str) \
        .cat(')')
    
    base_collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterBounds(hanoi_districts) \
        .filterDate(start, end) \
        .map(mask_l8_sr) \
        .select(['SR_B4', 'SR_B5', 'ST_B10'])
    
    combined_image = ee.ImageCollection([dummy_image]).merge(base_collection).mosaic()
    
    # Tính NDVI và Nhiệt độ gốc (°C)
    ndvi = combined_image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    thermal = combined_image.select('ST_B10') \
        .multiply(0.00341802) \
        .add(149.0) \
        .subtract(273.15) \
        .rename('Temperature')
    
    processed_image = ndvi.addBands(thermal)
    
    # Tính thống kê cho từng quận/huyện
    def calc_district_stats(district):
        district_name = district.get('ADM2_NAME')
        
        stats = processed_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=district.geometry(),
            scale=30,
            maxPixels=1e9
        )
        
        return ee.Feature(None, {
            'Period': periodLabel,
            'District': district_name,
            'NDVI': stats.get('NDVI'),
            'Temperature': stats.get('Temperature')
        })
    
    # Sửa biến nhãn periodLabel cho đúngscope
    district_stats = hanoi_districts.map(lambda district: ee.Feature(None, {
        'Period': period_label,
        'District': district.get('ADM2_NAME'),
        'NDVI': processed_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=district.geometry(),
            scale=30,
            maxPixels=1e9
        ).get('NDVI'),
        'Temperature': processed_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=district.geometry(),
            scale=30,
            maxPixels=1e9
        ).get('Temperature')
    }))
    
    return district_stats

# 6. Chạy lặp qua tất cả các chu kỳ và gộp kết quả
periodic_data = period_sequence.map(process_period)
final_collection = ee.FeatureCollection(periodic_data).flatten()

# 7. Xuất file CSV lên Google Drive
task = ee.batch.Export.table.toDrive(
    collection=final_collection,
    description='Du_Lieu_Goc_Landsat8_Hanoi_2022_2025',
    fileFormat='CSV',
    selectors=['Period', 'District', 'NDVI', 'Temperature']
)

# Kích hoạt tiến trình export
task.start()

print("🚀 Đã gửi yêu cầu xuất file 'Du_Lieu_Goc_Landsat8_Hanoi_2022_2025' lên Google Drive thành công!")
print("Kiểm tra tiến trình tại: https://code.earthengine.google.com/tasks")