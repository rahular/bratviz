from abc import ABC, abstractmethod
from typing import Dict, List

class Reader(ABC):
    @abstractmethod
    def read(self, fpath: str) -> Dict[str, List[List]]:
        pass