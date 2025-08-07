import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image


# Load CSV
df = pd.read_csv('sat1.csv')

# Title
st.title("Cancer Analysis Dashboard")

# Category Selection
categories = df['Cancer_Type'].unique()
Select = st.multiselect(
    "Select Cancer Type(s):",
    options=categories
)

# Filter DataFrame based on selection
if 'Lung' in Select or 'Breast' in Select:
    
        Mdf = df[df['Cancer_Type'].isin(Select)]

        #  Bar Chart: Gender Distribution by Cancer Type
        bd = Mdf.groupby(['Cancer_Type', 'Gender']).size().reset_index(name='Count')
        bg = px.bar(
          bd,
          x='Cancer_Type',
          y='Count',
          color='Gender',
          title='Gender Distribution by Cancer Type',
          labels={'Count': 'Patient Count', 'Cancer_Type': 'Cancer Type'}
        )
        

        #  Pie Chart: Survival Status Across Stages
        pied = Mdf.groupby(['Stage', 'Survival_Status']).size().reset_index(name='Count')

        # Combine 'Stage' and 'Survival_Status' for clarity
        pied['Label'] = pied['Stage'] + ' - ' + pied['Survival_Status']

        pg = px.pie(
        pied,
        names='Label',
        values='Count',
        title='Survival Status by Stage'
        )

        

       # Sunburst Chart: Genetic Mutation Breakdown
       
        sunburst_df = Mdf.dropna(subset=['Cancer_Type', 'Stage', 'Genetic_Mutation'])

        sg = px.sunburst(
            sunburst_df,
            path=['Cancer_Type', 'Stage', 'Genetic_Mutation'],
            values=[1] * len(sunburst_df),
            title='\t\tGenetic Mutation Breakdown by Cancer Type and Stage'
        )
        col1,col2,=st.columns(2)
        with col1:
             st.plotly_chart(bg, use_container_width=True)
        with col2:
             st.plotly_chart(pg, use_container_width=True)
        
        st.plotly_chart(sg, use_container_width=True)
if 'Skin' in Select or 'Blood' in Select:
    img_df = df[df['Cancer_Type'].isin(Select) & df['Image_Path'].notna()]
    i_col=st.columns(2)
    for i, row in img_df.iterrows():
        image = Image.open(row['Image_Path'])
        with i_col[i%2]:
             st.image(image, caption=f"{row['Cancer_Type']} - {row['Diagnosis']}", use_container_width=True)
if not Select:
    st.warning("Please select one or more Cancer Types to view analysis and images.")

