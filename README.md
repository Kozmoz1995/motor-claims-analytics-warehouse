# Motor Claims Analytics Warehouse

A portfolio-grade data warehouse built from the official NYC Motor Vehicle Collisions datasets. The project demonstrates dimensional modelling, repeatable ETL, data quality, dbt transformations, and the practical trade-offs between star and snowflake schemas.

> The source contains public collision records, not insurance-policy or customer data. “Claims” metrics are analytical risk proxies and must not be interpreted as actual insurer loss amounts.

## Business goal

Give road-safety and motor-insurance analysts a consistent model for answering:

- When and where do severe collisions occur?
- Which vehicle types and contributing factors are associated with higher severity?
- How many vehicles and people are involved in each collision?
- How do collision, injury, and fatality trends change over time?
- Which data-quality issues could distort those conclusions?

## Sources

| Dataset | NYC Open Data ID | Grain |
|---|---|---|
| Crashes | `h9gi-nx95` | One row per collision |
| Vehicles | `bm4k-52h4` | One row per vehicle involved |
| Persons | `f55k-p6yu` | One row per person involved |

The ingestion command uses the official Socrata API and supports incremental date filters and configurable limits.

## Architecture

```mermaid
flowchart TD
    A[NYC Open Data API] --> B[Raw JSONL]
    B --> C[Python quality gate]
    C --> D[PostgreSQL staging]
    D --> E[dbt intermediate models]
    E --> F[Star schema marts]
    E --> G[Snowflake alternative]
    F --> H[Analytics and BI]
```

## Dimensional model

The primary production design is a star schema because it keeps BI queries simple and fast.

```mermaid
erDiagram
    FACT_COLLISION }o--|| DIM_DATE : crash_date
    FACT_COLLISION }o--|| DIM_TIME : crash_time
    FACT_COLLISION }o--|| DIM_LOCATION : location
    FACT_VEHICLE_INVOLVEMENT }o--|| FACT_COLLISION : collision
    FACT_VEHICLE_INVOLVEMENT }o--|| DIM_VEHICLE_TYPE : vehicle_type
    FACT_PERSON_INVOLVEMENT }o--|| FACT_COLLISION : collision
    FACT_PERSON_INVOLVEMENT }o--|| DIM_PERSON_ROLE : person_role
```

Detailed grain decisions and the snowflake comparison are in [docs/dimensional_model.md](docs/dimensional_model.md).

## Quick start

Requires Python 3.11+. The lightweight sample pipeline uses only the standard library.

```bash
python -m src.motor_dwh.cli validate-sample
python -m unittest discover -s tests -v
```

Download a bounded slice from the public API:

```bash
python -m src.motor_dwh.cli extract \
  --dataset crashes \
  --limit 10000 \
  --since 2025-01-01 \
  --output data/raw/crashes.jsonl
```

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run dbt after installing `dbt-postgres` and configuring the included profile example:

```bash
dbt seed
dbt run
dbt test
dbt docs generate
```

## Layers

| Layer | Purpose |
|---|---|
| `raw` | Immutable API payloads with ingestion metadata |
| `staging` | Renamed, typed, and minimally cleaned source records |
| `intermediate` | Reusable joins and derived severity rules |
| `marts` | Star schema facts and dimensions for analytics |
| `snowflake` | Normalized location hierarchy for comparison |

## Repository map

```text
src/motor_dwh/       Extraction and quality logic
data/sample/         Small deterministic fixtures
models/              dbt staging, intermediate, and marts
sql/                 DDL and analyst queries
docs/                Requirements, grain, and modelling decisions
tests/               Unit tests
```

## Quality controls

- required collision identifiers;
- valid latitude and longitude ranges;
- non-negative injury and fatality counts;
- collision totals reconciled with person-level fields;
- duplicate natural-key detection;
- accepted-values and relationship tests in dbt;
- source freshness metadata through `ingested_at`.

## Portfolio skills demonstrated

Dimensional modelling, fact grain selection, conformed dimensions, surrogate keys, star vs snowflake trade-offs, incremental ingestion, idempotency, data contracts, data-quality tests, SQL analytics, PostgreSQL, dbt, Docker, and CI.

## License

MIT. Dataset terms remain governed by NYC Open Data.
