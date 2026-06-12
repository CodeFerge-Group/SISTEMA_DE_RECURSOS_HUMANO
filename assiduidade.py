from models.abstrato import EntidadeAbstrata

class Assiduidade(EntidadeAbstrata):
    def __init__(self, colaborador_id, horas_extra=0.0, id_entidade=None):
        super().__init__(id_entidade)
        self._colaborador_id = colaborador_id
        self.horas_extra = horas_extra 

    @property
    def colaborador_id(self):
        return self._colaborador_id

    @property
    def horas_extra(self):
        return self._horas_extra

    @horas_extra.setter
    def horas_extra(self, valor):
        if float(valor) < 0:
            self._horas_extra = 0.0
        else:
            self._horas_extra = float(valor)

    def converter_para_dicionario(self) -> dict:
        return {
            "id": self.id,
            "colaborador_id": self._colaborador_id,
            "horas_extra": self._horas_extra
        }
