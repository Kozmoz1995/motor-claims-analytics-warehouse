# Business requirements

## Stakeholders

- Motor portfolio analyst
- Claims operations manager
- Road-safety analyst
- Data-quality owner

## Required metrics

1. Collision count by day, month, borough, and contributing factor.
2. People injured and killed per collision and per 1,000 collisions.
3. Cyclist, pedestrian, and motorist injury and fatality breakdowns.
4. Vehicles and people involved per collision.
5. Severe-collision count and severity rate.
6. Vehicle-type participation and severe-collision association.
7. Data completeness for location, vehicle type, and person role.

## Definitions

- **Collision:** one unique `collision_id` in the crashes source.
- **Severe collision:** a collision with at least one fatality or three or more injuries.
- **Injury rate:** injured persons divided by collisions in the selected population.
- **Fatality rate:** killed persons divided by collisions in the selected population.
- **Involvement:** participation in a collision; it does not establish fault.

## Guardrails

- Association must not be described as causation.
- Public collision data must not be represented as insurance-claim payments.
- Missing dimension values map to an explicit `Unknown` member.
- Fact table measures must preserve source totals before downstream aggregation.
