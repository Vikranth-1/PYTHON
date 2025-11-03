import pandas as pd
import numpy as np

# Load dataset (example: any real-time Kaggle dataset)
data = pd.read_csv("house_prices.csv")

# Select numeric columns
numeric_cols = data.select_dtypes(include=[np.number]).columns

# Perform Univariate Analysis
for col in numeric_cols:
    print(f"--- {col} ---")
    print("Frequency:\n", data[col].value_counts().head())
    print("Mean:", data[col].mean())
    print("Median:", data[col].median())
    print("Mode:", data[col].mode()[0])
    print("Variance:", data[col].var())
    print("Standard Deviation:", data[col].std())
    print("Skewness:", data[col].skew())
    print("Kurtosis:", data[col].kurt())
    print("-" * 40)
