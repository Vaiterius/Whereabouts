import { useState } from "react";

import { Map } from "@vis.gl/react-maplibre";
import "maplibre-gl/dist/maplibre-gl.css";

function Trip() {
  const [viewState, setViewState] = useState({
    longitude: -100,
    latitude: 40,
    zoom: 3.5,
  });
  return (
    <Map
      {...viewState}
      onMove={(event) => setViewState(event.viewState)}
      mapStyle={"https://demotiles.maplibre.org/style.json"}
      style={{ width: "100%", height: "100vh" }}
    />
  );
}

export default Trip;
