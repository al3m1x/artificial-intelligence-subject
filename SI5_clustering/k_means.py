import numpy as np

def initialize_centroids_forgy(data, k): # losowanie k centroidów spośród obserwacji
    indexes = np.random.choice(data.shape[0], size=k, replace=False)
    centroids = data[indexes] # zbieramy koordynaty pod tymi indeksami
    return centroids

def initialize_centroids_kmeans_pp(data, k):
    centroids = [data[np.random.randint(data.shape[0])]] # wybieramy losowo pierwszy centroid

    for _ in range(1, k):
        distances = np.array([sum(np.linalg.norm(point - centroid) ** 2 for centroid in centroids) for point in data]) # obliczamy sumę odległości danych punktów od wszystkich centroidów
        max_distance_index = np.argmax(distances) # wybieramy indeks argumentu, którego suma odległości od centroidów była najwyższa
        centroids.append(data[max_distance_index]) # wpisanie do listy centroids

    return np.array(centroids)


def assign_to_cluster(data, centroids):
    # szukany jest centroid który jest najbliżej danego punktu, przypisywania zapisywane są w assignments
    distances = np.array([[np.linalg.norm(point - centroid) ** 2 for centroid in centroids] for point in data])
    assignments = np.argmin(distances, axis=1)

    return assignments

def update_centroids(data, assignments):
    new_centroids = []
    for centroid_index in np.unique(assignments): # iterujemy po indexach centroidów
        points_for_centroid = data[assignments == centroid_index] # wybieramy punkty z danym przypisaniem
        new_centroid = np.mean(points_for_centroid, axis=0) # nowym centroidem jest średnia współrzędnych centroidów należących do danego centroidu
        new_centroids.append(new_centroid)
    return np.array(new_centroids)

def mean_intra_distance(data, assignments, centroids): # średnia odległość punktu przypisanego do danego centroidu od niego
    return np.sqrt(np.sum((data - centroids[assignments, :])**2))

def k_means(data, num_centroids, kmeansplusplus= False):
    # centroids initizalization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else: 
        centroids = initialize_centroids_forgy(data, num_centroids)

    
    assignments  = assign_to_cluster(data, centroids)
    for i in range(100): # max number of iteration = 100
        print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments): # stop if nothing changed
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, centroids)         

