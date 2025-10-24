from flask import Flask, request, jsonify
from flask_cors import CORS
import ee
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

ee.Initialize(project='satellite-imagery-analyzer')

# Function to mask clouds in Landsat 8 L2
def maskL8sr(image):
    qa = image.select('QA_PIXEL')
    cloud_mask = qa.bitwiseAnd(1 << 3).eq(0)  # Clear pixels only
    return image.updateMask(cloud_mask)

@app.route("/get-multi-image", methods=["POST"])
def get_multi_image():
    data = request.json
    coords = data.get("coordinates", [])

    if not coords:
        return jsonify({"error": "No coordinates provided"}), 400

    geometry = ee.Geometry.Polygon([coords])
    year_offsets = [0, 3, 5, 7, 10]
    images_urls = []
    today = datetime.today()

    for offset in year_offsets:
        end_date = today - timedelta(days=365 * offset)
        start_date = end_date - timedelta(days=365)  # 1-year window

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Choose collection based on years ago
        if offset <= 5:
            collection_id = 'COPERNICUS/S2_SR_HARMONIZED'  # Sentinel-2
            bands = ['B4', 'B3', 'B2']
            max_val = 3000
        else:
           collection_id = 'LANDSAT/LC08/C02/T1_L2'  
           bands = ['SR_B4', 'SR_B3', 'SR_B2']     
           max_val = 3000                           

        collection = (ee.ImageCollection(collection_id)
                      .filterBounds(geometry)
                      .filterDate(start_date_str, end_date_str)
                      .select(bands))

        if collection.size().getInfo() == 0:
            images_urls.append({"years_ago": offset, "url": None})
            continue

        image = collection.median().clip(geometry)

        url = image.getThumbURL({
            'region': geometry,
            'format': 'png',
            'bands': bands,
            'min': 0,
            'max': max_val,
            'gamma': 1.4,
            'dimensions': [1024, 1024],
            'crs': 'EPSG:4326'
        })

        images_urls.append({"years_ago": offset, "url": url})

    return jsonify({"images": images_urls})


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
