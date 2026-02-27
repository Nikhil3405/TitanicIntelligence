import pandas as pd

def load_data():
    df = pd.read_csv("C:/Projects/titanic/Titanic-Dataset.csv")
    return df