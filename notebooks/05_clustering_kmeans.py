def run():

    import os
    import pandas as pd
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    # Loading data
    repo_root = os.path.dirname(os.path.abspath(__name__))
    data_dir = os.path.join(repo_root, 'data')
    file_name = os.path.join('03_Processed', '02_ProcessedData_Quantative.csv')
    file_path = os.path.join(data_dir, file_name)
    df = pd.read_csv(file_path)

    # Dropping undesired columns
    df_skills = df.drop(columns=['ID', 'Organizowanie życia community'])

    # Standardizing the data
    scaler = StandardScaler()
    df_skills_scaled = scaler.fit_transform(df_skills)

    # Applying PCA
    pca = PCA()
    pca.fit(df_skills_scaled)
    
    # Getting needed values for quality of data representation metric
    explained_variance_ratio = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance_ratio)

    # Creating table
    num_components = len(explained_variance_ratio)
    quality_representation = cumulative_variance * 100  # Convert to percentage
    table_data = {
        "Wartość własna lj": pca.explained_variance_,
        "% ogółu": explained_variance_ratio * 100,
        "Skumul.": cumulative_variance * 100,
        "Jakość reprezentacji fq": quality_representation
    }

    # Converting to DataFrame for better presentation
    table_quality = pd.DataFrame(table_data, columns=["Wartość własna lj", "% ogółu", "Skumul.", "Jakość reprezentacji fq"])
    table_quality.index += 1  # Start indexing from 1
    print(table_quality)

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
    plt.xlabel('Number of clusters / Liczba klastrów')
    plt.ylabel('SSE (Sum of Squared Errors) / Resztowa suma kwadratów')
    plt.title('Elbow Method / Wykres osypiska')
    
    # Saving the chart
    save_path = os.path.join(figures_dir, '05_elbow_method.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()

    # Based on the Elbow curve, choosing the optimal number of clusters
    optimal_k = 6
    kmeans = KMeans(n_clusters=optimal_k, random_state=24)
    df['Cluster'] = kmeans.fit_predict(df_skills_pca)
    
    # Adding +1 to clusters so they don't start at 0
    df['Cluster'] = df['Cluster'] + 1

    # Visualizing the clusters in the PCA-reduced space
    cluster_centers = pd.DataFrame(pca.inverse_transform(kmeans.cluster_centers_), columns=df_skills.columns)
    print(cluster_centers)

    # Plotting the clusters
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_skills_pca[:, 0], y=df_skills_pca[:, 1], hue=df['Cluster'], palette='tab10', s=100)
    for i, id in enumerate(df['ID']):
        plt.text(df_skills_pca[i, 0], df_skills_pca[i, 1], id, fontsize=9, ha='center', va='center')
    plt.title('Clusters of Skill Ratings in PCA-reduced Space / Zgrupowanie w dwóch wymiarach')
    plt.xlabel('PCA Component 1 / Główna składowa 1')
    plt.ylabel('PCA Component 2 / Główna składowa 2')
    
    # Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')

    save_path = os.path.join(figures_dir, '05_2d_plot.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()

    # Performing PCA to reduce dimensions - this time 3 dimensional
    pca = PCA(n_components=3)
    df_skills_pca = pca.fit_transform(df_skills_scaled)

    # Scatter plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(df_skills_pca[:, 0], df_skills_pca[:, 1], df_skills_pca[:, 2], 
                        c=df['Cluster'], cmap='tab10', s=100)

    # Adding IDs as labels
    for i, id in enumerate(df['ID']):
        ax.text(df_skills_pca[i, 0], df_skills_pca[i, 1], df_skills_pca[i, 2], id, fontsize=8, ha='center', va='center')

    # Adding labels
    ax.set_title('3D Scatter Plot of Clusters / Wykres 3-wymiarowy zgrupowania')
    ax.set_xlabel('PCA Component 1 / Główna składowa 1')
    ax.set_ylabel('PCA Component 2 / Główna składowa 2')
    ax.set_zlabel('PCA Component 3 / Główna składowa 3')

    # Adding legend
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters / Klastry")
    ax.add_artist(legend1)

    # Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')

    save_path = os.path.join(figures_dir, '05_3d_plot.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()



    # NO SOFT SKILLS
    # Loading data again
    repo_root = os.path.dirname(os.path.abspath(__name__))
    data_dir = os.path.join(repo_root, 'data')
    file_name = os.path.join('03_Processed', '02_ProcessedData_Quantative.csv')
    file_path = os.path.join(data_dir, file_name)
    df = pd.read_csv(file_path)

    # Dropping undesired columns - no soft skills
    df_skills_no_soft = df.drop(columns=['ID', 'Organizowanie życia community', 'Relacje z Biznesem', 'Relacje z naukowcami', 'Pozyskiwanie finansowania', 'Project Management', 'Projektowanie graficzne', 'Social Media', 'Ux/Ui', 'Współpraca z administracją UEW'])

    scaler = StandardScaler()
    df_skills_scaled = scaler.fit_transform(df_skills_no_soft)

    pca = PCA()
    pca.fit(df_skills_scaled)
    
    explained_variance_ratio = pca.explained_variance_ratio_

    cumulative_variance = np.cumsum(explained_variance_ratio)

    # Preparing the table
    num_components = len(explained_variance_ratio)
    quality_representation = cumulative_variance * 100  # Convert to percentage
    table_data = {
        "Wartość własna lj": pca.explained_variance_,
        "% ogółu": explained_variance_ratio * 100,
        "Skumul.": cumulative_variance * 100,
        "Jakość reprezentacji fq": quality_representation
    }

    # Converting to DataFrame for better presentation
    df_table = pd.DataFrame(table_data, columns=["Wartość własna lj", "% ogółu", "Skumul.", "Jakość reprezentacji fq"])
    df_table.index += 1  # Start indexing from 1
    print(df_table)

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
    plt.xlabel('Number of clusters / Liczba klastrów')
    plt.ylabel('SSE (Sum of Squared Errors) / Resztowa suma kwadratów')
    plt.title('Elbow Method (no soft skills) / Wykres osypiska (bez umiej. miękkich)')
    save_path = os.path.join(figures_dir, '05_elbow_method_no_soft_skills.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()

    # Based on the Elbow curve, choosing the optimal number of clusters
    optimal_k = 5
    kmeans = KMeans(n_clusters=optimal_k, random_state=24)
    df['Cluster'] = kmeans.fit_predict(df_skills_pca)

    # Adding +1 to clusters so they don't start at 0
    df['Cluster'] = df['Cluster'] + 1

    # Visualizing the clusters in PCA-reduced space
    cluster_centers = pd.DataFrame(pca.inverse_transform(kmeans.cluster_centers_), columns=df_skills.columns)
    print(cluster_centers)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df_skills_pca[:, 0], y=df_skills_pca[:, 1], hue=df['Cluster'], palette='tab10', s=100)
    for i, id in enumerate(df['ID']):
        plt.text(df_skills_pca[i, 0], df_skills_pca[i, 1], id, fontsize=9, ha='center', va='center')
    plt.title('Clusters of Skill Ratings in PCA-reduced Space (no soft skills) / Zgrupowanie w dwóch wymiarach (bez umiej. miękkich)')
    plt.xlabel('PCA Component 1 / Główna składowa 1')
    plt.ylabel('PCA Component 2 / Główna składowa 2')

    # Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')
    save_path = os.path.join(figures_dir, '05_2d_plot_no_soft_skills.png')
    plt.savefig(save_path, bbox_inches='tight')
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
    ax.set_title('3D Scatter Plot of Clusters (no soft skills) / Wykres 3-wymiarowy zgrupowania (bez umiej. miękkich)')
    ax.set_xlabel('PCA Component 1 / Główna składowa 1')
    ax.set_ylabel('PCA Component 2 / Główna składowa 2')
    ax.set_zlabel('PCA Component 3 / Główna składowa 3')

    # Adding legend
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)

    save_path = os.path.join(figures_dir, '05_3d_plot_no_soft_skills.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()