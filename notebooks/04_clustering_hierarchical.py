
def run():
    
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

    print(df)

    # Dropping undesired columns
    df_skills = df.drop(columns=['ID', 'Organizowanie życia community'])

    # Replace 0 with 1 and 1 with 0 to be more logical
    df_skills_rep = df_skills.replace({0: 1, 1: 0})

    # Standardize the data
    scaler = StandardScaler()
    df_skills_scaled = scaler.fit_transform(df_skills_rep)

    # Calculating distance matrix (using Euclidean distance)
    distance_matrix = linkage(df_skills_scaled, method='complete')

    # Plotting dendrogram
    plt.figure(figsize=(12, 8))
    dendrogram(distance_matrix, labels=df['ID'].values, orientation='top', leaf_rotation=90)
    threshold_distance = 14
    plt.axhline(y=threshold_distance, color='r', linestyle='--', label=f'Threshold Distance: {threshold_distance}')
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Individuals')
    plt.ylabel('Distance')
    plt.legend()
    plt.show()