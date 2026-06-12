# Sistema de Gestão de RH com Inteligência Artificial (Churn Preditivo)

Este sistema de software inteligente foi desenvolvido como requisito prático para a disciplina de **Linguagem de Programação VI (Python)** no **Instituto Politécnico - UNIKIVI**.

O sistema integra conceitos avançados de Programação Orientada a Objetos (POO), persistência robusta em base de dados relacional MySQL (através de uma arquitetura DAO estrita) e análise preditiva em tempo real com Machine Learning para antever a rotatividade (churn) de colaboradores.

##  Funcionalidades Principais
- **Core HR:** Gestão estruturada de colaboradores, controlo de assiduidade (horas extra) e registo de clima organizacional/satisfação.
- **Preditor de Churn:** Motor de IA baseado no algoritmo Random Forest que estima a probabilidade de demissão de um colaborador.
- **Simulador What-If:** Painel interativo para simulação de políticas de retenção de talentos com recomendações automáticas tomadas pela IA.
- **Interface Desktop Moderna:** Construída em CustomTkinter com dashboards gráficos dinâmicos integrados via Matplotlib.

##  Pré-requisitos e Instalação

1. Instalamos as dependências do projeto listadas no ficheiro de requisitos:
   ```bash
   pip install -r requirements.txt