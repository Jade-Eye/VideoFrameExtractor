from dataclasses import dataclass,field

@dataclass(slots=True)
class FrameDistribution:

    train: set[int]= field(default_factory=set)

    test: set[int]= field(default_factory=set)

    val: set[int]= field(default_factory=set)