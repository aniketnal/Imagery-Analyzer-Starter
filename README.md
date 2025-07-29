# 🌍 Satellite Imagery Analyzer

## Description
A web application for analyzing satellite imagery that allows users to:
- Draw polygons on an interactive map (React + Leaflet)
- Process selected regions through Flask backend
- Access Sentinel-2 imagery via Google Earth Engine
- Download high-resolution satellite images as PNG

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/satellite-imagery-analyzer.git
cd satellite-imagery-analyzer

# Frontend setup
cd frontend
npm install

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
# Start frontend (http://localhost:3000)
cd frontend
npm start

# Start backend (http://localhost:5000)
cd backend
python app.py
```


## License
[MIT](https://choosealicense.com/licenses/mit/)