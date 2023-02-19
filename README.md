# babybear 🐼

*A microscopic, functional data manipulation tool based on `pandas`.*

## Motivation

I wanted to teach data manipulation in Python. But people come in with various
levels of prior Python experience, and may not be comfortable with
[Python environments](https://xkcd.com/1987/) or packages yet.

`babybear` implements a pure-Python DataFrame with *select*, *where*,
*function application*, *reduce aggregation*, and
*slice indexing*. All in ~40 lines of code.

Those familiar with functional programming may recognize these as
`map`, `filter`, and `reduce` operations:

```python
import babybear as bb

df = bb.read_csv("penguins-sample.csv")

# Compute the maximum body mass for penguins with a bill length > 49
max_body_mass = (
    df.apply(float, ["bill_length_mm", "body_mass_g"])      # map
    .where(lambda row: row["bill_length_mm"] > 49)          # filter
    .reduce(max, "body_mass_g")                             # reduce
)

print(max_body_mass)
# 5400.0
```

## Installation

Just copy and paste it. It only uses the Python standard library and
should be compatible with Python 3.7+

**penguin-sample.csv**:

```csv
species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex,year
"Adelie","Torgersen",39.1,18.7,181,3750,"male",2007
"Adelie","Dream",42.3,21.2,191,4150,"male",2007
"Adelie","Biscoe",39.6,17.7,186,3500,"female",2008
"Gentoo","Biscoe",46.1,13.2,211,4500,"female",2007
"Gentoo","Biscoe",49.9,16.1,nan,5400,nan,2009
"Chinstrap","Dream",46.5,17.9,192,3500,"female",2007
"Chinstrap","Dream",50,19.5,196,3900,"male",2007
```

**babybear.py**:

```python
# Copyright 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing!

from csv import DictReader, DictWriter
from typing import Callable, Dict, List, Union
from os import PathLike


class DataFrame:
    def __init__(self, data: List[Dict[str, str]]):
        self.data = data
        self.columns = list(data[0].keys())

    def apply(self, func: Callable, columns: List[str]):
        for c in columns:
            for row in self.data:
                row[c] = func(row[c])
        return self

    def reduce(self, func: Callable, column: str):
        return func(row[column] for row in self.data)

    def where(self, predicate: Callable):
        subset = [{c: row[c] for c in self.columns} for row in self.data if predicate(row)]  # fmt: skip
        return DataFrame(data=subset)

    def to_csv(self, file_name: Union[str, PathLike]) -> None:
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


def read_csv(file_name: Union[str, PathLike]) -> DataFrame:
    with open(file_name, "r") as fh:
        reader = DictReader(fh, delimiter=",", quotechar='"')
        return DataFrame([row for row in reader])
```

## Differences from `pandas`

There are too many to name, I'm trying to be minimal here!

Here's the weird one: *everything is a string by default*. If you want numeric comparison, you have to convert types with `apply`, or convert types on the fly:

```python
df.where(lambda row: float(row["bill_length_mm"]) > 49)
```

A few cases worth mentioning (e.g. if you're teaching with this and need to
jump into `pandas` at the end, or if you're using this as a bridge between
talking about Python data structures and SQL).

1. `read_csv` assumes comma delimiters, double-quoted quotes `"`, and `nan` representing missing values.
2. `babybear` supports directly on the object (you can do `df[0]` to get the first row, without having to do `df.iloc[0]`). In general you can do: `df[...]` for rows and `df[[...]]` for columns.
3. `babybear` uses `where()` like a `SELECT WHERE` statement. Instead of writing `df[df['species'] == 'Adelie']`, you'd write: `df.where(lambda row: row['species'] == "Adelie")`
4. `babybear` does not have a `Series` object.
5. `babybear` does not support `__setitem__`. You can *select* columns, but cannot add a new column with `df["new_column"] = ...`.

## API Examples

Load a `DataFrame` from a `.csv` file:

```python
import babybear as bb

df = bb.read_csv("penguins-sample.csv")
```

Select the `"species"` and `"island"` columns from `df`:

```python
df[["species", "island"]]
# {'species': 'Adelie', 'island': 'Torgersen'}
# ...
# {'species': 'Chinstrap', 'island': 'Dream'}
# 7 rows, 2 columns
```

Select the first row:

```python
df[0]
# {'species': 'Adelie', 'island': 'Torgersen', 'bill_length_mm': '39.1', 'bill_depth_mm': '18.7', 'flipper_length_mm': '181', 'body_mass_g': '3750', 'sex': 'male', 'year': '2007'}
# 1 rows, 8 columns
```

Select the first three rows:

```python
df[:3]
# ...
# 3 rows, 8 columns
```

Select rows between `1:3`:

```python
df[1:3]
# ...
# 2 rows, 8 columns
```

Select the last (`-1`) row:

```python
df[-1]
# {'species': 'Chinstrap', 'island': 'Dream', 'bill_length_mm': '50', 'bill_depth_mm': '19.5', 'flipper_length_mm': '196', 'body_mass_g': '3900', 'sex': 'male', 'year': '2007'}
# 1 rows, 8 columns
```

Select the `"species"` column for penguins where the `"island"` column is `"Dream"`:

```python
df.where(lambda row: row["island"] == "Dream")[["species"]]
# {'species': 'Adelie'}
# {'species': 'Chinstrap'}
# {'species': 'Chinstrap'}
# 3 rows, 1 columns
```
