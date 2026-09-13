import os
import json
import hashlib
import shutil

def get_deterministic_id(seed):
    return hashlib.md5(seed.encode('utf-8')).hexdigest()[:20]

def col_expr(table, col):
    return {
        "field": {
            "Column": {
                "Expression": {"SourceRef": {"Entity": table}},
                "Property": col
            }
        },
        "queryRef": f"{table}.{col}",
        "nativeQueryRef": col
    }

def meas_expr(table, meas):
    return {
        "field": {
            "Measure": {
                "Expression": {"SourceRef": {"Entity": table}},
                "Property": meas
            }
        },
        "queryRef": f"{table}.{meas}",
        "nativeQueryRef": meas
    }

def make_textbox(name, title_text, x, y, w, h, z=0):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": [
                                {
                                    "textRuns": [
                                        {
                                            "value": title_text,
                                            "textStyle": {
                                                "fontFamily": "Segoe UI Semibold",
                                                "fontSize": "16pt",
                                                "color": "#0F172A"
                                            }
                                        }
                                    ],
                                    "horizontalTextAlignment": "left"
                                }
                            ]
                        }
                    }
                ]
            },
            "visualContainerObjects": {
                "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
                "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
                "padding": [{"properties": {
                    "top": {"expr": {"Literal": {"Value": "2D"}}},
                    "bottom": {"expr": {"Literal": {"Value": "2D"}}},
                    "left": {"expr": {"Literal": {"Value": "4D"}}},
                    "right": {"expr": {"Literal": {"Value": "4D"}}}
                }}]
            }
        }
    }

def make_slicer(name, table, col, display_name, x, y, w, h, z=1000):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "slicer",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [col_expr(table, col)]
                    }
                }
            },
            "objects": {
                "data": [{"properties": {"mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}}}],
                "header": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{display_name}'"}}}
                    }
                }]
            },
            "visualContainerObjects": {
                "padding": [{
                    "properties": {
                        "top": {"expr": {"Literal": {"Value": "4D"}}},
                        "bottom": {"expr": {"Literal": {"Value": "4D"}}},
                        "left": {"expr": {"Literal": {"Value": "4D"}}},
                        "right": {"expr": {"Literal": {"Value": "4D"}}}
                    }
                }]
            }
        }
    }

def make_card_visual(name, measures, x, y, w, h, z=1000):
    projections = [meas_expr(t, m) for t, m in measures]
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "cardVisual",
            "query": {
                "queryState": {
                    "Data": {
                        "projections": projections
                    }
                }
            }
        }
    }

def make_line_chart(name, title, cat_table, cat_col, y_measures, x, y, w, h, z=1000):
    y_projections = [meas_expr(t, m) for t, m in y_measures]
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "lineChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [col_expr(cat_table, cat_col)]},
                    "Y": {"projections": y_projections}
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            }
        }
    }

def make_donut_chart(name, title, cat_table, cat_col, meas_table, meas_name, x, y, w, h, z=1000):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "donutChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [col_expr(cat_table, cat_col)]},
                    "Y": {"projections": [meas_expr(meas_table, meas_name)]}
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            }
        }
    }

def make_bar_chart(name, title, cat_table, cat_col, meas_table, meas_name, x, y, w, h, z=1000):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "barChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [col_expr(cat_table, cat_col)]},
                    "Y": {"projections": [meas_expr(meas_table, meas_name)]}
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            }
        }
    }

def make_column_chart(name, title, cat_table, cat_col, meas_table, meas_name, x, y, w, h, z=1000):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "columnChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [col_expr(cat_table, cat_col)]},
                    "Y": {"projections": [meas_expr(meas_table, meas_name)]}
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            }
        }
    }

def make_clustered_column_chart(name, title, cat_table, cat_col, y_measures, x, y, w, h, z=1000):
    y_projections = [meas_expr(t, m) for t, m in y_measures]
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "clusteredColumnChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [col_expr(cat_table, cat_col)]},
                    "Y": {"projections": y_projections}
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            }
        }
    }

def make_pivot_table(name, title, row_fields, col_fields, val_measures, x, y, w, h, z=1000):
    row_projs = [col_expr(t, c) for t, c in row_fields]
    col_projs = [col_expr(t, c) for t, c in col_fields] if col_fields else []
    val_projs = [meas_expr(t, m) for t, m in val_measures]
    qs = {"Values": {"projections": val_projs}}
    if row_projs:
        qs["Rows"] = {"projections": row_projs}
    if col_projs:
        qs["Columns"] = {"projections": col_projs}
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "pivotTable",
            "query": {
                "queryState": qs
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            }
        }
    }

def make_table_ex(name, title, fields, x, y, w, h, z=1000):
    projections = []
    for f in fields:
        kind, tbl, prop = f
        if kind == 'col':
            projections.append(col_expr(tbl, prop))
        else:
            projections.append(meas_expr(tbl, prop))
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "tableEx",
            "query": {
                "queryState": {
                    "Values": {"projections": projections}
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            }
        }
    }

base_dir = r"Retail_Ecommerce_Analytics.Report"
def_dir = os.path.join(base_dir, "definition")
pages_dir = os.path.join(def_dir, "pages")
static_res_dir = os.path.join(def_dir, "StaticResources", "RegisteredResources")

os.makedirs(pages_dir, exist_ok=True)
os.makedirs(static_res_dir, exist_ok=True)

# 0. .platform
with open(os.path.join(base_dir, ".platform"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {
            "type": "Report",
            "displayName": "Retail_Ecommerce_Analytics"
        },
        "config": {
            "version": "2.0",
            "logicalId": "00000000-0000-0000-0000-000000000001"
        }
    }, f, indent=2)

# 1. definition.pbir
with open(os.path.join(base_dir, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {
            "byPath": {
                "path": "../Retail_Ecommerce_Analytics.SemanticModel"
            }
        }
    }, f, indent=2)

# 2. version.json
with open(os.path.join(def_dir, "version.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0"
    }, f, indent=2)

# 3. Theme
theme_filename = "RetailEditorialTheme-7c8e9f1a.json"
with open(os.path.join(static_res_dir, theme_filename), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.114.json",
        "name": theme_filename,
        "dataColors": [
            "#0F172A", "#0EA5E9", "#10B981", "#64748B", "#8B5CF6", "#F59E0B", "#EF4444", "#38BDF8"
        ],
        "good": "#10B981",
        "bad": "#EF4444",
        "neutral": "#F59E0B",
        "background": "#F8F9FA",
        "foreground": "#0F172A",
        "tableAccent": "#0EA5E9",
        "textClasses": {
            "callout": {"fontSize": 18, "fontFace": "Segoe UI Semibold", "color": "#0F172A"},
            "title": {"fontSize": 13, "fontFace": "Segoe UI Semibold", "color": "#0F172A"},
            "header": {"fontSize": 11, "fontFace": "Segoe UI Semibold", "color": "#334155"},
            "label": {"fontSize": 10, "fontFace": "Segoe UI", "color": "#64748B"}
        },
        "visualStyles": {
            "*": {
                "*": {
                    "background": [{"color": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}],
                    "border": [{"show": True, "color": {"solid": {"color": "#E2E8F0"}}, "radius": 6}],
                    "visualContainerObjects": {
                        "padding": [{"top": 8, "bottom": 8, "left": 8, "right": 8}]
                    }
                }
            }
        }
    }, f, indent=2)

# 4. report.json
with open(os.path.join(def_dir, "report.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
        "layoutOptimization": "None",
        "themeCollection": {
            "baseTheme": {
                "name": "CY24SU10",
                "reportVersionAtImport": "2.1.0",
                "type": "SharedResources"
            },
            "customTheme": {
                "name": theme_filename,
                "reportVersionAtImport": "2.1.0",
                "type": "RegisteredResources"
            }
        },
        "resourcePackages": [
            {
                "name": "RegisteredResources",
                "type": "RegisteredResources",
                "items": [
                    {
                        "name": theme_filename,
                        "path": theme_filename,
                        "type": "CustomTheme"
                    }
                ]
            }
        ]
    }, f, indent=2)

pages = [
    {
        "id": "ReportSection01",
        "displayName": "Executive Omnichannel Summary",
        "title": "BlueMart Retail & E-Commerce Executive Overview",
        "slicers": [
            ("Dim_Date", "Year", "Year", 24, 60, 180),
            ("Fact_Sales", "channel", "Channel", 216, 60, 220),
            ("Dim_Product", "category", "Category", 448, 60, 240),
            ("Dim_Customer", "loyalty_segment", "Loyalty Segment", 700, 60, 220)
        ],
        "kpi_measures": [
            ("_Measures", "Net Sales"),
            ("_Measures", "Gross Margin %"),
            ("_Measures", "Transactions Count"),
            ("_Measures", "Average Unit Retail (AUR)"),
            ("_Measures", "Online Penetration %")
        ],
        "charts": [
            ("line", "Monthly Net Sales vs Prior Year", "Dim_Date", "Year Month", [("_Measures", "Net Sales"), ("_Measures", "Sales Prior Year (PY)")], 24, 256, 740, 224),
            ("donut", "Net Sales by Channel", "Fact_Sales", "channel", "_Measures", "Net Sales", 780, 256, 476, 224),
            ("bar", "Net Sales by Category", "Dim_Product", "category", "_Measures", "Net Sales", 24, 488, 740, 220),
            ("pivot", "Omnichannel Performance Matrix", [("Fact_Sales", "channel")], None, [("_Measures", "Net Sales"), ("_Measures", "Gross Margin %"), ("_Measures", "Total Units Sold")], 780, 488, 476, 220)
        ]
    },
    {
        "id": "ReportSection02",
        "displayName": "E-Commerce & Customer Dynamics",
        "title": "Customer Demographics, Loyalty & Channel Adoption",
        "slicers": [
            ("Dim_Date", "Year", "Year", 24, 60, 180),
            ("Fact_Sales", "channel", "Channel", 216, 60, 220),
            ("Dim_Product", "category", "Category", 448, 60, 240),
            ("Dim_Customer", "loyalty_segment", "Loyalty Segment", 700, 60, 220)
        ],
        "kpi_measures": [
            ("_Measures", "Active Customers"),
            ("_Measures", "Customer Retention / Repeat Purchase Rate"),
            ("_Measures", "Average Order Value (AOV)"),
            ("_Measures", "Average Unit Retail (AUR)")
        ],
        "charts": [
            ("column", "Revenue by Loyalty Segment", "Dim_Customer", "loyalty_segment", "_Measures", "Net Sales", 24, 256, 600, 224),
            ("pivot", "Preferred Channel vs Transacting Channel", [("Dim_Customer", "preferred_channel")], [("Fact_Sales", "channel")], [("_Measures", "Net Sales")], 640, 256, 616, 224),
            ("bar", "Net Sales by Customer City", "Dim_Customer", "city", "_Measures", "Net Sales", 24, 488, 600, 220),
            ("clustered_column", "Sales & Profit Margin by Gender", "Dim_Customer", "gender", [("_Measures", "Net Sales"), ("_Measures", "Gross Margin $")], 640, 488, 616, 220)
        ]
    },
    {
        "id": "ReportSection03",
        "displayName": "Category & Merchandising Performance",
        "title": "Merchandising Economics: Profitability, Velocity & Discounts",
        "slicers": [
            ("Dim_Date", "Year", "Year", 24, 60, 180),
            ("Fact_Sales", "channel", "Channel", 216, 60, 220),
            ("Dim_Product", "category", "Category", 448, 60, 240),
            ("Dim_Customer", "loyalty_segment", "Loyalty Segment", 700, 60, 220)
        ],
        "kpi_measures": [
            ("_Measures", "Total Units Sold"),
            ("_Measures", "Gross Margin $"),
            ("_Measures", "Gross Margin %"),
            ("_Measures", "Average Unit Retail (AUR)")
        ],
        "charts": [
            ("pivot", "Category & Subcategory Margin Matrix", [("Dim_Product", "category"), ("Dim_Product", "subcategory")], None, [("_Measures", "Net Sales"), ("_Measures", "Total COGS"), ("_Measures", "Gross Margin $"), ("_Measures", "Gross Margin %")], 24, 256, 720, 224),
            ("bar", "Top Brands by Net Sales", "Dim_Product", "brand", "_Measures", "Net Sales", 760, 256, 496, 224),
            ("clustered_column", "Gross vs Net Sales by Category (Discount Erosion)", "Dim_Product", "category", [("_Measures", "Gross Sales"), ("_Measures", "Net Sales")], 24, 488, 720, 220),
            ("table", "Promotional Campaigns & Discount Rates", [("col", "Dim_Promotion", "promo_name"), ("col", "Dim_Promotion", "promo_type"), ("col", "Dim_Promotion", "discount_pct")], None, None, 760, 488, 496, 220)
        ]
    },
    {
        "id": "ReportSection04",
        "displayName": "Inventory Health & Replenishment Monitor",
        "title": "Supply Chain & Inventory Operational Replenishment Monitor",
        "slicers": [
            ("Dim_Product", "category", "Category", 24, 60, 260),
            ("Dim_Store", "store_name", "Store", 300, 60, 280),
            ("Dim_Store", "city", "City", 600, 60, 240)
        ],
        "kpi_measures": [
            ("_Measures", "Current Stock On Hand"),
            ("_Measures", "Inventory Valuation"),
            ("_Measures", "Out of Stock Risk SKUs"),
            ("_Measures", "Stock-to-Sales Ratio")
        ],
        "charts": [
            ("column", "Category Stock On Hand", "Dim_Product", "category", "_Measures", "Current Stock On Hand", 24, 256, 640, 224),
            ("bar", "Stock On Hand by Store City", "Dim_Store", "city", "_Measures", "Current Stock On Hand", 680, 256, 576, 224),
            ("table", "SKU-Level Replenishment Stock Status", [("col", "Dim_Product", "sku_name"), ("col", "Dim_Product", "category"), ("col", "Dim_Store", "store_name"), ("col", "Fact_Inventory", "stock_on_hand"), ("col", "Fact_Inventory", "reorder_point"), ("col", "Fact_Inventory", "safety_stock")], None, None, 24, 488, 1232, 220)
        ]
    }
]

# Wipe old files in pages directory cleanly
for root, dirs, files in os.walk(pages_dir, topdown=False):
    for f in files:
        try: os.remove(os.path.join(root, f))
        except: pass
    for d in dirs:
        try: os.rmdir(os.path.join(root, d))
        except: pass

page_order = []
for p in pages:
    page_id = p["id"]
    page_order.append(page_id)
    p_dir = os.path.join(pages_dir, page_id)
    v_dir = os.path.join(p_dir, "visuals")
    os.makedirs(v_dir, exist_ok=True)
    
    # page.json
    with open(os.path.join(p_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
            "name": page_id,
            "displayName": p["displayName"],
            "displayOption": "FitToPage",
            "height": 720,
            "width": 1280
        }, f, indent=2)
    
    # 1. Textbox Title (Y: 12, H: 44)
    tb_id = get_deterministic_id(f"{page_id}_title")
    tb_v = make_textbox(tb_id, p["title"], 24, 12, 1232, 44, z=0)
    os.makedirs(os.path.join(v_dir, tb_id), exist_ok=True)
    with open(os.path.join(v_dir, tb_id, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(tb_v, f, indent=2)
        
    # 2. Slicers (Y: 60, H: 76)
    z_idx = 1000
    for idx, (tbl, col, disp, sx, sy, sw) in enumerate(p["slicers"]):
        sl_id = get_deterministic_id(f"{page_id}_slicer_{idx}")
        sl_v = make_slicer(sl_id, tbl, col, disp, sx, sy, sw, 76, z=z_idx)
        z_idx += 1000
        os.makedirs(os.path.join(v_dir, sl_id), exist_ok=True)
        with open(os.path.join(v_dir, sl_id, "visual.json"), "w", encoding="utf-8") as f:
            json.dump(sl_v, f, indent=2)
            
    # 3. KPI Card Strip (Y: 144, H: 104)
    card_id = get_deterministic_id(f"{page_id}_kpi")
    card_v = make_card_visual(card_id, p["kpi_measures"], 24, 144, 1232, 104, z=z_idx)
    z_idx += 1000
    os.makedirs(os.path.join(v_dir, card_id), exist_ok=True)
    with open(os.path.join(v_dir, card_id, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(card_v, f, indent=2)
        
    # 4. Charts (Y: 256, H: 224 and Y: 488, H: 220)
    for idx, chart in enumerate(p["charts"]):
        c_type = chart[0]
        c_id = get_deterministic_id(f"{page_id}_chart_{idx}")
        if c_type == "line":
            _, title, ct, cc, y_m, cx, cy, cw, ch = chart
            v_obj = make_line_chart(c_id, title, ct, cc, y_m, cx, cy, cw, ch, z=z_idx)
        elif c_type == "donut":
            _, title, ct, cc, mt, mn, cx, cy, cw, ch = chart
            v_obj = make_donut_chart(c_id, title, ct, cc, mt, mn, cx, cy, cw, ch, z=z_idx)
        elif c_type == "bar":
            _, title, ct, cc, mt, mn, cx, cy, cw, ch = chart
            v_obj = make_bar_chart(c_id, title, ct, cc, mt, mn, cx, cy, cw, ch, z=z_idx)
        elif c_type == "column":
            _, title, ct, cc, mt, mn, cx, cy, cw, ch = chart
            v_obj = make_column_chart(c_id, title, ct, cc, mt, mn, cx, cy, cw, ch, z=z_idx)
        elif c_type == "clustered_column":
            _, title, ct, cc, y_m, cx, cy, cw, ch = chart
            v_obj = make_clustered_column_chart(c_id, title, ct, cc, y_m, cx, cy, cw, ch, z=z_idx)
        elif c_type == "pivot":
            _, title, r_f, c_f, v_m, cx, cy, cw, ch = chart
            v_obj = make_pivot_table(c_id, title, r_f, c_f, v_m, cx, cy, cw, ch, z=z_idx)
        elif c_type == "table":
            _, title, fields, _, _, cx, cy, cw, ch = chart
            v_obj = make_table_ex(c_id, title, fields, cx, cy, cw, ch, z=z_idx)
            
        z_idx += 1000
        os.makedirs(os.path.join(v_dir, c_id), exist_ok=True)
        with open(os.path.join(v_dir, c_id, "visual.json"), "w", encoding="utf-8") as f:
            json.dump(v_obj, f, indent=2)

# pages.json
with open(os.path.join(pages_dir, "pages.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
        "pageOrder": page_order,
        "activePageName": page_order[0]
    }, f, indent=2)

print("Report generation with deterministic IDs completed successfully!")
