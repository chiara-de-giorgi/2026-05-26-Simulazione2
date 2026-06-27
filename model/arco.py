from dataclasses import dataclass

from model.names import Names


@dataclass
class Arco:
    n1: Names
    n2: Names
    peso: int