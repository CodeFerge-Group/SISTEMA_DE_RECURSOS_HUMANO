import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path


def treinar_modelo_inicial():
    # Criação de massa de dados sintética realista para o cenário do TFC
    dados = {
        'horas_extra': [10, 45, 5, 50, 12, 38, 0, 42, 8, 35],
        'nota_desempenho': [8.5, 6.2, 9.0, 5.5, 7.8, 6.0, 9.2, 5.8, 8.0, 6.9],
        'indice_satisfacao': [4, 1, 5, 2, 4, 2, 5, 1, 4, 3],
        'salario_vs_mercado': [1.1, 0.7, 1.2, 0.6, 1.0, 0.8, 1.3, 0.7, 0.9, 0.8],
        'churn': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 1 = Demitiu-se, 0 = Estável
    }

    df = pd.DataFrame(dados)
    X = df[['horas_extra', 'nota_desempenho', 'indice_satisfacao', 'salario_vs_mercado']]
    y = df['churn']

    # Modelo Random Forest ideal para classificação e análise probabilística
    modelo = RandomForestClassifier(n_estimators=50, random_state=42)
    modelo.fit(X, y)

    diretoria_ia = Path(__file__).parent
    diretoria_ia.mkdir(exist_ok=True)

    with open(diretoria_ia / "modelo_churn.pkl", "wb") as f:
        pickle.dump(modelo, f)
    print("🤖 IA: Modelo de Churn preditivo treinado e guardado com sucesso!")


if __name__ == "__main__":
    treinar_modelo_inicial()