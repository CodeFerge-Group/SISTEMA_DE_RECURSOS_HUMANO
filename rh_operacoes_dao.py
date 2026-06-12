from core.conexao import ConexaoBD

class RHOperacoesDAO:
    def __init__(self):
        self.db_manager = ConexaoBD()

    def registrar_horas(self, colaborador_id, horas_extras):
        with self.db_manager as db:
            cursor = db.cursor()
            query = """
                INSERT INTO assiduidade (colaborador_id, horas_extra) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE horas_extra = horas_extra + %s
            """
            try:
                cursor.execute(query, (colaborador_id, horas_extras, horas_extras))
                db.commit()
                return True
            except:
                return False

    def obter_resumo_folha(self):
        with self.db_manager as db:
            cursor = db.cursor(dictionary=True)
            query = """
                SELECT 
                    c.id, c.nome, c.salario as salario_base,
                    COALESCE(a.horas_extra, 0) as horas_extras,
                    (c.salario / 160 * 1.5 * COALESCE(a.horas_extra, 0)) as valor_horas_extras,
                    (c.salario + (c.salario / 160 * 1.5 * COALESCE(a.horas_extra, 0))) as salario_total
                FROM colaboradores c
                LEFT JOIN assiduidade a ON c.id = a.colaborador_id
                WHERE c.status = 'Ativo'
            """
            cursor.execute(query)
            return cursor.fetchall()

    def registrar_avaliacao(self, colaborador_id, nota_desempenho, indice_satisfacao):
        with self.db_manager as db:
            cursor = db.cursor()
            query = """
                INSERT INTO avaliacoes (colaborador_id, nota_desempenho, indice_satisfacao)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    nota_desempenho = VALUES(nota_desempenho), 
                    indice_satisfacao = VALUES(indice_satisfacao)
            """
            try:
                cursor.execute(query, (colaborador_id, nota_desempenho, indice_satisfacao))
                db.commit()
                return True
            except:
                db.rollback()
                return False

    def obter_todas_assiduidades(self):
        with self.db_manager as db:
            cursor = db.cursor(dictionary=True)
            # Removida a coluna data_atualizacao que causava erro
            query = """
                SELECT c.nome, a.horas_extra
                FROM assiduidade a
                JOIN colaboradores c ON a.colaborador_id = c.id
                WHERE c.status = 'Ativo'
            """
            cursor.execute(query)
            return cursor.fetchall()

    def obter_todas_avaliacoes(self):
        with self.db_manager as db:
            cursor = db.cursor(dictionary=True)
            # Removida a coluna data_avaliacao que causava erro
            query = """
                SELECT c.nome, av.nota_desempenho, av.indice_satisfacao
                FROM avaliacoes av
                JOIN colaboradores c ON av.colaborador_id = c.id
                WHERE c.status = 'Ativo'
            """
            cursor.execute(query)
            return cursor.fetchall()
