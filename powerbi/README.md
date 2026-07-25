# Motor Claims Intelligence — Power BI

Open `MotorClaimsIntelligence.pbip` after running PostgreSQL and `dbt build`.

Required Power BI preview features:

- Power BI Project (.pbip)
- Store semantic model using TMDL format
- Store reports using enhanced metadata format (PBIR)

If PostgreSQL is not local, update the `Server` and `Database` parameters in
Power Query. The report imports four views from the `reporting` schema.

The anomaly page contains explainable review indicators. It does not determine
fraud, guilt, fault, or insurance price.
