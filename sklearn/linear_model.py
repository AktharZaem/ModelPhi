from collections import Counter, defaultdict
from math import sqrt


class LogisticRegression:
    def __init__(self, random_state=None, solver=None, multi_class=None, max_iter=None):
        self.random_state = random_state
        self.solver = solver
        self.multi_class = multi_class
        self.max_iter = max_iter
        self.classes_ = []
        self._centroids = {}
        self._majority_class = None
        self.feature_names_in_ = []

    def _to_matrix(self, X):
        if hasattr(X, "to_matrix"):
            matrix = X.to_matrix()
            columns = list(getattr(X, "columns", []))
            return matrix, columns
        if isinstance(X, list) and X and isinstance(X[0], dict):
            columns = []
            for row in X:
                for key in row.keys():
                    if key not in columns:
                        columns.append(key)
            matrix = [[row.get(column, 0) for column in columns] for row in X]
            return matrix, columns
        return [list(row) for row in X], []

    def fit(self, X, y):
        matrix, columns = self._to_matrix(X)
        labels = list(y)
        self.feature_names_in_ = columns
        self.classes_ = sorted(set(labels), key=lambda value: str(value))
        if labels:
            self._majority_class = Counter(labels).most_common(1)[0][0]
        else:
            self._majority_class = None

        grouped = defaultdict(list)
        for vector, label in zip(matrix, labels):
            grouped[label].append(vector)

        for label, vectors in grouped.items():
            if not vectors:
                continue
            centroid = []
            for column_index in range(len(vectors[0])):
                centroid.append(sum(vector[column_index]
                                for vector in vectors) / len(vectors))
            self._centroids[label] = centroid

        return self

    def _predict_vector(self, vector):
        if not self._centroids:
            return self._majority_class

        best_label = None
        best_distance = None
        for label, centroid in self._centroids.items():
            distance = sqrt(
                sum((value - centroid[index]) ** 2 for index, value in enumerate(vector)))
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_label = label
        return best_label if best_label is not None else self._majority_class

    def predict(self, X):
        matrix, _ = self._to_matrix(X)
        return [self._predict_vector(vector) for vector in matrix]
