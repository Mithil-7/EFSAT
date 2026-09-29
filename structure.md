# EFSAT project structure

```text
EFSAT/
├── server.py                 # Dependency-free local API and static server
├── README.md                 # Setup, scope and roadmap
├── structure.md              # This file
├── LICENSE
├── docs/
│   ├── architecture.md      # Detailed architecture and decisions
│   └── architecture.svg     # Renderable architecture diagram
├── data/
│   └── demo_events.json      # Synthetic events used by the prototype
└── web/
    ├── index.html            # Application shell
    ├── styles.css            # Dark geospatial dashboard styling
    └── app.js                # Search, map, timeline and review interactions
```

## Runtime flow

1. `server.py` serves `web/` and exposes `/api/events`, `/api/stats` and `/api/ingest`.
2. `web/app.js` loads the event index, applies text/metadata filters and renders the ranked queue.
3. Selecting an event updates the map, evidence panel, timeline and semantic packet.
4. The ingestion control accepts an image file for a realistic UI flow and creates a local queued-ingestion receipt. Production adapters should process the image with GDAL/Rasterio and persist results to PostGIS/vector storage.

## Production boundary

The UI is already separated from the processing boundary by JSON contracts. The demo event objects model the fields that a real pipeline must emit: source scene, acquisition time, geometry, sensor, change type, confidence, quality and processing history.
