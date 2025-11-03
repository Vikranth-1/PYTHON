import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Load dataset (replace with your Kaggle dataset path)
data = pd.read_csv("data.csv")

# (i) Correlation and Scatter Plot
print(data.corr())
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

sns.scatterplot(x=data.columns[0], y=data.columns[1], data=data)
plt.title("Scatter Plot")
plt.show()

# (ii) Histogram
data.hist(figsize=(8,6))
plt.suptitle("Histograms")
plt.show()

# (iii) 3D Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data.iloc[:,0], data.iloc[:,1], data.iloc[:,2])
ax.set_xlabel(data.columns[0])
ax.set_ylabel(data.columns[1])
ax.set_zlabel(data.columns[2])
plt.title("3D Scatter Plot")
plt.show()
