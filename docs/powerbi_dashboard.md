# Motor Claims Intelligence Dashboard

## Purpose

This dashboard turns the dimensional warehouse into an analyst-facing decision
surface for collision frequency, severity, vehicle benchmarks, geographic
hotspots, and explainable anomaly-review indicators.

It is designed as a motor-insurance portfolio project, but the underlying source
is public NYC collision data. Measures such as `severity score`, `risk segment`,
and `review status` are analytical proxies. They are not claim amounts, fraud
decisions, liability decisions, or insurance prices.

## Data contract

Power BI imports four PostgreSQL views maintained by dbt:

| Power BI table | dbt view | Grain |
|---|---|---|
| CollisionOverview | `reporting.rpt_collision_overview` | One collision |
| VehicleRisk | `reporting.rpt_vehicle_risk` | One vehicle type |
| Hotspot | `reporting.rpt_hotspot` | One street/coordinate combination |
| AnomalySignals | `reporting.rpt_fraud_signal_proxy` | One collision |

## Pages

### Executive Overview

Headline volume and severity KPIs, borough comparison, monthly pattern, and
year filtering.

### Severity & Risk

Severity-score distribution, vulnerable road-user metrics, risk segments, and
contributing-factor comparison.

### Anomaly Signal Explorer

Explainable review indicators based on night events, multi-vehicle events,
missing geocodes, unspecified factors, high injury counts, and weekends.
Indicators support review prioritization only.

### Vehicle Risk Profile

Vehicle involvement volume, severe-collision rate, average severity,
within-population ranking, and quartile segmentation.

### Geographic Hotspots

Borough/street collision counts, severity rate, and within-borough hotspot rank.

### Collision Detail

Auditable collision-grain table with borough, street, time, factor, casualty,
and severity attributes.

## Interaction design

- global-style slicers for year, borough, risk segment, review status, and risk quartile;
- cross-filtering from bar charts into KPI cards and detail tables;
- dedicated detail page for auditability;
- consistent 1280×720 layout;
- no custom visuals, so the project remains portable.

## Measure definitions

| Measure | Definition |
|---|---|
| Total Collisions | Row count at collision grain |
| Severe Collisions | Collision rows where `is_severe = true` |
| Severe Collision Rate | Severe collisions / total collisions |
| Avg Severity Score | Average weighted casualty proxy |
| Review Collisions | Rows where explainable `review_status = Review` |
| Review Rate | Review collisions / all anomaly rows |
| Vehicle Severe Rate | Severe vehicle-linked collisions / vehicle-linked collisions |

## Refresh

1. Start PostgreSQL with `docker compose up -d postgres`.
2. Load the source tables and run `dbt build`.
3. Open `powerbi/MotorClaimsIntelligence.pbip`.
4. Update Power Query parameters `Server` and `Database` if necessary.
5. Refresh the semantic model.

