from flask import Flask, request, jsonify
from flask_cors import CORS
import ee

app = Flask(__name__)
CORS(app)

ee.Initialize(project='satellite-imagery-analyzer')

@app.route("/get-image", methods=["POST"])
def get_image():
    coords = request.json.get("coordinates", [])
    if not coords:
        return jsonify({"error": "No coordinates provided"}), 400

    geometry = ee.Geometry.Polygon([coords])

    image = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
         .filterBounds(geometry)
         .filterDate('2024-01-01', '2024-12-31')
         .select(['B4', 'B3', 'B2'])  # Select only RGB bands
         .median()
         .clip(geometry))


    url = image.getThumbURL({
        'region': geometry,
        'format': 'png',
        'bands': ['B4', 'B3', 'B2'],
        'min': 0,
        'max': 3000,
        'scale': 10
    })
 


    return jsonify({"url": url})

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
