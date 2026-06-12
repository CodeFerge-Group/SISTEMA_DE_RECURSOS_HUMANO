import hashlib
from core.conexao import ConexaoBD
from core.excecoes import ErroPersistencia
from models.colaborador import Colaborador
from core.utilitarios import log_operacao

class ColaboradorDAO:
    def __init__(self):
        self.db_manager = ConexaoBD()

    @log_operacao
    def autenticar(self, email, senha_limpa):
        email_limpo = email.strip()
        senha_hash = hashlib.sha256(senha_limpa.strip().encode()).hexdigest()
        
        with self.db_manager as db:
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM colaboradores WHERE LOWER(email) = LOWER(%s) AND senha_hash = %s AND status = 'Ativo'"
            cursor.execute(query, (email_limpo, senha_hash))
            linha = cursor.fetchone()
            
            if linha:
                return Colaborador(
                    id_entidade=linha["id"],
                    nome=linha["nome"],
                    email=linha["email"],
                    cargo=linha["cargo"],
                    salario=float(linha["salario"]),
                    data_admissao=linha["data_admissao"],
                    departamento_id=linha["departamento_id"]
                )
        return None

    def listar_todos_metricas(self):
        with self.db_manager as db:
            cursor = db.cursor(dictionary=True)
            query = """
                SELECT c.*, d.nome as departamento,
                       COALESCE(a.horas_extra, 0) as horas_extra,
                       COALESCE(av.nota_desempenho, 0) as nota_desempenho,
                       COALESCE(av.indice_satisfacao, 0) as indice_satisfacao
                FROM colaboradores c
                LEFT JOIN departamentos d ON c.departamento_id = d.id
                LEFT JOIN assiduidade a ON c.id = a.colaborador_id
                LEFT JOIN avaliacoes av ON c.id = av.colaborador_id
                WHERE c.status = 'Ativo'
            """
            cursor.execute(query)
            return cursor.fetchall()

    @log_operacao
    def cadastrar(self, colab_obj, senha_limpa):
        senha_hash = hashlib.sha256(senha_limpa.encode()).hexdigest()
        with self.db_manager as db:
            cursor = db.cursor()
            query = """
                INSERT INTO colaboradores (nome, email, senha_hash, cargo, salario, data_admissao, departamento_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(query, (
                    colab_obj.nome, colab_obj.email, senha_hash, 
                    colab_obj.cargo, colab_obj.salario, colab_obj.data_admissao, 
                    colab_obj.departamento_id
                ))
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise ErroPersistencia(f"Erro ao salvar funcionário: {e}")

    def inativar(self, id_colab):
        with self.db_manager as db:
            cursor = db.cursor()
            try:
                cursor.execute("UPDATE colaboradores SET status = 'Inativo' WHERE id = %s", (id_colab,))
                db.commit()
                return True
            except:
                db.rollback()
                return False

    def listar_departamentos(self):
        with self.db_manager as db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM departamentos")
            return cursor.fetchall()
