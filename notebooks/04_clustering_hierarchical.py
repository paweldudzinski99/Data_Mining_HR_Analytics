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

    # Dropping undesired columns
    df_skills = df.drop(columns=['ID', 'Organizowanie życia community'])

    # Calculating distance matrix (using Euclidean distance)
    distance_matrix = linkage(df_skills, method='ward')

    # Plotting dendrogram
    plt.figure(figsize=(12, 8))
    dendrogram(distance_matrix, labels=df['ID'].values, orientation='top', leaf_rotation=90)
    threshold_distance = 13.5
    plt.axhline(y=threshold_distance, color='r', linestyle='--', label=f'Threshold Distance / Odległość wiązań: {threshold_distance}')
    plt.title('Hierarchical Clustering Dendrogram - Ward method / Dendrogram grupowania hierarchicznego - metoda Warda')
    plt.xlabel('ID')
    plt.ylabel('Distance / Odległość')
    plt.legend()

    #Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')

    save_path = os.path.join(figures_dir, '04_dendrogram_ward_method.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()


    # Calculating distance matrix (using Euclidean distance)
    distance_matrix2 = linkage(df_skills, method='complete')

    # Plotting dendrogram
    plt.figure(figsize=(12, 8))
    dendrogram(distance_matrix2, labels=df['ID'].values, orientation='top', leaf_rotation=90)
    threshold_distance = 11.7
    plt.axhline(y=threshold_distance, color='r', linestyle='--', label=f'Threshold Distance / Odległość wiązań: {threshold_distance}')
    plt.title('Hierarchical Clustering Dendrogram - complete method / Dendrogram grupowania hierarchicznego - metoda pełnego wiązania')
    plt.xlabel('ID')
    plt.ylabel('Distance / Odległość')
    plt.legend()

    #Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')

    save_path = os.path.join(figures_dir, '04_dendrogram_complete_method.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()


    df_no_soft_skills = df.drop(columns=['ID', 'Organizowanie życia community', 'Relacje z Biznesem', 'Relacje z naukowcami', 'Pozyskiwanie finansowania', 'Project Management', 'Projektowanie graficzne', 'Social Media', 'Ux/Ui', 'Współpraca z administracją UEW'])

    # Calculating distance matrix (using Euclidean distance)
    distance_matrix3 = linkage(df_no_soft_skills, method='ward')

    # Plotting dendrogram
    plt.figure(figsize=(12, 8))
    dendrogram(distance_matrix3, labels=df['ID'].values, orientation='top', leaf_rotation=90)
    threshold_distance = 12
    plt.axhline(y=threshold_distance, color='r', linestyle='--', label=f'Threshold Distance / Odległość wiązań: {threshold_distance}')
    plt.title('Hierarchical Clustering Dendrogram - Ward method / Dendrogram grupowania hierarchicznego - metoda Warda')
    plt.xlabel('ID')
    plt.ylabel('Distance / Odległość')
    plt.legend()

    #Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')

    save_path = os.path.join(figures_dir, '04_dendrogram_ward_method_no_soft_skills.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()


    # Calculating distance matrix (using Euclidean distance)
    distance_matrix4 = linkage(df_no_soft_skills, method='complete')

    # Plotting dendrogram
    plt.figure(figsize=(12, 8))
    dendrogram(distance_matrix4, labels=df['ID'].values, orientation='top', leaf_rotation=90)
    threshold_distance = 9
    plt.axhline(y=threshold_distance, color='r', linestyle='--', label=f'Threshold Distance / Odległość wiązań: {threshold_distance}')
    plt.title('Hierarchical Clustering Dendrogram - complete method / Dendrogram grupowania hierarchicznego - metoda pełnego wiązania')
    plt.xlabel('ID')
    plt.ylabel('Distance / Odległość')
    plt.legend()

    #Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')

    save_path = os.path.join(figures_dir, '04_dendrogram_complete_method_no_soft_skills.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()