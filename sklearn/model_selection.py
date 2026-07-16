import random


def _subset(value, indices):
    if hasattr(value, "_subset"):
        return value._subset(indices)
    if isinstance(value, list):
        return [value[index] for index in indices]
    return [value[index] for index in indices]


def train_test_split(X, y, test_size=0.25, random_state=None, stratify=None):
    total = len(X)
    if total == 0:
        return X, X, y, y

    indices = list(range(total))
    random.Random(random_state).shuffle(indices)

    test_count = max(1, int(round(total * test_size))) if total > 1 else 1
    test_indices = indices[:test_count]
    train_indices = indices[test_count:] or indices[:1]

    return (
        _subset(X, train_indices),
        _subset(X, test_indices),
        _subset(y, train_indices),
        _subset(y, test_indices),
    )
