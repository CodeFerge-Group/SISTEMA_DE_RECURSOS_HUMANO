import sys
import mysql.connector
import hashlib
from core.conexao import ConexaoBD
from gui.login import JanelaLogin
from gui.dashboard import DashboardPrincipal
from core.excecoes import ErroSistemaRHException, ErroConexaoBanco


def verificar_base_dados():

    try:
        conexao_obj = ConexaoBD()
        with conexao_obj as db:
            cursor = db.cursor(dictionary=True)

            # 1. Garantir que as tabelas existem (Script básico de emergência)
            cursor.execute("CREATE TABLE IF NOT EXISTS departamentos (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100))")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS colaboradores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(150),
                    email VARCHAR(100) UNIQUE,
                    senha_hash VARCHAR(255),
                    cargo VARCHAR(100),
                    salario DECIMAL(10,2),
                    data_admissao DATE,
                    departamento_id INT,
                    status VARCHAR(20) DEFAULT 'Ativo'
                )
            """)
            db.commit()

            # 2. Reset Total do Utilizador Admin
            senha_hash = hashlib.sha256("1234".encode()).hexdigest()
            
            # Apagamos qualquer rastro de Admin antigo para evitar conflitos de ID ou Senha
            cursor.execute("DELETE FROM colaboradores WHERE email = 'Admin'")
            
            # Garantir que existe pelo menos um departamento
            cursor.execute("INSERT IGNORE INTO departamentos (id, nome) VALUES (1, 'Administração')")
            db.commit()

            # Inserir o Admin do zero
            query_admin = """
                INSERT INTO colaboradores (nome, email, senha_hash, cargo, salario, data_admissao, departamento_id, status)
                VALUES ('Administrador do Sistema', 'Admin', %s, 'Gestor', 0.0, '2024-01-01', 1, 'Ativo')
            """
            cursor.execute(query_admin, (senha_hash,))
            db.commit()
            
            print(" DATABASE: Utilizador 'Admin' com senha '1234' configurado com sucesso!")

    except Exception as e:
        print(f" Erro Crítico na Base de Dados: {e}")
        # Não paramos o sistema aqui para permitir que o utilizador tente logar se o BD já estiver OK
        pass


def carregar_dashboard(usuario_autenticado):
    app_dashboard = DashboardPrincipal(usuario_autenticado)
    app_dashboard.mainloop()


if __name__ == "__main__":
    # Forçar configuração correta antes de abrir o login
    verificar_base_dados()

    # Abrir interface
    app_login = JanelaLogin(callback_sucesso=carregar_dashboard)
    app_login.mainloop()
