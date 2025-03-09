# Imports 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random



def cleanup(path="Iris.csv"): 

    data = pd.read_csv(path)

    # Cleaning up the Dataset 
    print("Size before cleaning: ", len(data))

    # Removing duplicate rows
    data = data.drop_duplicates()

    # Removing NaN values
    data = data.dropna()

    # Removing outliers using Z-score
    z_scores = np.abs(stats.zscore(data.select_dtypes(include=[np.number])))
    data = data[(z_scores < 3).all(axis=1)]

    print("Size after cleaning: ", len(data))
    return data 

def make_boxplots(dataset, name):
    # Boxplots for Versicolor Sepal and Petal dimensions
    fig, axs = plt.subplots(2, 2, figsize=(8, 4))

    # Sepal Length
    axs[0, 0].boxplot(dataset['SepalLengthCm'])
    axs[0, 0].set_title(f'{name} Sepal Length')

    # Sepal Width
    axs[0, 1].boxplot(dataset['SepalWidthCm'])
    axs[0, 1].set_title(f'{name} Sepal Width')

    # Petal Length
    axs[1, 0].boxplot(dataset['PetalLengthCm'])
    axs[1, 0].set_title(f'{name} Petal Length')

    # Petal Width
    axs[1, 1].boxplot(dataset['PetalWidthCm'])
    axs[1, 1].set_title(f'{name} Petal Width')

    return fig, axs