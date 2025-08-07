import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Load CSV
df = pd.read_csv('sat1.csv')

# Title
st.title("Cancer Analysis Dashboard")

# Category Selection
categories = df['Cancer_Type'].dropna().unique()
Select = st.multiselect("Select Cancer Type(s):", options=categories)

# Filter DataFrame based on selection
if 'Lung' in Select or 'Breast' in Select:
    Mdf = df[df['Cancer_Type'].isin(Select)]
    missing_rows = Mdf[Mdf[['Cancer_Type', 'Stage', 'Genetic_Mutation']].isnull().any(axis=1)]
    print(f"Missing rows: {len(missing_rows)}")


    # Bar Chart
    bd = Mdf.groupby(['Cancer_Type', 'Gender']).size().reset_index(name='Count')
    bg = px.bar(bd, x='Cancer_Type', y='Count', color='Gender',
                title='Gender Distribution by Cancer Type',
                labels={'Count': 'Patient Count', 'Cancer_Type': 'Cancer Type'})
    st.plotly_chart(bg, use_container_width=True)

    # Pie Chart
    pied = Mdf.groupby(['Stage', 'Survival_Status']).size().reset_index(name='Count')
    pied['Label'] = pied['Stage'] + ' - ' + pied['Survival_Status']
    pg = px.pie(pied, names='Label', values='Count', title='Survival Status by Stage')
    st.plotly_chart(pg, use_container_width=True)

    # Sunburst Chart
    sunburst_df = Mdf
    sg = px.sunburst(sunburst_df,
                     path=['Cancer_Type', 'Stage', 'Genetic_Mutation'],
                     values=[1] * len(sunburst_df),
                     title='Genetic Mutation Breakdown by Cancer Type and Stage')
    st.plotly_chart(sg, use_container_width=True)

elif 'Skin' in Select or 'Blood' in Select:
    img_df = df[df['Cancer_Type'].isin(Select) & df['Image_Path'].notna()]
    st.subheader("Image Samples")
    for _, row in img_df.iterrows():
        try:
            image = Image.open(row['Image_Path'])
            st.image(image, caption=f"{row['Cancer_Type']} - {row['Diagnosis']}", use_column_width=True)
        except Exception as e:
            st.error(f"Could not load image: {row['Image_Path']}")

else:
    st.warning("Please select one or more Cancer Types to view analysis and images.")