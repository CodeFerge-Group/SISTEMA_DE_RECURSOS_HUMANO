import functools
import time

def log_operacao(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        print(f"🚀 [LOG] Iniciando operação: {func.__name__}")
        try:
            resultado = func(*args, **kwargs)
            fim = time.time()
            print(f"✅ [LOG] Operação {func.__name__} concluída em {fim - inicio:.4f}s")
            return resultado
        except Exception as e:
            print(f"❌ [LOG] Falha na operação {func.__name__}: {e}")
            raise e
    return wrapper
