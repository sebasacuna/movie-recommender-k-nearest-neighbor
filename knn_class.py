from collections import Counter
import math
import pandas as pd


def knn(data, query, k, distance_fn, choice_fn, movies_names_and_index):
    neighbor_distances_and_indices = []
    dataframe_panda_data = []
    # 3. For each example in the data
    for index, example in enumerate(data):
        # 3.1 Calculate the distance between the query example and the current
        # example from the data.
        distance = distance_fn(example[:-1], query)

        # 3.2 Add the distance and the index of the example to an ordered collection
        neighbor_distances_and_indices.append((distance, index))

        # 3.3 save the value to panda
        dataframe_panda_data.append({'distance': distance, 'indx': index})

    df = pd.DataFrame(dataframe_panda_data)

    plot = df.plot(x='distance', y='indx', marker='.', style='o', kind='scatter')
    df.apply(lambda item: plot.annotate(movies_names_and_index[item['indx'].astype(int)], (item.distance, item.indx * 1.02)), axis=1)

    fig = plot.get_figure()
    fig.savefig("output.png")

    # 4. Sort the ordered collection of distances and indices from
    # smallest to largest (in ascending order) by the distances
    sorted_neighbor_distances_and_indices = sorted(neighbor_distances_and_indices)

    # 5. Pick the first K entries from the sorted collection
    k_nearest_distances_and_indices = sorted_neighbor_distances_and_indices[:k]

    # 6. Get the labels of the selected K entries
    k_nearest_labels = [data[i][1] for distance, i in k_nearest_distances_and_indices]

    # 7. If regression (choice_fn = mean), return the average of the K labels
    # 8. If classification (choice_fn = mode), return the mode of the K labels
    return k_nearest_distances_and_indices, choice_fn(k_nearest_labels)


def euclidean_distance(point1, point2):
    sum_squared_distance = 0
    for i in range(len(point1)):
        sum_squared_distance += math.pow(point1[i] - point2[i], 2)
    return math.sqrt(sum_squared_distance)
