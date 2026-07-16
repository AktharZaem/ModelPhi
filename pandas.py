import csv
from collections import Counter


class Columns(list):
    def tolist(self):
        return list(self)


class _ILocAccessor:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, index):
        return self._data[index]


class Series:
    def __init__(self, data=None, name=None):
        self._data = list(data or [])
        self.name = name

    @property
    def shape(self):
        return (len(self._data),)

    @property
    def empty(self):
        return len(self._data) == 0

    @property
    def iloc(self):
        return _ILocAccessor(self._data)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __repr__(self):
        return f"Series({self._data!r})"

    def _subset(self, indices):
        return Series([self._data[i] for i in indices], name=self.name)

    def unique(self):
        seen = []
        for value in self._data:
            if value not in seen:
                seen.append(value)
        return seen

    def dropna(self):
        return Series([value for value in self._data if value not in (None, "")], name=self.name)

    def mode(self):
        values = [value for value in self._data if value not in (None, "")]
        if not values:
            return Series([], name=self.name)
        counts = Counter(values)
        highest = max(counts.values())
        return Series([value for value, count in counts.items() if count == highest], name=self.name)

    def astype(self, value_type):
        return Series([value_type(value) for value in self._data], name=self.name)

    def apply(self, func):
        return Series([func(value) for value in self._data], name=self.name)

    def value_counts(self):
        return Counter(self._data)


class DataFrame:
    def __init__(self, data=None, columns=None):
        self._rows = []
        self._columns = []

        if data is None:
            self._columns = list(columns or [])
            return

        if isinstance(data, dict):
            keys = list(data.keys())
            lengths = [len(values)
                       for values in data.values()] if data else [0]
            row_count = max(lengths) if lengths else 0
            self._columns = list(columns or keys)
            for index in range(row_count):
                row = {}
                for key in self._columns:
                    values = data.get(key, [])
                    row[key] = values[index] if index < len(values) else ""
                self._rows.append(row)
            return

        for row in data:
            self._rows.append(dict(row))

        if columns is not None:
            self._columns = list(columns)
        else:
            seen = []
            for row in self._rows:
                for key in row.keys():
                    if key not in seen:
                        seen.append(key)
            self._columns = seen

    @property
    def rows(self):
        return [dict(row) for row in self._rows]

    @property
    def columns(self):
        return Columns(self._columns)

    @property
    def shape(self):
        return (len(self._rows), len(self._columns))

    @property
    def empty(self):
        return len(self._rows) == 0

    def __len__(self):
        return len(self._rows)

    def __repr__(self):
        return f"DataFrame(rows={len(self._rows)}, columns={self._columns!r})"

    def _subset(self, indices):
        return DataFrame([self._rows[i] for i in indices], columns=self._columns)

    def to_rows(self):
        return [dict(row) for row in self._rows]

    def to_matrix(self, columns=None):
        use_columns = list(columns or self._columns)
        matrix = []
        for row in self._rows:
            matrix.append([row.get(column, 0) for column in use_columns])
        return matrix

    def __getitem__(self, key):
        if isinstance(key, str):
            return Series([row.get(key, "") for row in self._rows], name=key)
        if isinstance(key, (list, tuple)):
            return DataFrame([
                {column: row.get(column, "") for column in key}
                for row in self._rows
            ], columns=list(key))
        raise TypeError(f"Unsupported key type: {type(key)!r}")

    def __setitem__(self, key, value):
        if isinstance(value, Series):
            values = list(value)
        elif isinstance(value, (list, tuple)):
            values = list(value)
        else:
            values = [value] * len(self._rows)

        if key not in self._columns:
            self._columns.append(key)

        for index, row in enumerate(self._rows):
            row[key] = values[index] if index < len(values) else ""

    def drop(self, columns=None):
        columns = list(columns or [])
        return DataFrame([
            {key: value for key, value in row.items() if key not in columns}
            for row in self._rows
        ])

    def iterrows(self):
        for index, row in enumerate(self._rows):
            yield index, dict(row)


def read_csv(file_path):
    with open(file_path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return DataFrame(list(reader), columns=reader.fieldnames or [])


def concat(frames, ignore_index=False, axis=0):
    frames = [frame for frame in frames if frame is not None]
    if not frames:
        return DataFrame()

    if axis == 1:
        row_count = max(len(frame) for frame in frames)
        combined_rows = []
        columns = []
        for frame in frames:
            for column in frame.columns:
                if column not in columns:
                    columns.append(column)
        for index in range(row_count):
            row = {}
            for frame in frames:
                if index < len(frame._rows):
                    row.update(frame._rows[index])
            combined_rows.append(row)
        return DataFrame(combined_rows, columns=columns)

    combined_rows = []
    columns = []
    for frame in frames:
        for column in frame.columns:
            if column not in columns:
                columns.append(column)
        combined_rows.extend(frame.to_rows())
    return DataFrame(combined_rows, columns=columns)


def get_dummies(series, prefix=""):
    values = list(series)
    unique_values = []
    for value in values:
        if value not in unique_values:
            unique_values.append(value)

    columns = [f"{prefix}_{value}" for value in unique_values]
    rows = []
    for value in values:
        row = {}
        for column, unique_value in zip(columns, unique_values):
            row[column] = 1 if value == unique_value else 0
        rows.append(row)
    return DataFrame(rows, columns=columns)
