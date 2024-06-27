def run():

    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    #Defining root path
    repo_root = os.path.dirname(os.path.abspath(__name__))

    #Loading and reading the raw data
    data_dir = os.path.join(repo_root, 'data')
    file_name = os.path.join('03_Processed', '02_ProcessedData_Quantative.csv')
    file_path = os.path.join(data_dir, file_name)
    df = pd.read_csv(file_path)
    df.info()

    #Selecting all columns but ID and Organising community life 
    columns = df.columns[1:-1]

    #Creating a stacked bar chart for the distribution of ratings for each skill
    ratings_distribution = df[columns].apply(pd.Series.value_counts).transpose()

    #Sorting the DataFrame by the highest number of 4s, then 3s, then 2s, then 1s, then 0s
    sort_order = [4, 3, 2, 1, 0]
    ratings_distribution = ratings_distribution.sort_values(by=sort_order, ascending=False)
    #Reversing the order of the rows for ease of reading the chart
    ratings_distribution = ratings_distribution.iloc[::-1]


    #Defining figures directory
    figures_dir = os.path.join(repo_root, 'figures')

    #Plotting the stacked bar chart
    blue_palette = sns.color_palette("pastel", 5)
    ax = ratings_distribution.plot(kind='barh', stacked=True, title='Distribution of Ratings for Each Skill / Rozkład ocen dla umiejętności', 
                                color=blue_palette, figsize=(12, 8))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.xlabel('Count / Liczba ')
    plt.ylabel('Skills / Umiejętności')
    plt.legend(title='Rating / Ocena', loc='upper left', bbox_to_anchor=(1, 1))

    legend_labels = ['Mentor', 'Competent / Kompetenty', 'Interested / Zainteresowany', 'Unaware / Nieświadomy', 'Uninterested / Niezainteresowany']
    legend_patches = [plt.Rectangle((0,0),1,1,fc=color) for color in blue_palette[::-1]]
    plt.legend(legend_patches, legend_labels, title='Rating', loc='upper left', bbox_to_anchor=(1, 1))

    #Saving the chart
    save_path = os.path.join(figures_dir, '03_survey_answer_distrtibution.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()



    #Creating groups
    groups = {
        'Programming / Programowanie': ['CLI', 'Docker', 'Front End', 'Bash', 'Python', 'R', 'GIT'],
        'Data Analysis / Analiza Danych': ['Classical ML', 'Computer Vision', 'NLP', 'Time Series', 'PowerBI', 'Tableau'],
        'Soft Skills / Umiejętności miękkie': ['Relacje z Biznesem', 'Relacje z naukowcami', 'Pozyskiwanie finansowania', 'Project Management', 'Projektowanie graficzne', 'Social Media', 'Ux/Ui', 'Współpraca z administracją UEW'],
        'Cloud & DBs / Chmury i bazy danych': ['AWS', 'Azure', 'GPC', 'NoSQL', 'SQL'],
        'Industries / Branże': ['Cybersecurity', 'E-commerce', 'FashionTech', 'FinTech', 'HealthTech', 'HR', 'Non-profit', 'PropTech', 'SportTech']
    }

    #Extracting the list of columns based on groups
    ordered_columns = [col for group in groups.values() for col in group]
    #Reordering the DataFrame columns based on groups
    df_ordered = df[ordered_columns]

    #Creating Spearman rank correlation matrix
    correlation_df = df_ordered
    correlation = correlation_df.corr(method='spearman')

    plt.figure(figsize=(16, 12), dpi=100)
    plt.title('Spearman Rank Correlation Matrix / Macierz korelacji rang Spearmana')
    plt.rcParams.update({'font.size': 8})
    mask = np.triu(np.ones_like(correlation, dtype=bool))

    sns.heatmap(correlation, cmap='coolwarm', vmin=-1, vmax=1, center=0, annot=True, mask=mask, fmt='.2f', 
                xticklabels=ordered_columns, yticklabels=ordered_columns)

    #Adding lines to separate the groups
    current_index = 0
    for group, columns in groups.items():
        next_index = current_index + len(columns)
        plt.axhline(y=next_index, color='black', linewidth=2)
        plt.axvline(x=next_index, color='black', linewidth=2)
        current_index = next_index

    #Adding group names
    for i, (group, columns) in enumerate(groups.items()):
        group_start = ordered_columns.index(columns[0])
        group_end = ordered_columns.index(columns[-1])
        group_center = (group_start + group_end) / 2
        plt.text(group_center, len(ordered_columns) + 8, group, ha='center', va='center', color='black', fontsize=8,
                bbox=dict(facecolor='white', alpha=0.2, boxstyle='round,pad=0.2'))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    #Saving the chart
    figures_dir = os.path.join(repo_root, 'figures')

    save_path = os.path.join(figures_dir, '03_spearman_rank_correlation_matrix_grouped.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()