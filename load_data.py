import pandas as pd

def load_dashboard():

    df = pd.read_csv("dashboard_data.csv")

    return df


def load_database():

    df = pd.read_csv("hanoi_database.csv")

    return df