"""Generate the source-controlled PBIP dashboard for the portfolio project."""

from pathlib import Path
import json
import shutil
import uuid

ROOT = Path(__file__).resolve().parents[1]
POWERBI = ROOT / "powerbi"
REPORT = POWERBI / "MotorClaimsIntelligence.Report"
MODEL = POWERBI / "MotorClaimsIntelligence.SemanticModel"

if POWERBI.exists():
    shutil.rmtree(POWERBI)
(REPORT / "definition" / "pages").mkdir(parents=True)
(MODEL / ".pbi").mkdir(parents=True)
(MODEL / "definition" / "tables").mkdir(parents=True)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


write_json(
    POWERBI / "MotorClaimsIntelligence.pbip",
    {
        "version": "1.0",
        "artifacts": [{"report": {"path": "MotorClaimsIntelligence.Report"}}],
        "settings": {"enableAutoRecovery": True},
    },
)
write_json(
    REPORT / "definition.pbir",
    {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": "../MotorClaimsIntelligence.SemanticModel"}},
    },
)
write_json(
    MODEL / "definition.pbism",
    {"version": "4.0", "settings": {"qnaEnabled": True}},
)
write_json(
    MODEL / ".pbi" / "editorSettings.json",
    {
        "version": "1.0",
        "showHiddenFields": True,
        "parallelQueryLoading": True,
        "relationshipImportEnabled": False,
        "shouldNotifyUserOfNameConflictResolution": True,
    },
)
for folder, item_type in ((REPORT, "Report"), (MODEL, "SemanticModel")):
    write_json(
        folder / ".platform",
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
            "metadata": {"type": item_type, "displayName": "Motor Claims Intelligence"},
            "config": {"version": "2.0", "logicalId": str(uuid.uuid4())},
        },
    )

definition = REPORT / "definition"
write_json(
    definition / "version.json",
    {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0",
    },
)
write_json(
    definition / "report.json",
    {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
        "layoutOptimization": "None",
        "themeCollection": {
            "baseTheme": {
                "name": "CY24SU06",
                "reportVersionAtImport": "5.55",
                "type": "SharedResources",
            }
        },
    },
)

pages = [
    ("ReportSection01", "Executive Overview"),
    ("ReportSection02", "Severity & Risk"),
    ("ReportSection03", "Anomaly Signal Explorer"),
    ("ReportSection04", "Vehicle Risk Profile"),
    ("ReportSection05", "Geographic Hotspots"),
    ("ReportSection06", "Collision Detail"),
]
write_json(
    definition / "pages" / "pages.json",
    {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
        "pageOrder": [p[0] for p in pages],
        "activePageName": pages[0][0],
    },
)


def col(entity, prop, active=False):
    result = {
        "field": {
            "Column": {
                "Expression": {"SourceRef": {"Entity": entity}},
                "Property": prop,
            }
        },
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop,
    }
    if active:
        result["active"] = True
    return result


def measure(entity, prop):
    return {
        "field": {
            "Measure": {
                "Expression": {"SourceRef": {"Entity": entity}},
                "Property": prop,
            }
        },
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop,
    }


def visual(page_id, visual_type, query_state, x, y, width, height, order, objects=None):
    visual_id = uuid.uuid4().hex[:20]
    payload = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": visual_id,
        "position": {
            "x": x,
            "y": y,
            "z": order * 1000,
            "height": height,
            "width": width,
            "tabOrder": order * 1000,
        },
        "visual": {"visualType": visual_type},
    }
    if query_state:
        payload["visual"]["query"] = {"queryState": query_state}
    if objects:
        payload["visual"]["objects"] = objects
    target = definition / "pages" / page_id / "visuals" / visual_id
    target.mkdir(parents=True, exist_ok=True)
    write_json(target / "visual.json", payload)


def textbox(page_id, text, x=24, y=12, width=900, height=60, order=0):
    objects = {
        "general": [
            {
                "properties": {
                    "paragraphs": [
                        {
                            "textRuns": [
                                {
                                    "value": text,
                                    "textStyle": {
                                        "fontFamily": "Segoe UI Semibold",
                                        "fontSize": "24px",
                                        "color": "#14213D",
                                    },
                                }
                            ],
                            "horizontalTextAlignment": "left",
                        }
                    ]
                }
            }
        ]
    }
    visual(page_id, "textbox", None, x, y, width, height, order, objects)


def card(page_id, metric, x, y, width=220, height=108, order=1):
    visual(
        page_id,
        "cardVisual",
        {"Data": {"projections": [measure("CollisionOverview", metric)]}},
        x,
        y,
        width,
        height,
        order,
    )


def card_from(page_id, entity, metric, x, y, width=220, height=108, order=1):
    visual(
        page_id,
        "cardVisual",
        {"Data": {"projections": [measure(entity, metric)]}},
        x,
        y,
        width,
        height,
        order,
    )


def slicer(page_id, entity, field, title, x, y, width=220, height=82, order=1):
    visual(
        page_id,
        "slicer",
        {"Values": {"projections": [col(entity, field)]}},
        x,
        y,
        width,
        height,
        order,
        {
            "data": [{"properties": {"mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}}}],
            "header": [
                {
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": repr(title)}}},
                    }
                }
            ],
        },
    )


def bar(page_id, entity, category, metric_entity, metric, x, y, width, height, order):
    visual(
        page_id,
        "barChart",
        {
            "Category": {"projections": [col(entity, category, active=True)]},
            "Y": {"projections": [measure(metric_entity, metric)]},
        },
        x,
        y,
        width,
        height,
        order,
    )


def table(page_id, fields, x, y, width, height, order):
    projections = [
        measure(entity, prop) if kind == "measure" else col(entity, prop)
        for entity, prop, kind in fields
    ]
    visual(
        page_id,
        "tableEx",
        {"Values": {"projections": projections}},
        x,
        y,
        width,
        height,
        order,
        {
            "columnHeaders": [
                {
                    "properties": {
                        "columnAdjustment": {"expr": {"Literal": {"Value": "'growToFit'"}}},
                        "autoSizeColumnWidth": {"expr": {"Literal": {"Value": "true"}}},
                    }
                }
            ]
        },
    )


for page_id, title in pages:
    page_dir = definition / "pages" / page_id
    (page_dir / "visuals").mkdir(parents=True, exist_ok=True)
    write_json(
        page_dir / "page.json",
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
            "name": page_id,
            "displayName": title,
            "displayOption": "FitToPage",
            "height": 720,
            "width": 1280,
        },
    )

# 1 | Executive Overview
p = pages[0][0]
textbox(p, "MOTOR CLAIMS INTELLIGENCE  |  EXECUTIVE OVERVIEW")
card(p, "Total Collisions", 24, 80, order=1)
card(p, "Severe Collisions", 260, 80, order=2)
card(p, "People Injured", 496, 80, order=3)
card(p, "Severe Collision Rate", 732, 80, order=4)
slicer(p, "CollisionOverview", "Year", "Year", 968, 24, 280, 82, 5)
bar(p, "CollisionOverview", "Borough", "CollisionOverview", "Total Collisions", 24, 220, 585, 460, 6)
bar(p, "CollisionOverview", "Month", "CollisionOverview", "Total Collisions", 633, 220, 615, 460, 7)

# 2 | Severity
p = pages[1][0]
textbox(p, "SEVERITY & RISK  |  WHO, WHERE AND WHY")
card(p, "Avg Severity Score", 24, 80, order=1)
card(p, "People Killed", 260, 80, order=2)
card(p, "Pedestrians Injured", 496, 80, order=3)
card(p, "Cyclists Injured", 732, 80, order=4)
slicer(p, "CollisionOverview", "Risk Segment", "Risk segment", 968, 24, 280, 82, 5)
bar(p, "CollisionOverview", "Risk Segment", "CollisionOverview", "Total Collisions", 24, 220, 500, 460, 6)
bar(p, "CollisionOverview", "Primary Factor", "CollisionOverview", "Severe Collisions", 548, 220, 700, 460, 7)

# 3 | Anomaly signals
p = pages[2][0]
textbox(p, "ANOMALY SIGNAL EXPLORER  |  EXPLAINABLE REVIEW INDICATORS")
card_from(p, "AnomalySignals", "Review Collisions", 24, 80, order=1)
card_from(p, "AnomalySignals", "Review Rate", 260, 80, order=2)
card_from(p, "AnomalySignals", "Night Events", 496, 80, order=3)
card_from(p, "AnomalySignals", "Multi Vehicle Events", 732, 80, order=4)
slicer(p, "AnomalySignals", "Review Status", "Review status", 968, 24, 280, 82, 5)
bar(p, "AnomalySignals", "Borough", "AnomalySignals", "Review Collisions", 24, 220, 585, 460, 6)
table(
    p,
    [
        ("AnomalySignals", "Collision ID", "column"),
        ("AnomalySignals", "Crash Date", "column"),
        ("AnomalySignals", "Borough", "column"),
        ("AnomalySignals", "Anomaly Score", "column"),
        ("AnomalySignals", "Review Status", "column"),
    ],
    633,
    220,
    615,
    460,
    7,
)

# 4 | Vehicle risk
p = pages[3][0]
textbox(p, "VEHICLE RISK PROFILE  |  BENCHMARKS & QUARTILES")
card_from(p, "VehicleRisk", "Vehicle Involvements", 24, 80, order=1)
card_from(p, "VehicleRisk", "Vehicle Severe Rate", 260, 80, order=2)
slicer(p, "VehicleRisk", "Risk Quartile", "Risk quartile", 968, 24, 280, 82, 3)
bar(p, "VehicleRisk", "Vehicle Type", "VehicleRisk", "Avg Vehicle Severity", 24, 220, 660, 460, 4)
table(
    p,
    [
        ("VehicleRisk", "Vehicle Type", "column"),
        ("VehicleRisk", "Collisions", "column"),
        ("VehicleRisk", "Severe Collisions", "column"),
        ("VehicleRisk", "Severe Collision Rate", "column"),
        ("VehicleRisk", "Severity Rank", "column"),
        ("VehicleRisk", "Risk Quartile", "column"),
    ],
    708,
    220,
    540,
    460,
    5,
)

# 5 | Hotspots
p = pages[4][0]
textbox(p, "GEOGRAPHIC HOTSPOTS  |  LOCATION-BASED RISK")
card_from(p, "Hotspot", "Hotspot Collisions", 24, 80, order=1)
card_from(p, "Hotspot", "Hotspot Severe Collisions", 260, 80, order=2)
slicer(p, "Hotspot", "Borough", "Borough", 968, 24, 280, 82, 3)
bar(p, "Hotspot", "Street", "Hotspot", "Hotspot Collisions", 24, 220, 660, 460, 4)
table(
    p,
    [
        ("Hotspot", "Borough", "column"),
        ("Hotspot", "ZIP Code", "column"),
        ("Hotspot", "Street", "column"),
        ("Hotspot", "Collisions", "column"),
        ("Hotspot", "Severe Collision Rate", "column"),
        ("Hotspot", "Borough Rank", "column"),
    ],
    708,
    220,
    540,
    460,
    5,
)

# 6 | Collision detail
p = pages[5][0]
textbox(p, "COLLISION DETAIL  |  AUDITABLE EVENT GRAIN")
slicer(p, "CollisionOverview", "Borough", "Borough", 24, 80, 280, 82, 1)
slicer(p, "CollisionOverview", "Severity Band", "Severity", 324, 80, 280, 82, 2)
slicer(p, "CollisionOverview", "Primary Factor", "Primary factor", 624, 80, 350, 82, 3)
table(
    p,
    [
        ("CollisionOverview", "Collision ID", "column"),
        ("CollisionOverview", "Crash Date", "column"),
        ("CollisionOverview", "Crash Time", "column"),
        ("CollisionOverview", "Borough", "column"),
        ("CollisionOverview", "Street", "column"),
        ("CollisionOverview", "Primary Factor", "column"),
        ("CollisionOverview", "Severity Band", "column"),
        ("CollisionOverview", "People Injured", "column"),
        ("CollisionOverview", "People Killed", "column"),
    ],
    24,
    200,
    1224,
    480,
    4,
)

# Semantic model
(MODEL / "definition" / "database.tmdl").write_text(
    "database Unknown\n\tcompatibilityLevel: 1601\n\tcompatibilityMode: powerBI\n",
    encoding="utf-8",
)
table_names = ["CollisionOverview", "VehicleRisk", "Hotspot", "AnomalySignals"]
(MODEL / "definition" / "model.tmdl").write_text(
    """model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tdiscourageImplicitMeasures
\tsourceQueryCulture: en-US
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

"""
    + "".join(f"ref table {name}\n" for name in table_names),
    encoding="utf-8",
)
(MODEL / "definition" / "expressions.tmdl").write_text(
    f"""expression Server = "localhost" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
\tlineageTag: {uuid.uuid4()}

expression Database = "motor_dwh" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
\tlineageTag: {uuid.uuid4()}
""",
    encoding="utf-8",
)

schemas = {
    "CollisionOverview": (
        "rpt_collision_overview",
        [
            ("Collision ID", "collision_key", "string"),
            ("Crash Date", "crash_date", "dateTime"),
            ("Year", "year_number", "int64"),
            ("Quarter", "quarter_number", "int64"),
            ("Month Number", "month_number", "int64"),
            ("Month", "month_name", "string"),
            ("Day", "day_name", "string"),
            ("Is Weekend", "is_weekend", "boolean"),
            ("Crash Time", "crash_time_key", "int64"),
            ("Is Night", "is_night", "boolean"),
            ("Borough", "borough", "string"),
            ("ZIP Code", "zip_code", "string"),
            ("Street", "on_street_name", "string"),
            ("Cross Street", "cross_street_name", "string"),
            ("Latitude", "latitude", "double"),
            ("Longitude", "longitude", "double"),
            ("Primary Factor", "primary_factor", "string"),
            ("Severity Band", "severity_band", "string"),
            ("Is Severe", "is_severe", "boolean"),
            ("People Injured", "persons_injured", "int64"),
            ("People Killed", "persons_killed", "int64"),
            ("Pedestrians Injured", "pedestrians_injured", "int64"),
            ("Cyclists Injured", "cyclists_injured", "int64"),
            ("Severity Score", "severity_score", "double"),
            ("Risk Segment", "risk_segment", "string"),
        ],
    ),
    "VehicleRisk": (
        "rpt_vehicle_risk",
        [
            ("Vehicle Type", "vehicle_type", "string"),
            ("Vehicle Involvements", "vehicle_involvements", "int64"),
            ("Collisions", "collisions", "int64"),
            ("Severe Collisions", "severe_collisions", "int64"),
            ("People Injured", "persons_injured", "int64"),
            ("People Killed", "persons_killed", "int64"),
            ("Avg Severity Score", "avg_severity_score", "double"),
            ("Severe Collision Rate", "severe_collision_rate", "double"),
            ("Severity Rank", "severity_rank", "int64"),
            ("Risk Quartile", "risk_quartile", "int64"),
        ],
    ),
    "Hotspot": (
        "rpt_hotspot",
        [
            ("Borough", "borough", "string"),
            ("ZIP Code", "zip_code", "string"),
            ("Street", "on_street_name", "string"),
            ("Cross Street", "cross_street_name", "string"),
            ("Latitude", "latitude", "double"),
            ("Longitude", "longitude", "double"),
            ("Collisions", "collisions", "int64"),
            ("Severe Collisions", "severe_collisions", "int64"),
            ("People Injured", "persons_injured", "int64"),
            ("People Killed", "persons_killed", "int64"),
            ("Severe Collision Rate", "severe_collision_rate", "double"),
            ("Borough Rank", "borough_hotspot_rank", "int64"),
        ],
    ),
    "AnomalySignals": (
        "rpt_fraud_signal_proxy",
        [
            ("Collision ID", "collision_key", "string"),
            ("Crash Date", "crash_date", "dateTime"),
            ("Borough", "borough", "string"),
            ("Primary Factor", "primary_factor", "string"),
            ("Is Night", "is_night", "boolean"),
            ("Vehicle Count", "vehicle_count", "int64"),
            ("People Injured", "persons_injured", "int64"),
            ("People Killed", "persons_killed", "int64"),
            ("Anomaly Score", "anomaly_signal_score", "int64"),
            ("Review Status", "review_status", "string"),
        ],
    ),
}

measures = {
    "CollisionOverview": {
        "Total Collisions": "COUNTROWS('CollisionOverview')",
        "Severe Collisions": "CALCULATE([Total Collisions], 'CollisionOverview'[Is Severe] = TRUE())",
        "Severe Collision Rate": "DIVIDE([Severe Collisions], [Total Collisions])",
        "People Injured": "SUM('CollisionOverview'[People Injured])",
        "People Killed": "SUM('CollisionOverview'[People Killed])",
        "Pedestrians Injured": "SUM('CollisionOverview'[Pedestrians Injured])",
        "Cyclists Injured": "SUM('CollisionOverview'[Cyclists Injured])",
        "Avg Severity Score": "AVERAGE('CollisionOverview'[Severity Score])",
    },
    "VehicleRisk": {
        "Vehicle Involvements": "SUM('VehicleRisk'[Vehicle Involvements])",
        "Vehicle Severe Rate": "DIVIDE(SUM('VehicleRisk'[Severe Collisions]), SUM('VehicleRisk'[Collisions]))",
        "Avg Vehicle Severity": "AVERAGE('VehicleRisk'[Avg Severity Score])",
    },
    "Hotspot": {
        "Hotspot Collisions": "SUM('Hotspot'[Collisions])",
        "Hotspot Severe Collisions": "SUM('Hotspot'[Severe Collisions])",
    },
    "AnomalySignals": {
        "Review Collisions": "CALCULATE(COUNTROWS('AnomalySignals'), 'AnomalySignals'[Review Status] = \"Review\")",
        "Review Rate": "DIVIDE([Review Collisions], COUNTROWS('AnomalySignals'))",
        "Night Events": "CALCULATE(COUNTROWS('AnomalySignals'), 'AnomalySignals'[Is Night] = TRUE())",
        "Multi Vehicle Events": "CALCULATE(COUNTROWS('AnomalySignals'), 'AnomalySignals'[Vehicle Count] >= 3)",
    },
}

for table_name, (source_view, columns) in schemas.items():
    lines = [f"table {table_name}", f"\tlineageTag: {uuid.uuid4()}", ""]
    for name, dax in measures.get(table_name, {}).items():
        fmt = "0.0%" if "Rate" in name else "#,##0.00" if "Avg" in name else "#,##0"
        lines += [
            f"\tmeasure '{name}' = {dax}",
            f"\t\tformatString: {fmt}",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "",
        ]
    for display, source, dtype in columns:
        lines += [
            f"\tcolumn '{display}'",
            f"\t\tdataType: {dtype}",
            f"\t\tlineageTag: {uuid.uuid4()}",
            "\t\tsummarizeBy: none",
            f"\t\tsourceColumn: {source}",
            "",
            "\t\tannotation SummarizationSetBy = Automatic",
            "",
        ]
    lines += [
        f"\tpartition {table_name} = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        "\t\t\t\t    Source = PostgreSQL.Database(Server, Database),",
        f'\t\t\t\t    Data = Source{{[Schema="reporting",Item="{source_view}"]}}[Data]',
        "\t\t\t\tin",
        "\t\t\t\t    Data",
        "",
        "\tannotation PBI_ResultType = Table",
        "",
    ]
    (MODEL / "definition" / "tables" / f"{table_name}.tmdl").write_text(
        "\n".join(lines), encoding="utf-8"
    )

(MODEL / "definition" / "relationships.tmdl").write_text("", encoding="utf-8")

readme = """# Motor Claims Intelligence — Power BI

Open `MotorClaimsIntelligence.pbip` after running PostgreSQL and `dbt build`.

Required Power BI preview features:

- Power BI Project (.pbip)
- Store semantic model using TMDL format
- Store reports using enhanced metadata format (PBIR)

If PostgreSQL is not local, update the `Server` and `Database` parameters in
Power Query. The report imports four views from the `reporting` schema.

The anomaly page contains explainable review indicators. It does not determine
fraud, guilt, fault, or insurance price.
"""
(POWERBI / "README.md").write_text(readme, encoding="utf-8")

print(POWERBI / "MotorClaimsIntelligence.pbip")
