import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_plot(df, query, plot_type=None, column=None):

    plt.figure()

    if plot_type == "histogram":
        sns.histplot(df[column], kde=True)

    elif plot_type == "bar":
        df[column].value_counts().plot(kind="bar")

    elif plot_type == "pie":
        df[column].value_counts().plot(kind="pie", autopct="%1.1f%%")

    elif plot_type == "box":
        sns.boxplot(y=df[column])

    else:
        return None

    plt.title(query)
    plt.tight_layout()
    plt.savefig("output.png")
    plt.close()

    return "output.png"