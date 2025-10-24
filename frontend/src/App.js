import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import L from "leaflet";
import "leaflet-draw";
import axios from "axios";

// DrawControl Component
const DrawControl = ({ setImageUrls, setLoading }) => {
  const map = useMap();

  useEffect(() => {
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new L.Control.Draw({
      edit: { featureGroup: drawnItems },
      draw: {
        polygon: true,
        rectangle: true,
        circle: false,
        marker: false,
        polyline: false,
        circlemarker: false
      }
    });

    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, async (event) => {
      const layer = event.layer;
      drawnItems.addLayer(layer);

      const coords = layer.getLatLngs()[0].map(p => [p.lng, p.lat]);
      coords.push(coords[0]); // Close polygon

      try {
        setLoading(true);
        const res = await axios.post("http://localhost:5000/get-multi-image", {
          coordinates: coords
        });
        setImageUrls(res.data.images);
      } catch (err) {
        console.error(err);
        alert("Error fetching images.");
      } finally {
        setLoading(false);
      }
    });
  }, [map, setImageUrls, setLoading]);

  return null;
};

// Main App Component
export default function App() {
  const [imageUrls, setImageUrls] = useState([]);
  const [loading, setLoading] = useState(false);

  return (
    <div>
      <MapContainer center={[19.05, 73.88]} zoom={12} style={{ height: "70vh" }}>
        <TileLayer
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <DrawControl setImageUrls={setImageUrls} setLoading={setLoading} />
      </MapContainer>

      <div style={{ padding: "10px", textAlign: "center" }}>
        {loading && <p>Fetching satellite images from Google Earth Engine...</p>}

        {!loading && imageUrls.length > 0 && (
          <div>
            {imageUrls.map(img => (
              <div key={img.years_ago} style={{ marginBottom: "30px" }}>
                <p><strong>{img.years_ago === 0 ? "Current Year" : `${img.years_ago} Years Ago`}</strong></p>
                {img.url ? (
                  <>
                    <img
                      src={img.url}
                      alt={`Satellite ${img.years_ago} yrs ago`}
                      style={{ maxWidth: "90%" }}
                    />
                    <br />
                    <a
                      href={img.url}
                      target="_blank"
                      download={`gee_image_${img.years_ago}yr.png`}
                      rel="noreferrer"
                    >
                      Download Image
                    </a>
                  </>
                ) : (
                  <p style={{ color: "red" }}>No image available for this timeframe.</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
