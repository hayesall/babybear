# Copyright 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing!

"""
A microscopic data manipulation tool based on `pandas`.
"""

__all__ = ["read_csv", "DataFrame"]

from csv import DictReader, DictWriter
from typing import Callable, Dict, List, Union


class DataFrame:
    def __init__(self, data: List[Dict[str, str]]):
        self.data = data
        self.columns = list(data[0].keys())

    def mean(self, column: str) -> float:
        values = [float(row[column]) for row in self.data if row[column] != "nan"]
        return sum(values) / len(values)

    def where(self, predicate: Callable):
        subset = [{c: row[c] for c in self.columns} for row in self.data if predicate(row)]  # fmt: skip
        return DataFrame(data=subset)

    def to_csv(self, file_name: str) -> None:
        with open(file_name, "w") as fh:
            writer = DictWriter(fh, fieldnames=self.columns)
            writer.writeheader()
            writer.writerows(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key: Union[slice, int, List[str]]):
        if isinstance(key, slice):
            return DataFrame(data=self.data[key])
        elif isinstance(key, int):
            return DataFrame(data=[self.data[key]])
        elif isinstance(key, list):
            subset = [{c: row[c] for c in key} for row in self.data]
            return DataFrame(data=subset)
        raise TypeError(f"Unknown type {type(key)}")

    def __repr__(self):
        return "\n".join(d.__repr__() for d in self.data[:3]) + "\n...\n" + "\n".join(d.__repr__() for d in self.data[-3:]) + f"\n{len(self)} rows, {len(self.columns)} columns" if len(self) > 10 else "\n".join(d.__repr__() for d in self.data) + f"\n{len(self)} rows, {len(self.columns)} columns"  # fmt: skip


def read_csv(file_name: str) -> DataFrame:
    with open(file_name, "r") as fh:
        reader = DictReader(fh, delimiter=",", quotechar='"')
        return DataFrame([row for row in reader])