import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --- Load & Combine Data ---
@st.cache_data
def load_data():
    df_lama = pd.read_csv("data_clean.csv")

    df_baru_raw = pd.read_excel("20180920_Marine_Pollution.xlsx", sheet_name="Sheet1")
    df_baru_long = pd.melt(df_baru_raw, id_vars=["Countries"], var_name="INDICATOR", value_name="OBS_VALUE")
    df_baru_long["TIME_PERIOD"] = 2018
    df_baru_long["UNIT_MEASURE"] = "COUNT"
    df_baru_long["DATA_SOURCE"] = "SPREP (2018)"

    country_to_code = {
        "American Samoa": "AS", "Cook Islands": "CK", "Fiji": "FJ", "French Polynesia": "PF",
        "International Waters": "IW", "Niue": "NU", "Papua New Guinea": "PG", "Samoa": "WS",
        "Solomon Islands": "SB", "Tokelau": "TK", "Tonga": "TO", "Tuvalu": "TV", "Vanuatu": "VU"
    }
    df_baru_long["GEO_PICT"] = df_baru_long["Countries"].map(country_to_code)
    df_baru_long["INDICATOR"] = "MARINE_POLLUTION_" + df_baru_long["INDICATOR"].str.upper().str.replace(" ", "_")
    df_baru = df_baru_long[["INDICATOR", "GEO_PICT", "TIME_PERIOD", "OBS_VALUE", "UNIT_MEASURE", "DATA_SOURCE"]]

    df_terbaru_raw = pd.read_csv("ENV_Marine_Pollution_Obs_data_v4.csv")
    df_terbaru_long = pd.melt(df_terbaru_raw, id_vars="Row Labels", var_name="INDICATOR", value_name="OBS_VALUE")
    df_terbaru_long = df_terbaru_long.rename(columns={"Row Labels": "Countries"})
    df_terbaru_long["TIME_PERIOD"] = 2015
    df_terbaru_long["UNIT_MEASURE"] = "COUNT"
    df_terbaru_long["DATA_SOURCE"] = "SPREP (2015)"
    df_terbaru_long["GEO_PICT"] = df_terbaru_long["Countries"].map(country_to_code)
    df_terbaru_long["INDICATOR"] = "MARINE_POLLUTION_" + df_terbaru_long["INDICATOR"].str.upper().str.replace(" ", "_")
    df_terbaru = df_terbaru_long[["INDICATOR", "GEO_PICT", "TIME_PERIOD", "OBS_VALUE", "UNIT_MEASURE", "DATA_SOURCE"]]

    df_all = pd.concat([df_lama, df_baru, df_terbaru], ignore_index=True)

    indicator_labels = {
        "MARINE_POLLUTION_ABANDONED": "Abandoned Waste",
        "MARINE_POLLUTION_CHEMICALS": "Chemical Pollution",
        "MARINE_POLLUTION_DUMPED": "Dumped Waste",
        "MARINE_POLLUTION_GENERAL_GARBAGE": "General Garbage",
        "MARINE_POLLUTION_LAND_BASED_SOURCE": "Land-based Sources",
        "MARINE_POLLUTION_LOST_DURING_FISHING": "Lost During Fishing",
        "MARINE_POLLUTION_METALS": "Metal Waste",
        "MARINE_POLLUTION_OIL_SPLILLAGES_AND_LEAKAGES": "Oil Spillages & Leakages",
        "MARINE_POLLUTION_OLD_FISHING_GEAR": "Old Fishing Gear",
        "MARINE_POLLUTION_PLASTICS": "Plastic Waste",
        "MARINE_POLLUTION_WASTE_OILS": "Waste Oils",
        "AG_PRD_FIESMS": "Food Insecurity (FIES-Metric)",
        "EN_MAR_BEALITSQ": "Mangrove Area (sq km)",
        "ER_GRF_PLNTSTOR": "Forest Biomass Stock",
        "ER_H2O_FWTL": "Freshwater Levels",
        "ER_MRN_MARINKBA": "Marine Protected Area Coverage",
        "ER_PTD_TOT": "Total Protected Land Area",
        "ER_RSK_LST": "Species at Risk",
        "SPC_12_4_2": "Hazardous Waste Management",
        "SPC_12_5_1": "Recycling Rate",
        "SPC_14_2_1": "Sustainable Marine Management",
        "SPC_14_6_1": "Illegal Fishing Regulations",
        "SPC_14_b_1": "Small-scale Fisheries Access",
        "SPC_15_8_1": "Invasive Alien Species Control",
        "SPC_2_4_1": "Sustainable Agriculture Practices",
    }
    df_all["INDICATOR_LABEL"] = df_all["INDICATOR"].replace(indicator_labels)

    return df_all

# --- Load ---
df = load_data()

# --- Negara ---
country_map = {
    'CK': 'Cook Islands', 'WS': 'Samoa', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea',
    'MH': 'Marshall Islands', 'FJ': 'Fiji', 'VU': 'Vanuatu', 'FM': 'Micronesia (Federated States of)',
    'KI': 'Kiribati', 'NR': 'Nauru', 'PW': 'Palau', 'NU': 'Niue', 'TV': 'Tuvalu', 'TO': 'Tonga',
    'AS': 'American Samoa', 'IW': 'International Waters', 'SB': 'Solomon Islands', 'TK': 'Tokelau'
}
df['Country'] = df['GEO_PICT'].map(country_map).fillna(df['GEO_PICT'])

# --- Indicator desc ---
indicator_descriptions = {
    "Abandoned Waste": "Refers to materials like broken vessels, containers, or discarded objects left in the ocean or coastal areas without proper disposal.",
    "Chemical Pollution": "Pollution caused by harmful chemicals such as industrial waste, pesticides, or heavy metals entering marine environments and disrupting ecosystems.",
    "Dumped Waste": "Intentional disposal of waste materials—like garbage, sludge, or construction debris—into oceans or seas, often from ships or coastal sources.",
    "General Garbage": "Everyday litter such as wrappers, bags, and bottles found in marine or coastal areas, commonly resulting from improper waste management.",
    "Land-based Sources": "Pollution that originates from land (e.g., agriculture runoff, sewage, plastics) and flows into the ocean via rivers, drainage, or wind.",
    "Lost During Fishing": "Fishing gear or equipment accidentally lost at sea, which can continue to harm marine life by entanglement or ingestion (ghost gear).",
    "Metal Waste": "Refers to metal debris like wires, cans, or ship parts that corrode in marine environments, potentially releasing toxic substances.",
    "Oil Spillages & Leakages": "Release of oil into marine waters from accidents, leaking ships, or drilling operations, which can suffocate marine species and damage ecosystems.",
    "Old Fishing Gear": "Obsolete or broken nets, lines, and traps left or dumped in oceans, posing serious threats to marine biodiversity.",
    "Plastic Waste": "Plastic debris, including bottles, packaging, and microplastics, that accumulates in oceans, harming marine animals and entering the food chain.",
    "Waste Oils": "Used or leaked oils from ships or coastal sources that contaminate water, harming aquatic life and disrupting habitats.",
    "Food Insecurity (FIES-Metric)": "Percentage of the population experiencing moderate or severe food insecurity, meaning insufficient access to safe, nutritious food.",
    "Forest Biomass Stock": "Number of crop genetic resources (e.g., seeds, plants) preserved in gene banks for conservation and future agricultural resilience.",
    "Freshwater Levels": "Represents the share of fish populations that are not overfished and remain within safe biological limits.",
    "Marine Protected Area Coverage": "Percentage of marine areas classified as Key Biodiversity Areas (KBAs) that are protected through legal or regulatory measures.",
    "Total Protected Land Area": "Average percentage of freshwater and terrestrial KBAs covered by protected areas—an indicator of conservation efforts on land.",
    "Species at Risk": "Measures changes in the extinction risk of species, based on the IUCN Red List; a lower score indicates higher biodiversity threat.",
    "Hazardous Waste Management": "Amount of hazardous waste produced per capita, reflecting a country’s waste production intensity and management effectiveness.",
    "Recycling Rate": "Total amount of municipal waste recycled annually, in tonnes—indicating how much waste is diverted from landfills or incineration.",
    "Sustainable Marine Management": "Extent to which countries manage their marine environments using ecosystem-based approaches, balancing ecological health and resource use.",
    "Illegal Fishing Regulations": "Progress in implementing laws and international instruments to combat illegal, unreported, and unregulated (IUU) fishing, rated on a scale from 1 to 5.",
    "Small-scale Fisheries Access": "Level of legal and policy recognition given to small-scale fisheries for accessing marine resources, also rated from 1 (low) to 5 (high).",
    "Invasive Alien Species Control": "Reflects the presence of national legislation or regulations to prevent and control the spread of non-native species that harm ecosystems.",
    "Sustainable Agriculture Practices": "Percentage of agricultural land using sustainable and productive farming methods that support environmental, social, and economic sustainability."
}

# --- Sidebar ---
st.sidebar.markdown("### Indicator Selection")
indicator_options = df["INDICATOR_LABEL"].dropna().unique()
selected_indicator = st.sidebar.selectbox("Select Indicator", sorted(indicator_options))

# --- Filter data & cleaning ---
filtered_df = df[df["INDICATOR_LABEL"] == selected_indicator].copy()
filtered_df = filtered_df.dropna(subset=["OBS_VALUE"])
filtered_df["OBS_VALUE"] = pd.to_numeric(filtered_df["OBS_VALUE"], errors="coerce")
filtered_df["TIME_PERIOD"] = pd.to_numeric(filtered_df["TIME_PERIOD"], errors="coerce")
filtered_df = filtered_df.dropna(subset=["TIME_PERIOD"])
filtered_df["TIME_PERIOD"] = filtered_df["TIME_PERIOD"].astype(int)

# --- Koordinat ---
country_coords = {
    'Cook Islands': (-21.2367, -159.7777), 'Samoa': (-13.7590, -172.1046),
    'French Polynesia': (-17.6797, -149.4068), 'Papua New Guinea': (-6.314993, 143.95555),
    'Marshall Islands': (7.1315, 171.1845), 'Fiji': (-17.7134, 178.0650),
    'Vanuatu': (-15.3767, 166.9592), 'Micronesia (Federated States of)': (7.4256, 150.5508),
    'Kiribati': (1.8709, -157.3630), 'Nauru': (-0.5228, 166.9315), 'Palau': (7.5150, 134.5825),
    'Niue': (-19.0544, -169.8672), 'Tuvalu': (-7.1095, 177.6493), 'Tonga': (-21.1789, -175.1982),
    'American Samoa': (-14.2710, -170.1322), 'Solomon Islands': (-9.6457, 160.1562), 'Tokelau': (-9.2002, -171.8484),
    'International Waters': (-10.0, 160.0)
}

# --- Judul ---
st.title("🌊 Pacific Marine Pollution Dashboard")
st.markdown(f"### Indicator: {selected_indicator}")

# --- Latest map ---
latest_df = filtered_df.sort_values("TIME_PERIOD").groupby("Country").tail(1)
latest_df["lat"] = latest_df["Country"].map(lambda x: country_coords.get(x, (None, None))[0])
latest_df["lon"] = latest_df["Country"].map(lambda x: country_coords.get(x, (None, None))[1])
latest_df = latest_df.dropna(subset=["lat", "lon", "OBS_VALUE"])

if not latest_df.empty:
    # After determining latest_df and computing average
    # st.markdown(f"### Indicator: {selected_indicator}")

    # Display description
    st.markdown(indicator_descriptions.get(
        selected_indicator, 
        "No description available for this indicator."
    ))

    st.metric("Average Value (Latest Year)", f"{latest_df['OBS_VALUE'].mean():.2f}")
    fig_map = px.scatter_mapbox(
        latest_df, lat="lat", lon="lon", size="OBS_VALUE", color="OBS_VALUE",
        color_continuous_scale=["#E74C3C", "#FADA7A", "#27AE60"], size_max=60, zoom=2,
        hover_name="Country", hover_data={"OBS_VALUE": ':.2f', "lat": False, "lon": False},
        labels={"OBS_VALUE": selected_indicator}, height=550
    )
    fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_traces(marker=dict(sizemode="area", opacity=0.8))
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("""
    *࿐࿔ Bubble size* corresponds to the specific value of this indicator per country.  
    *࿐࿔ Bubble color* gives a relative intensity comparison across nations.
    """)
    
else:
    st.warning("❌ No valid data for the selected indicator.")

# --- Time Trend ---
st.markdown("### 📈 Indicator Trend Over Time")

# Bersihkan data & deteksi valid
trend_plot = (
    filtered_df.groupby(["Country", "TIME_PERIOD"])["OBS_VALUE"]
    .mean().reset_index()
)

if trend_plot.empty:
    st.info("❌ Trend data is not available for this indicator.")
else:
    country_counts = trend_plot["Country"].value_counts()
    country_has_single = country_counts[country_counts == 1].index.tolist()
    country_has_multi = country_counts[country_counts > 1].index.tolist()

    # Split line vs point
    df_line = trend_plot[trend_plot["Country"].isin(country_has_multi)]
    df_point = trend_plot[trend_plot["Country"].isin(country_has_single)]

    fig = px.line(
        df_line, x="TIME_PERIOD", y="OBS_VALUE", color="Country",
        labels={"TIME_PERIOD": "Year", "OBS_VALUE": selected_indicator},
        title=f"Trend of {selected_indicator} Over Time"
    )

    # Tambahkan titik untuk negara dengan hanya 1 tahun data
    if not df_point.empty:
        fig.add_scatter(
            x=df_point["TIME_PERIOD"], y=df_point["OBS_VALUE"],
            mode="markers", name="Single Year", marker=dict(color="gray", size=10),
            text=df_point["Country"], hoverinfo="text+y"
        )

    fig.update_layout(legend_title_text="Country", height=500)
    st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "This chart illustrates the temporal trend of the selected sustainability indicator across countries. "
    "Each line or dot represents how the indicator has evolved over time for countries with multi-year data. "
    "For countries with only a single year of data, the corresponding point is marked in gray. "
)

# --- Dominant Type by Country ---
st.markdown("### 🌐 Dominant Type of Marine Pollution by Country")
marine_df = df[df["INDICATOR"].str.startswith("MARINE_POLLUTION")].copy()
marine_df["OBS_VALUE"] = pd.to_numeric(marine_df["OBS_VALUE"], errors="coerce")
latest_pollution = marine_df.dropna(subset=["OBS_VALUE"]).sort_values("TIME_PERIOD").groupby(["Country", "INDICATOR_LABEL"]).tail(1)
dominant_pollution = latest_pollution.groupby("Country").apply(lambda x: x.loc[x["OBS_VALUE"].idxmax()]).reset_index(drop=True)
fig = px.bar(
    dominant_pollution.sort_values("OBS_VALUE", ascending=False),
    x="Country", y="OBS_VALUE", color="INDICATOR_LABEL",
    labels={"OBS_VALUE": "Pollution Level", "INDICATOR_LABEL": "Pollution Type"},
    title="Most Dominant Type of Marine Pollution per Country"
)
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "This visualization highlights the most prevalent type of marine pollution for each country based on the latest available data. "
    "The chart presents the dominant pollution category with the highest observed value, offering insights into region-specific environmental challenges."
)

# --- Plastic vs Protection ---
st.markdown("### 🛡 Marine Pollution vs. Environmental Protection Efforts")

# Filter indicators
plastik = df[df["INDICATOR_LABEL"] == "Plastic Waste"]
lindung = df[df["INDICATOR_LABEL"] == "Marine Protected Area Coverage"]

# Merge and clean
merged_env = pd.merge(
    plastik[["Country", "TIME_PERIOD", "OBS_VALUE"]],
    lindung[["Country", "TIME_PERIOD", "OBS_VALUE"]],
    on=["Country", "TIME_PERIOD"], suffixes=("_PLASTIC", "_MPA")
).dropna()

# Add category for color
def classify_risk(row):
    if row["OBS_VALUE_MPA"] >= 30 and row["OBS_VALUE_PLASTIC"] <= 50:
        return "Low Risk (Protected & Clean)"
    elif row["OBS_VALUE_MPA"] < 10 and row["OBS_VALUE_PLASTIC"] > 100:
        return "High Risk (Polluted & Unprotected)"
    else:
        return "Moderate Risk"

merged_env["Risk_Level"] = merged_env.apply(classify_risk, axis=1)

# Plot
fig = px.scatter(
    merged_env,
    x="OBS_VALUE_MPA", y="OBS_VALUE_PLASTIC",
    color="Risk_Level",  # <-- Color by category
    hover_name="Country",
    labels={
        "OBS_VALUE_PLASTIC": "Plastic Pollution",
        "OBS_VALUE_MPA": "Protected Area Coverage"
    },
    title="Plastic Pollution vs. Marine Protected Area Coverage",
    color_discrete_map={
        "Low Risk (Protected & Clean)": "green",
        "High Risk (Polluted & Unprotected)": "red",
        "Moderate Risk": "orange"
    }
)
fig.update_traces(marker=dict(size=12, opacity=0.8))
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This chart compares the relationship between *plastic pollution* and the extent of *marine protected areas (MPAs)* across various Pacific countries.

Each point on the scatter plot represents a country:

- *X-axis*: The proportion of the country's marine area that is officially protected (Marine Protected Area Coverage).
- *Y-axis: The level of **plastic waste pollution* reported (Plastic Pollution).

Hover over each data point to view the country name and detailed descriptions of the environmental indicators.       
                
This visualization is useful for spotting imbalances between environmental threats and conservation efforts, helping policymakers, researchers, and the public *prioritize action* in regions where marine ecosystems are most under pressure.
""")

# --- Risiko Lingkungan Tinggi ---
st.markdown("### ⚠ High-Risk Ocean Areas (High Pollution, Low Protection)")
merged_env["Risk_Score"] = merged_env["OBS_VALUE_PLASTIC"] / (merged_env["OBS_VALUE_MPA"] + 1)
merged_env["lat"] = merged_env["Country"].map(lambda x: country_coords.get(x, (None, None))[0])
merged_env["lon"] = merged_env["Country"].map(lambda x: country_coords.get(x, (None, None))[1])
merged_env = merged_env.dropna(subset=["lat", "lon"])
fig = px.scatter_mapbox(
    merged_env, lat="lat", lon="lon", size="Risk_Score", color="Risk_Score",
    color_continuous_scale="inferno", size_max=50,
    hover_name="Country", labels={"Risk_Score": "Environmental Risk Score"},
    zoom=2, height=550
)
fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
This visualization identifies *critical ocean zones* where environmental risk is notably high, based on two core factors:

- *Plastic Pollution Intensity* (OBS_VALUE_PLASTIC)
- *Marine Protected Area (MPA) Coverage* (OBS_VALUE_MPA)

A *Risk Score* is computed by dividing the level of plastic pollution by the level of marine protection in each country (Risk_Score = Plastic Pollution / (MPA Coverage + 1)). A higher score indicates areas where plastic waste is severe, yet marine protection remains minimal—posing a serious threat to marine biodiversity and ecosystem health.

Each bubble on the map represents a country:

- *Bubble Size and Color: Correspond to the calculated Risk Score. Larger and darker bubbles highlight **regions at greatest ecological risk*.
- *Hover Details*: Hovering over each bubble displays the country name and its risk level.

By mapping these risk hotspots, we spotlight regions that require *urgent conservation efforts, policy attention, and sustainable waste management strategies to protect marine environments. This information is especially valuable for guiding international cooperation and resource allocation toward **vulnerable marine ecosystems*.
""")