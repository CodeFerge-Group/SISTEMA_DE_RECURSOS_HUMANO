import mysql.connector
from core.excecoes import ErroConexaoBanco

class ConexaoBD:

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexaoBD, cls).__new__(cls)
            cls._instancia.config = {
                'host': 'localhost',
                'user': 'root',
                'password': '1234',
                'database': 'sistema_RH'
            }
        return cls._instancia

    def __enter__(self):

        try:
            self.conn = mysql.connector.connect(**self.config)
            return self.conn
        except mysql.connector.Error as e:
            raise ErroConexaoBanco(f"Falha ao conectar no MySQL: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):

        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()

    def obter_conexao(self):
        return mysql.connector.connect(**self.config)
