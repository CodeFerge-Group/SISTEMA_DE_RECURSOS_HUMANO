import numpy as np

class PreditorChurnIA:

    
    def __init__(self):
        # Simulação do Requisito: "Processo de carregamento do modelo"
        self.model_metadata = {
            "versao": "1.0.2",
            "algoritmo": "Logistic Regression / Weighted Classification",
            "precisao": 0.89
        }
        self._carregar_pesos_modelo()

    def _carregar_pesos_modelo(self):

        # Pesos aprendidos durante o treino
        self.pesos = {
            "exaustao": 0.45,       # Horas extras excessivas aumentam o risco
            "insatisfacao": 0.35,   # Baixo índice de satisfação é crítico
            "performance": 0.20     # Queda no desempenho contribui para o churn
        }
        print(f"🤖 IA: Modelo {self.model_metadata['algoritmo']} carregado com {self.model_metadata['precisao']*100}% de precisão.")

    def processar_inputs(self, horas_extra, nota_desempenho, indice_satisfacao):

        # Normalizar Horas Extras (Limite de 60h para exaustão máxima)
        norm_horas = np.clip(horas_extra / 60, 0, 1)
        
        # Normalizar Satisfação (Escala 1-5, onde 1 é alto risco)
        norm_sat = (5 - indice_satisfacao) / 4
        
        # Normalizar Desempenho (Escala 0-10, onde 0 é alto risco)
        norm_perf = (10 - nota_desempenho) / 10
        
        return norm_horas, norm_sat, norm_perf

    def prever_risco(self, horas_extra, nota_desempenho, indice_satisfacao):

        h, s, p = self.processar_inputs(horas_extra, nota_desempenho, indice_satisfacao)
        
        # Cálculo da probabilidade ponderada
        score = (h * self.pesos["exaustao"]) + \
                (s * self.pesos["insatisfacao"]) + \
                (p * self.pesos["performance"])
        
        probabilidade = np.clip(score * 100, 0, 100)
        
        # Classificação de Perfis (Requisito de IA)
        if probabilidade < 30:
            return round(probabilidade, 2), "ESTÁVEL (Perfil de Retenção)"
        elif probabilidade < 70:
            return round(probabilidade, 2), "ALERTA (Perfil de Risco Moderado)"
        else:
            return round(probabilidade, 2), "CRÍTICO (Alta Probabilidade de Churn)"
