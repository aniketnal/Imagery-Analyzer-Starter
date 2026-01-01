from flask import Flask, request, jsonify
from flask_cors import CORS
import ee
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

ee.Initialize(project='satellite-imagery-analyzer')

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
        start_date = end_date - timedelta(days=365)

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Sentinel-2 (preferred)
        if offset <= 7:
            collection_id = 'COPERNICUS/S2_SR_HARMONIZED'
            bands = ['B3', 'B4', 'B8', 'B11']  
            scale = 10
        else:
            # Landsat-8 equivalent bands
            collection_id = 'LANDSAT/LC08/C02/T1_L2'
            bands = ['SR_B3', 'SR_B4', 'SR_B5', 'SR_B6']
            scale = 30

        collection = (
            ee.ImageCollection(collection_id)
            .filterBounds(geometry)
            .filterDate(start_date_str, end_date_str)
            .select(bands)
        )

        if collection.size().getInfo() == 0:
            images_urls.append({"years_ago": offset, "url": None})
            continue

        image = collection.median().clip(geometry)

        # GeoTIFF with bands embedded
        url = image.getDownloadURL({
            'region': geometry,
            'scale': scale,
            'format': 'GEO_TIFF',
            'bands': bands,
            'crs': 'EPSG:4326'
        })

        images_urls.append({
            "years_ago": offset,
            "bands": bands,
            "url": url
        })

    return jsonify({"images": images_urls})


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
