import sys
import os

# Add the notebooks folder to the Python path
sys.path.append(os.path.join(os.path.abspath(__file__)))
import raw_data_transformation
import data_processing
import exploratory_analysis
import clustering_hierarchical
import clustering_kmeans

def main():
    print("Welcome to the clustering program! Here we present all the data we have.")
    raw_data_transformation.run()
    data_processing.run()
    exploratory_analysis.run()
    
    while True:
        print("Please choose a clustering method:")
        print("1. Hierarchical Clustering")
        print("2. K-Means Clustering")
        
        choice = input("Enter 1 or 2: ")

        if choice == '1':
            print("You have chosen Hierarchical Clustering.")
            
            clustering_hierarchical.run()
            break
        elif choice == '2':
            print("You have chosen K-Means Clustering.")
            clustering_kmeans.run()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue

if __name__ == "__main__":
    main()
