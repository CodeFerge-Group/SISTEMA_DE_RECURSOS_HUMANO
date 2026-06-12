from abc import ABC, abstractmethod

class EntidadeAbstrata(ABC):

    def __init__(self, id_entidade=None):
        self._id = id_entidade

    @property
    def id(self):
        return self._id

    @abstractmethod
    def validar(self):

        pass
