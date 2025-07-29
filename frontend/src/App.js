import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import L from "leaflet";
import "leaflet-draw";
import axios from "axios";

const DrawControl = ({ setImageUrl, setLoading }) => {
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
        const res = await axios.post("http://localhost:5000/get-image", {
          coordinates: coords
        });
        setImageUrl(res.data.url);
      } catch (err) {
        console.error(err);
        alert("Error fetching image.");
      } finally {
        setLoading(false);
      }
    });
  }, [map, setImageUrl, setLoading]);

  return null;
};

export default function App() {
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div>
      <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: "70vh" }}>
        <TileLayer
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <DrawControl setImageUrl={setImageUrl} setLoading={setLoading} />
      </MapContainer>
      <div style={{ padding: "10px", textAlign: "center" }}>
        {loading && <p>Fetching image from Google Earth Engine...</p>}
        {imageUrl && !loading && (
          <div>
            <p><strong>Satellite Image:</strong></p>
            <img src={imageUrl} alt="Satellite Preview" style={{ maxWidth: "90%" }} />
            <br />
            <a href={imageUrl} target="_blank" download="gee_image.png">Download Image</a>
          </div>
        )}
      </div>
    </div>
  );
}
