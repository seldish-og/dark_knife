from abc import ABC, abstractmethod


class MetaObserver(ABC):

    @abstractmethod
    def change(self):
        pass
