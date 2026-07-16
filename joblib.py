import pickle


def dump(value, file_path):
    with open(file_path, "wb") as handle:
        pickle.dump(value, handle)


def load(file_path):
    with open(file_path, "rb") as handle:
        return pickle.load(handle)
