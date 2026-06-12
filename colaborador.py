from models.abstrato import EntidadeAbstrata

class Colaborador(EntidadeAbstrata):

    def __init__(self, nome, email, cargo, salario, data_admissao, departamento_id, id_entidade=None):
        super().__init__(id_entidade)
        self.nome = nome
        self.email = email
        self.cargo = cargo
        self.salario = float(salario)
        self.data_admissao = data_admissao
        self.departamento_id = departamento_id

    def validar(self):

        if not self.nome or "@" not in self.email:
            return False
        if self.salario <= 0:
            return False
        return True

    def __str__(self):
        return f"{self.nome} ({self.cargo})"
