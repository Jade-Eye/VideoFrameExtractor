from dataclasses import dataclass

@dataclass(slots=True)
class DatasetSplit:
    train: int
    test: int
    val: int