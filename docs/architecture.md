# EFSAT architecture

## Design goal

EFSAT separates **pixels**, **semantic objects**, and **change events**. Pixels are retained for evidence, but the operational search and communication path is driven by compact, georeferenced events.

## Components

### 1. Ingestion and provenance

The ingestion adapter accepts GeoTIFF/COG scenes, extracts acquisition and sensor metadata, validates CRS/bounds, creates tiles and records a source-scene identifier. Every derived result carries the source scene, model version and processing version.

### 2. Quality and alignment

Cloud, haze, snow, shadow and no-data masks are applied before comparison. Scenes are reprojected and co-registered to reduce false positives caused by viewing geometry or pixel shifts.

### 3. Semantic representation

An image encoder creates tile embeddings and a text encoder creates query embeddings. A vector index supports text-to-image and image-to-image retrieval. Metadata filters are applied before a final relevance rerank.

### 4. Temporal change engine

The change engine combines learned feature differences with spectral indices such as NDVI, NDWI and NDBI. It proposes object-level events such as `NEW_STRUCTURE`, `ROAD_EXPANSION`, `WATER_CHANGE` and `VEGETATION_LOSS`.

### 5. Semantic packet encoder

Stable objects receive persistent IDs. A packet contains an event code, object ID, compact grid coordinate or delta geometry, timestamp, confidence, quality score and provenance reference. High-priority events may attach a small evidence patch.

### 6. Analyst experience

The dashboard provides natural-language search, AOI/date/sensor filters, ranked evidence, timeline context, confidence and confirm/reject feedback. Confirmed feedback can later become a reranking signal.

## Example packet

```json
{
  "event_code": "NEW_STRUCTURE",
  "object_id": "BLDG-204",
  "grid": {"origin": "28.6100,77.2000", "x": 912, "y": 1440, "resolution_m": 1},
  "observed_at": "2026-08-17T10:20:00Z",
  "confidence": 0.94,
  "quality": {"cloud_pct": 2.1, "registration": 0.91},
  "source_scene": "S2A_20260817_TILE_43R",
  "model_version": "changeformer-demo-1"
}
```

## Offline and security posture

Models, weights, imagery and indexes are staged locally before evaluation. Runtime calls do not require cloud services or external APIs. The production packet layer should add signing, replay protection, encryption at rest and role-based analyst access.

## Scaling path

The dependency-free prototype uses JSON and an in-memory index. A production deployment can use PostGIS for spatial metadata, FAISS/Qdrant for vectors, object storage for COGs and a task queue for incremental ingestion. None of those changes require a UI redesign.
