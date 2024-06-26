import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram

# Loading data
repo_root = os.path.dirname(os.path.abspath(__name__))
data_dir = os.path.join(repo_root, 'data')
file_name = os.path.join('03_Processed', '02_ProcessedData_Quantative.csv')
file_path = os.path.join(data_dir, file_name)
df = pd.read_csv(file_path)

# Dropping undesired columns
df_skills = df.drop(columns=['ID', 'Organizowanie życia community'])

# Replace 0 with 1 and 1 with 0 to be more logical
df_skills_rep = df_skills.replace({0: 1, 1: 0})

scaler = StandardScaler()
df_skills_scaled = scaler.fit_transform(df_skills_rep)

# Performing PCA to reduce dimensions
pca = PCA(n_components=2)
df_skills_pca = pca.fit_transform(df_skills_scaled)

# Determining the optimal number of clusters using the Elbow method on the reduced data
sse = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=24)
    kmeans.fit(df_skills_pca)
    sse.append(kmeans.inertia_)

# Plotting the Elbow curve
plt.figure(figsize=(8, 5))
plt.plot(k_range, sse, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('SSE (Sum of Squared Errors)')
plt.title('Elbow Method For Optimal k')
plt.show()

# Based on the Elbow curve, choosing the optimal number of clusters
optimal_k = 6
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_skills_pca)

# Visualizing the clusters in the PCA-reduced space
cluster_centers = pd.DataFrame(pca.inverse_transform(kmeans.cluster_centers_), columns=df_skills.columns)
print(cluster_centers)

plt.figure(figsize=(10, 6))
sns.scatterplot(x=df_skills_pca[:, 0], y=df_skills_pca[:, 1], hue=df['Cluster'], palette='tab10', s=100)
for i, id in enumerate(df['ID']):
    plt.text(df_skills_pca[i, 0], df_skills_pca[i, 1], id, fontsize=9, ha='center', va='center')
plt.title('Clusters of Skill Ratings in PCA-reduced Space')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()

# Performing PCA to reduce dimensions
pca = PCA(n_components=3)
df_skills_pca = pca.fit_transform(df_skills_scaled)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
scatter = ax.scatter(df_skills_pca[:, 0], df_skills_pca[:, 1], df_skills_pca[:, 2], 
                     c=df['Cluster'], cmap='tab10', s=100)

# Adding IDs as labels
for i, id in enumerate(df['ID']):
    ax.text(df_skills_pca[i, 0], df_skills_pca[i, 1], df_skills_pca[i, 2], id, fontsize=8, ha='center', va='center')

# Adding labels
ax.set_title('3D Scatter Plot of Clusters')
ax.set_xlabel('PCA Component 1')
ax.set_ylabel('PCA Component 2')
ax.set_zlabel('PCA Component 3')

# Adding legend
legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
ax.add_artist(legend1)

plt.show()