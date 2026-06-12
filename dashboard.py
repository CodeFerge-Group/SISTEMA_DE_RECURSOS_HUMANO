import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from dao.colaborador_dao import ColaboradorDAO
from ia.preditor import PreditorChurnIA
from gui.componentes import BotaoPersonalizado
from gui.colaboradores_gui import JanelaColaboradores
from gui.rh_operacoes_gui import JanelaRHOperacoes
from core.excecoes import ErroSistemaRH


class DashboardPrincipal(ctk.CTk):

    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.title(f"Core HR Intelligence - Operador: {admin.nome}")
        self.geometry("1150x700")

        # Injeção de Dependências
        self.dao_colaboradores = ColaboradorDAO()
        self.motor_ia = PreditorChurnIA()
        
        self.inicializar_interface()

    def inicializar_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Menu Lateral (Estilo Moderno)
        self.menu_lateral = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.menu_lateral, text="SISTEMA RH IA", font=("Arial", 22, "bold"), text_color="#3498db").pack(pady=40)

        BotaoPersonalizado(self.menu_lateral, "👥 Colaboradores", self.abrir_colaboradores).pack(pady=10, padx=20, fill="x")
        BotaoPersonalizado(self.menu_lateral, "💰 Folha Salarial", lambda: self.abrir_operacoes("Folha")).pack(pady=10, padx=20, fill="x")
        BotaoPersonalizado(self.menu_lateral, "📅 Assiduidade", lambda: self.abrir_operacoes("Assiduidade")).pack(pady=10, padx=20, fill="x")
        BotaoPersonalizado(self.menu_lateral, "📊 Desempenho", lambda: self.abrir_operacoes("Desempenho")).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.menu_lateral, text="STATUS: CONECTADO", text_color="#2ecc71", font=("Arial", 10, "bold")).pack(side="bottom", pady=20)

        # Painel Central com Scroll
        self.painel_central = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="#242424")
        self.painel_central.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.atualizar_dados_dashboard()

    def atualizar_dados_dashboard(self):

        try:
            for widget in self.painel_central.winfo_children():
                widget.destroy()

            # Busca dados via DAO (Abstração de Dados)
            self.colaboradores_cache = self.dao_colaboradores.listar_todos_metricas()
            
            self.construir_cards_metricas()
            self.construir_secao_ia()
            self.construir_graficos()
            
        except ErroSistemaRH as e:
            from tkinter import messagebox
            messagebox.showerror("Erro de Sistema", str(e))

    def abrir_colaboradores(self):
        JanelaColaboradores(self)
        
    def abrir_operacoes(self, aba):
        JanelaRHOperacoes(self, aba)

    def construir_cards_metricas(self):
        frame_cards = ctk.CTkFrame(self.painel_central, fg_color="transparent")
        frame_cards.pack(fill="x", pady=10)

        total_colab = len(self.colaboradores_cache)
        salario_total = sum(c['salario'] for c in self.colaboradores_cache)
        
        # Widgets de Métricas Rápidas
        self._criar_card(frame_cards, "QUADRO ATIVO", str(total_colab), "#2ecc71")
        self._criar_card(frame_cards, "FOLHA TOTAL", f"{salario_total:,.2f} Kz", "#e67e22")
        self._criar_card(frame_cards, "DEP. ATIVOS", "5", "#3498db")

    def _criar_card(self, master, titulo, valor, cor):
        card = ctk.CTkFrame(master, fg_color="#1e1e1e", border_width=1, border_color="#333")
        card.pack(side="left", padx=10, expand=True, fill="both")
        ctk.CTkLabel(card, text=titulo, font=("Arial", 11, "bold"), text_color="#aaa").pack(pady=(10, 0))
        ctk.CTkLabel(card, text=valor, font=("Arial", 20, "bold"), text_color=cor).pack(pady=(5, 15))

    def construir_secao_ia(self):

        frame_ia = ctk.CTkFrame(self.painel_central, fg_color="#1e1e1e", border_width=2, border_color="#3498db")
        frame_ia.pack(fill="x", padx=10, pady=20)

        ctk.CTkLabel(frame_ia, text="🔮 ANÁLISE PREDITIVA DE ROTATIVIDADE (CHURN RATE)", 
                     font=("Arial", 14, "bold"), text_color="#3498db").pack(pady=15)
        
        # Simulador Integrado com o Motor de IA
        ctk.CTkLabel(frame_ia, text="Simulação baseada em Exaustão (Horas Extras Mensais):", font=("Arial", 12)).pack()
        self.sld_horas = ctk.CTkSlider(frame_ia, from_=0, to=80, command=self.executar_predicao_ia, width=500)
        self.sld_horas.set(20)
        self.sld_horas.pack(pady=10)

        self.lbl_ia_res = ctk.CTkLabel(frame_ia, text="Selecione as horas para calcular o risco...", font=("Arial", 13, "bold"))
        self.lbl_ia_res.pack(pady=15)
        self.executar_predicao_ia()

    def executar_predicao_ia(self, event=None):

        hrs = self.sld_horas.get()
        # Mock de satisfação média para simulação global
        prob, status = self.motor_ia.prever_risco(hrs, 7.5, 3)
        
        cor = "#2ecc71" if prob < 30 else "#f1c40f" if prob < 70 else "#e74c3c"
        self.lbl_ia_res.configure(text=f"PROBABILIDADE DE CHURN: {prob}% | CLASSIFICAÇÃO: {status}", text_color=cor)

    def construir_graficos(self):

        frame_plot = ctk.CTkFrame(self.painel_central, fg_color="#1e1e1e")
        frame_plot.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_plot, text="DISTRIBUIÇÃO SALARIAL POR DEPARTAMENTO", font=("Arial", 12, "bold")).pack(pady=10)

        fig, ax = plt.subplots(figsize=(6, 3), facecolor="#1e1e1e")
        ax.set_facecolor("#1e1e1e")
        
        deps = {}
        for c in self.colaboradores_cache:
            d = c['departamento'] or "N/D"
            deps[d] = deps.get(d, 0) + c['salario']
        
        if deps:
            ax.bar(deps.keys(), deps.values(), color="#3498db")
            ax.tick_params(colors='white', labelsize=8)
            for spine in ax.spines.values(): spine.set_color('#444')
        
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
