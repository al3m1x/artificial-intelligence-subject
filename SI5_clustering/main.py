from k_means import k_means
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def load_iris(): # wczytanie zestawu danych
    data = pd.read_csv("data/iris.data", names=["sepal_length", "sepal_width", "petal_length", "petal_width", "class"])
    print(data)
    classes = data["class"].to_numpy()
    features = data.drop("class", axis=1).to_numpy()
    return features, classes

def evaluate(clusters, labels): # wykazanie zawartości danych klastrów
    for cluster in np.unique(clusters):
        labels_in_cluster = labels[clusters==cluster]
        print(f"Cluster: {cluster}")
        for label_type in np.unique(labels):
            print(f"Num of {label_type}: {np.sum(labels_in_cluster==label_type)}")
    

"""
W zależności od inicjalizacji centroidów możemy otrzymywać różne jej wartości. W celu ograniczenia ryzyka wylosowania złych punktów 
startowych, częstą praktyką jest uruchamianie k-means wielokrotnie i porównywanie średniej odległości od centroidów pomiędzy nimi.
"""
def clustering(kmeans_pp):
    features, classes = load_iris()
    intra_class_variance = []
    for i in range(100):
        assignments, centroids, error = k_means(features, 3, kmeans_pp)
        evaluate(assignments, classes)
        intra_class_variance.append(error)
    print(f"Mean intra-class variance: {np.mean(intra_class_variance)}")

    plt.figure(figsize=(8, 6)) # wykres dopasowania elementów do klastrów
    plt.scatter(features[:, 0], features[:, 1], c=assignments, s=50, alpha=0.5, label='Data Points')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, marker='X', label='Centroids')
    plt.title('K-means Clustering')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    clustering(kmeans_pp = True)
    #clustering(kmeans_pp = False)
