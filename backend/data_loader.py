import pandas as pd

def load_data():
    url = "https://raw.githubusercontent.com/Nikhil3405/TitanicIntelligence/main/Titanic-Dataset.csv"
    df = pd.read_csv(url)
    return df