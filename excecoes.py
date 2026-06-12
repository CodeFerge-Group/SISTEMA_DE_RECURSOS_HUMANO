class ErroSistemaRH(Exception):

    pass

class ErroSistemaRHException(ErroSistemaRH):

    pass

class ErroConexaoBanco(ErroSistemaRH):

    pass

class ErroAutenticacao(ErroSistemaRH):

    pass

class ErroPersistencia(ErroSistemaRH):

    pass
