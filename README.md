# EFSAT

**Event-based Fusion for Semantic Satellite Analytics and Transmission**

EFSAT is an offline-first prototype for discovering meaningful satellite-image content and transmitting compact semantic changes instead of repeatedly moving full-resolution imagery.

> Prototype by **Mithil-7 / Zero Coders**  
> GitHub: https://github.com/Mithil-7/EFSAT

## What this prototype demonstrates

- Natural-language semantic search over indexed satellite observations.
- Ranked change-event review queue with confidence, sensor, date and provenance.
- Interactive AOI map with event markers and change polygons.
- Before/after evidence panel and temporal timeline.
- Compact semantic packet preview for low-bandwidth transmission.
- Local ingestion simulation for GeoTIFF/COG files.
- Offline-ready architecture: no external API is required to run the demo.

The included dataset is synthetic and intended for demonstration. It does not represent classified or operational imagery.

## Run locally

### Option A: Python (recommended)

Requires Python 3.10+.

```bash
cd EFSAT
python server.py
```

Open http://localhost:8080.

### Option B: static preview

Open `web/index.html` directly in a browser. Search and review interactions work; the simulated ingestion endpoint requires the Python server.

## Repository map

See [structure.md](structure.md) for the full project structure and data flow.

## Architecture

See [docs/architecture.md](docs/architecture.md) and [docs/architecture.svg](docs/architecture.svg).

## Prototype scope and next steps

This repository intentionally keeps the demo dependency-free. A production implementation can replace the adapters in `server.py` with Rasterio/GDAL ingestion, a remote-sensing embedding model, ChangeFormer/Siamese change detection, PostGIS and FAISS/Qdrant without changing the UI contract.

1. Add GeoTIFF/COG validation and STAC metadata extraction.
2. Add cloud/shadow masks and image co-registration.
3. Replace deterministic demo ranking with local image/text embeddings.
4. Add vector-index persistence and model/version provenance.
5. Benchmark precision, recall, latency, storage and packet size on held-out imagery.

## Licence

MIT. See [LICENSE](LICENSE).
