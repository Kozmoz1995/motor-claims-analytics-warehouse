# Dimensional modelling decisions

## Bus matrix

| Business process | Date | Time | Location | Vehicle type | Person role | Factor |
|---|---:|---:|---:|---:|---:|---:|
| Collision | ✓ | ✓ | ✓ |  |  | ✓ |
| Vehicle involvement | ✓ |  | ✓ | ✓ |  | ✓ |
| Person involvement | ✓ |  | ✓ |  | ✓ |  |

## Fact grains

### `fact_collision`

Exactly one row per `collision_id`. Measures include people injured/killed and road-user-specific subtotals. This is an accumulating event fact; the source event is not updated through a workflow of claim statuses.

### `fact_vehicle_involvement`

Exactly one row per source `unique_id` representing one vehicle involved in one collision. `collision_key` is a foreign key to the collision fact and supports drill-across analysis.

### `fact_person_involvement`

Exactly one row per source `unique_id` representing one person involved in one collision. Measures are additive flags such as `is_injured` and `is_killed`.

## Surrogate and natural keys

Warehouse dimensions use integer surrogate keys. Source identifiers remain as durable natural keys for traceability and idempotent loading. Every dimension reserves key `-1` for Unknown.

## Star schema choice

The star model denormalizes borough, ZIP code, coordinates, and street descriptors into `dim_location`. It is the primary BI model because analysts need fewer joins and straightforward filtering.

## Snowflake alternative

The comparison model separates geography into:

```text
dim_location → dim_borough → dim_city → dim_state
```

Advantages:

- less repeated hierarchy text;
- centralized hierarchy governance;
- easier reuse of state and city attributes.

Costs:

- more joins and more complex BI semantics;
- slower ad-hoc exploration in some engines;
- hierarchy changes require coordinated dimension handling.

For this dataset the star schema is the recommended serving model. The snowflake DDL is retained as a learning and architecture-comparison artifact.

## Slowly changing dimensions

- Location and vehicle type are Type 1 because corrections should replace descriptive attributes.
- A future insured-policy dimension would normally use Type 2 to preserve coverage history.
