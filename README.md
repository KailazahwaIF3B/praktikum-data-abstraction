# Laporan Artefak Data Abstraction & Data Ingestion Multi-DBMS

## 1. Ringkasan Klasifikasi Atribut (Table & Attributes)
- **Categorical (Nominal)**: `cluster_group` - Kategori pembeda tanpa tingkatan.
- **Ordered (Ordinal)**: `severity_level` - Memiliki urutan (*Low < Medium < High < Critical*).
- **Ordered (Quantitative)**: `metric_value`, `latency_ms` - Nilai numerik terukur.

## 2. Abstraksi Network & Spatial
- **Network Topology**: Menghubungkan `source_node` dan `target_node` dengan bobot `latency_ms`.
- **Spatial**: Koordinat geografis `latitude` dan `longitude` berstandar WGS84.
- **Temporal**: Indeks timestamp berformat terurut ISO-8601.