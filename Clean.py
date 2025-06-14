import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data kamu
df = pd.read_csv("data_clean.csv")

# === MAPPING ===
geo_mapping = {
    'CK': 'Cook Islands', 'WS': 'Samoa', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea',
    'MH': 'Marshall Islands', 'FJ': 'Fiji', 'VU': 'Vanuatu', 'KI': 'Kiribati',
    'FM': 'Micronesia (Federated States of)', 'PW': 'Palau', 'NR': 'Nauru',
    'TV': 'Tuvalu', 'NU': 'Niue', 'SB': 'Solomon Islands', 'NC': 'New Caledonia', 'TO': 'Tonga'
}

indicator_mapping = {
    'AG_PRD_FIESMS': 'Prevalence of food insecurity (moderate or severe)',
    'EN_MAR_BEALITSQ': 'Beach litter per square kilometer (Number)',
    'ER_GRF_PLNTSTOR': 'Plant genetic resources stored ex situ (Number)',
    'ER_H2O_FWTL': 'Proportion of fish stocks within sustainable levels',
    'ER_MRN_MARINKBA': 'Marine protected area coverage (KBA)',
    'ER_PTD_TOT': 'Freshwater and Terrestrial KBA area covered',
    'ER_RSK_LST': 'Red List Index',
    'SPC_12_4_2': 'Hazardous waste generated per capita (Kg)',
    'SPC_12_5_1': 'Municipal waste recycled (Tonnes)',
    'SPC_14_2_1': 'EEZ managed using ecosystem-based approaches',
    'SPC_14_6_1': 'Implementation to combat IUU fishing (1-5)',
    'SPC_14_b_1': 'Legal access rights for small-scale fisheries (1-5)',
    'SPC_15_8_1': 'Legislation to control invasive alien species',
    'SPC_2_4_1': 'Agricultural area under sustainable agriculture'
}

# Tambahkan kolom nama lokasi
df["Country"] = df["GEO_PICT"].map(geo_mapping)

# === STREAMLIT ===
st.title("🌊 Blue Pacific 2050 - Thematic Area 6: Ocean and Environment")

# Pilih indikator
indikator = st.selectbox(
    "Choose Indicator:",
    options=sorted(df["INDICATOR"].unique())
)

# Penjelasan indikator di bawahnya
st.markdown(f"**Indikator explained:** {indicator_mapping.get(indikator, 'no description')}")

location_option=['Show All'] + sorted(df["Country"].dropna().unique().tolist())
location_choosen=st.selectbox("Choose Location to show (optional):", options=location_option)

#markdown location
with st.expander("Location is"):
    for code, name in geo_mapping.items():
        st.markdown(f"**{code}** = {name}")

# Filter data
df_filtered = df[df["INDICATOR"] == indikator]

if location_choosen != "Show All":
    df_filtered= df_filtered[df_filtered["Country"]==location_choosen]

# use graph_object
fig = go.Figure()

for country in df_filtered["Country"].unique():
    country_data = df_filtered[df_filtered["Country"] == country]
    country_data = country_data.sort_values(by="TIME_PERIOD")

    fig.add_trace(go.Scatter(
        x=country_data["TIME_PERIOD"],
        y=country_data["OBS_VALUE"],
        mode='lines+text',
        name=country,
        text=[country] + [""] * (len(country_data) - 1),  
        textposition='top right',
        textfont=dict(size=10),
        showlegend=False  # Jangan pakai legend warna
    ))

# Tambah label dan judul
fig.update_layout(
    title=f"Observation throughout the years: {indicator_mapping.get(indikator, indikator)}",
    xaxis_title="Year",
    yaxis_title="Value",
    height=600,
    template="plotly_white"
)

# Tampilkan grafik
st.plotly_chart(fig, use_container_width=True)
