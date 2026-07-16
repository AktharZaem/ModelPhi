from collections import Counter


class ConfusionMatrix(list):
    @property
    def shape(self):
        return (len(self), len(self[0]) if self else 0)

    def max(self):
        return max((max(row) for row in self), default=0)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            row_index, column_index = item
            return list.__getitem__(self, row_index)[column_index]
        return list.__getitem__(self, item)


def _as_list(values):
    if hasattr(values, "_data"):
        return list(values._data)
    return list(values)


def accuracy_score(y_true, y_pred):
    true_values = _as_list(y_true)
    predicted_values = _as_list(y_pred)
    if not true_values:
        return 0.0
    matches = sum(1 for expected, actual in zip(
        true_values, predicted_values) if expected == actual)
    return matches / len(true_values)


def confusion_matrix(y_true, y_pred):
    true_values = _as_list(y_true)
    predicted_values = _as_list(y_pred)
    labels = []
    for value in true_values + predicted_values:
        if value not in labels:
            labels.append(value)
    matrix = [[0 for _ in labels] for _ in labels]
    label_to_index = {label: index for index, label in enumerate(labels)}
    for expected, actual in zip(true_values, predicted_values):
        matrix[label_to_index[expected]][label_to_index[actual]] += 1
    return ConfusionMatrix(matrix)


def classification_report(y_true, y_pred, output_dict=False):
    true_values = _as_list(y_true)
    predicted_values = _as_list(y_pred)
    labels = []
    for value in true_values + predicted_values:
        if value not in labels:
            labels.append(value)

    report = {}
    lines = []
    total_correct = sum(1 for expected, actual in zip(
        true_values, predicted_values) if expected == actual)
    accuracy = total_correct / len(true_values) if true_values else 0.0

    for label in labels:
        true_positive = sum(1 for expected, actual in zip(
            true_values, predicted_values) if expected == label and actual == label)
        false_positive = sum(1 for expected, actual in zip(
            true_values, predicted_values) if expected != label and actual == label)
        false_negative = sum(1 for expected, actual in zip(
            true_values, predicted_values) if expected == label and actual != label)
        support = sum(1 for expected in true_values if expected == label)

        precision = true_positive / \
            (true_positive + false_positive) if (true_positive + false_positive) else 0.0
        recall = true_positive / \
            (true_positive + false_negative) if (true_positive + false_negative) else 0.0
        f1_score = (2 * precision * recall / (precision + recall)
                    ) if (precision + recall) else 0.0

        report[label] = {
            "precision": precision,
            "recall": recall,
            "f1-score": f1_score,
            "support": support,
        }
        lines.append(
            f"{label:>12}  {precision:0.2f}  {recall:0.2f}  {f1_score:0.2f}  {support:>6}")

    weighted_support = len(true_values)
    report["accuracy"] = accuracy
    report["macro avg"] = {
        "precision": sum(entry["precision"] for entry in report.values() if isinstance(entry, dict) and "precision" in entry) / len(labels) if labels else 0.0,
        "recall": sum(entry["recall"] for entry in report.values() if isinstance(entry, dict) and "recall" in entry) / len(labels) if labels else 0.0,
        "f1-score": sum(entry["f1-score"] for entry in report.values() if isinstance(entry, dict) and "f1-score" in entry) / len(labels) if labels else 0.0,
        "support": weighted_support,
    }
    report["weighted avg"] = dict(report["macro avg"])

    if output_dict:
        return report

    header = "              precision    recall  f1-score   support"
    body = "\n".join(lines)
    footer = f"\n\n    accuracy                          {accuracy:0.2f}      {len(true_values)}"
    return f"{header}\n{body}{footer}"
