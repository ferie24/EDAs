import streamlit as st 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import data_for_vis
import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events

data = data_for_vis.cleanup("Iris.csv")

st.title("Iris Dataset Visualisation")

def pie_chart_matplotlib(data): 
    label = data.Species.unique()
    counts = data.Species.value_counts()
    fig, ax = plt.subplots()
    ax.pie(counts, labels=label, startangle=90)
    ax.axis("equal")
    
    st.pyplot(fig)

def pie_chart_plotly(data): 
    label = data.Species.unique()
    counts = data.Species.value_counts()
    tmp_data = {
        'label' : label, 
        'counts' : counts,
        'color' : ['#E0BBE4','#F27348', '#76CDCD' ]
    }
    avg_sepal_length = data.groupby('Species')['SepalLengthCm'].mean().round(2)
    avg_sepel_width = data.groupby('Species')['SepalWidthCm'].mean().round(2)
    avg_petal_length = data.groupby('Species')['PetalLengthCm'].mean().round(2)
    avg_petal_width = data.groupby('Species')['PetalWidthCm'].mean().round(2)
    further_information = {
        'label' : label, 
        'avg_sepal_length' : avg_sepal_length, 
        'avg_sepal_width' : avg_sepel_width,
        'avg_petal_length' : avg_petal_length, 
        'avg_petal_width' : avg_petal_width,
    }
    fig = px.pie(tmp_data, values='counts', names='label', 
                 title="Interactive Pie Chart of the Data", 
                 color_discrete_sequence=tmp_data['color'])

    selected_points = plotly_events(fig, click_event=True)

    # Check if a slice was clicked
    if selected_points:
        clicked_slice = selected_points[0]
        category = tmp_data['label'][clicked_slice['pointNumber']]
        st.write(f"More information about the Species: {category}")
        # Here you can add more information or redirect logic
        avg_sw = further_information['avg_sepal_width'][category]
        avg_sl = further_information['avg_sepal_length'][category]
        avg_pw = further_information['avg_petal_width'][category]
        avg_pl = further_information['avg_petal_length'][category]
        with st.container(border=True):
            st.write(f"The average sepal width is: {avg_sw} cm")
            st.write(f"The average sepal length is: {avg_sl} cm")
            st.write(f"The average petal width is: {avg_pw} cm")
            st.write(f"The average petal length is: {avg_pl} cm")

def table(data): 
    print(data['Species'].value_counts())
    versicolor = data[data['Species'] == "Iris-versicolor"]
    virginica = data[data['Species'] == "Iris-virginica"]
    setosa = data[data['Species'] == "Iris-setosa"]

    table = pd.DataFrame(
        {
            "Versicolor": [versicolor.count()], 
            "Virginica": [virginica.count()], 
            "Setosa": [setosa.count()],
        }
    )

    st.table(table)
def boxplots(data):
    fig_Versicolor, ax1 = data_for_vis.make_boxplots(versicolor, "Versicolor")
    fig_Virginica, ax2 = data_for_vis.make_boxplots(virginica, "Virginica")
    fig_Setosa, ax3 = data_for_vis.make_boxplots(setosa, "Setosa")
    st.pyplot(fig_Versicolor)
    st.pyplot(fig_Virginica)
    st.pyplot(fig_Setosa)

pie_chart_plotly(data)
