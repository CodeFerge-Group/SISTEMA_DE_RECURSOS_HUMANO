from models.abstrato import EntidadeAbstrata
from core.excecoes import ErroSistemaRH

class Avaliacao(EntidadeAbstrata):

    def __init__(self, colaborador_id, nota_desempenho, indice_satisfacao, id_entidade=None):
        super().__init__(id_entidade)
        self._colaborador_id = colaborador_id
        self.nota_desempenho = nota_desempenho   
        self.indice_satisfacao = indice_satisfacao 

    def validar(self):

        return 0 <= self.nota_desempenho <= 10 and 1 <= self.indice_satisfacao <= 5

    @property
    def colaborador_id(self): 
        return self._colaborador_id

    @property
    def nota_desempenho(self): 
        return self._nota_desempenho

    @nota_desempenho.setter
    def nota_desempenho(self, valor):
        val = float(valor)
        if val < 0 or val > 10:
            raise ErroSistemaRH("A nota de desempenho deve situar-se entre 0.0 e 10.0!")
        self._nota_desempenho = val

    @property
    def indice_satisfacao(self): 
        return self._indice_satisfacao

    @indice_satisfacao.setter
    def indice_satisfacao(self, valor):
        val = int(valor)
        if val < 1 or val > 5:
            raise ErroSistemaRH("O índice de satisfação deve situar-se entre 1 e 5!")
        self._indice_satisfacao = val

    def converter_para_dicionario(self) -> dict:
        return {
            "id": self.id,
            "colaborador_id": self._colaborador_id,
            "nota_desempenho": self._nota_desempenho,
            "indice_satisfacao": self._indice_satisfacao
        }
