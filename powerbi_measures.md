# DAX measure catalogue

The generated PBIP keeps measures in the relevant semantic-model table.

```DAX
Total Collisions = COUNTROWS('CollisionOverview')

Severe Collisions =
CALCULATE(
    [Total Collisions],
    'CollisionOverview'[Is Severe] = TRUE()
)

Severe Collision Rate =
DIVIDE([Severe Collisions], [Total Collisions])

People Injured =
SUM('CollisionOverview'[People Injured])

People Killed =
SUM('CollisionOverview'[People Killed])

Avg Severity Score =
AVERAGE('CollisionOverview'[Severity Score])

Review Collisions =
CALCULATE(
    COUNTROWS('AnomalySignals'),
    'AnomalySignals'[Review Status] = "Review"
)

Review Rate =
DIVIDE([Review Collisions], COUNTROWS('AnomalySignals'))

Vehicle Severe Rate =
DIVIDE(
    SUM('VehicleRisk'[Severe Collisions]),
    SUM('VehicleRisk'[Collisions])
)
```

