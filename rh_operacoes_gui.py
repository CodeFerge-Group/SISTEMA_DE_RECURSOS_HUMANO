import customtkinter as ctk
from gui.componentes import BotaoPersonalizado
from dao.rh_operacoes_dao import RHOperacoesDAO
from dao.colaborador_dao import ColaboradorDAO
from tkinter import messagebox

class JanelaRHOperacoes(ctk.CTkToplevel):
    def __init__(self, parent, aba_inicial="Folha"):
        super().__init__(parent)
        self.title("Operações de RH")
        self.geometry("950x750")
        self.dao = RHOperacoesDAO()
        self.dao_colab = ColaboradorDAO()
        self.parent = parent

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_folha = self.tabview.add("Folha de Pagamento")
        self.tab_assiduidade = self.tabview.add("Assiduidade / Horas")
        self.tab_desempenho = self.tabview.add("Avaliação de Desempenho")
        
        self.inicializar_folha()
        self.inicializar_assiduidade()
        self.inicializar_desempenho()
        
        mapeamento = {
            "Folha": "Folha de Pagamento",
            "Assiduidade": "Assiduidade / Horas",
            "Desempenho": "Avaliação de Desempenho"
        }
        self.tabview.set(mapeamento.get(aba_inicial, "Folha de Pagamento"))

    def inicializar_folha(self):
        ctk.CTkLabel(self.tab_folha, text="Resumo Mensal de Folha (Kz)", font=("Arial", 16, "bold")).pack(pady=10)
        self.container_folha = ctk.CTkScrollableFrame(self.tab_folha)
        self.container_folha.pack(fill="both", expand=True, padx=5, pady=5)
        self.carregar_folha()

    def carregar_folha(self):
        for widget in self.container_folha.winfo_children(): widget.destroy()
        dados = self.dao.obter_resumo_folha()
        header = ctk.CTkFrame(self.container_folha, fg_color="#333")
        header.pack(fill="x", pady=2)
        cols = [("Colaborador", 300), ("Salário Base", 150), ("H. Extras", 100), ("Total Mensal", 150)]
        for t, w in cols: ctk.CTkLabel(header, text=t, width=w, font=("Arial", 11, "bold")).pack(side="left", padx=5)

        for d in dados:
            f = ctk.CTkFrame(self.container_folha)
            f.pack(fill="x", pady=1)
            ctk.CTkLabel(f, text=d['nome'], width=300, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(f, text=f"{d['salario_base']:,.2f} Kz", width=150).pack(side="left", padx=5)
            ctk.CTkLabel(f, text=f"{d['horas_extras']}h", width=100).pack(side="left", padx=5)
            ctk.CTkLabel(f, text=f"{d['salario_total']:,.2f} Kz", width=150, font=("Arial", 12, "bold")).pack(side="left", padx=5)

    def inicializar_assiduidade(self):
        ctk.CTkLabel(self.tab_assiduidade, text="Lançamento e Registro de Horas", font=("Arial", 16, "bold")).pack(pady=10)
        form = ctk.CTkFrame(self.tab_assiduidade)
        form.pack(pady=10, padx=20, fill="x")
        
        colabs = self.dao_colab.listar_todos_metricas()
        self.colab_map = {c['nome']: c['id'] for c in colabs}
        
        ctk.CTkLabel(form, text="Colaborador:").grid(row=0, column=0, padx=10, pady=10)
        self.combo_colab = ctk.CTkComboBox(form, values=list(self.colab_map.keys()), width=250)
        self.combo_colab.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(form, text="Horas Extras:").grid(row=0, column=2, padx=10, pady=10)
        self.ent_horas = ctk.CTkEntry(form, placeholder_text="Ex: 5.5")
        self.ent_horas.grid(row=0, column=3, padx=10, pady=10)
        BotaoPersonalizado(form, "Lançar", self.salvar_horas).grid(row=0, column=4, padx=10, pady=10)

        self.container_assiduidade = ctk.CTkScrollableFrame(self.tab_assiduidade)
        self.container_assiduidade.pack(fill="both", expand=True, padx=20, pady=10)
        self.carregar_assiduidade()

    def carregar_assiduidade(self):
        for widget in self.container_assiduidade.winfo_children(): widget.destroy()
        dados = self.dao.obter_todas_assiduidades()
        header = ctk.CTkFrame(self.container_assiduidade, fg_color="#333")
        header.pack(fill="x", pady=2)
        cols = [("Colaborador", 400), ("Total Horas Extras", 300)]
        for t, w in cols: ctk.CTkLabel(header, text=t, width=w, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        for d in dados:
            f = ctk.CTkFrame(self.container_assiduidade)
            f.pack(fill="x", pady=1)
            ctk.CTkLabel(f, text=d['nome'], width=400, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(f, text=f"{d['horas_extra']}h", width=300).pack(side="left", padx=5)

    def salvar_horas(self):
        try:
            cid = self.colab_map[self.combo_colab.get()]
            hrs = float(self.ent_horas.get())
            if self.dao.registrar_horas(cid, hrs):
                messagebox.showinfo("Sucesso", "Horas registradas!")
                self.carregar_assiduidade()
                self.carregar_folha()
                if hasattr(self.parent, "atualizar_dados_dashboard"): self.parent.atualizar_dados_dashboard()
        except: messagebox.showerror("Erro", "Verifique os dados.")

    def inicializar_desempenho(self):
        ctk.CTkLabel(self.tab_desempenho, text="Avaliação de Desempenho", font=("Arial", 16, "bold")).pack(pady=10)
        form = ctk.CTkFrame(self.tab_desempenho)
        form.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(form, text="Colaborador:").grid(row=0, column=0, padx=10, pady=10)
        self.combo_colab_av = ctk.CTkComboBox(form, values=list(self.colab_map.keys()), width=250)
        self.combo_colab_av.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(form, text="Nota (0-10):").grid(row=0, column=2, padx=10, pady=10)
        self.sld_nota = ctk.CTkSlider(form, from_=0, to=10, width=150)
        self.sld_nota.grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkLabel(form, text="Satisfação (1-5):").grid(row=0, column=4, padx=10, pady=10)
        self.sld_sat = ctk.CTkSlider(form, from_=1, to=5, number_of_steps=4, width=100)
        self.sld_sat.grid(row=0, column=5, padx=10, pady=10)
        BotaoPersonalizado(form, "Avaliar", self.salvar_avaliacao).grid(row=0, column=6, padx=10, pady=10)

        self.container_desempenho = ctk.CTkScrollableFrame(self.tab_desempenho)
        self.container_desempenho.pack(fill="both", expand=True, padx=20, pady=10)
        self.carregar_desempenho()

    def carregar_desempenho(self):
        for widget in self.container_desempenho.winfo_children(): widget.destroy()
        dados = self.dao.obter_todas_avaliacoes()
        header = ctk.CTkFrame(self.container_desempenho, fg_color="#333")
        header.pack(fill="x", pady=2)
        cols = [("Colaborador", 400), ("Nota Desempenho", 150), ("Satisfação", 150)]
        for t, w in cols: ctk.CTkLabel(header, text=t, width=w, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        for d in dados:
            f = ctk.CTkFrame(self.container_desempenho)
            f.pack(fill="x", pady=1)
            ctk.CTkLabel(f, text=d['nome'], width=400, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(f, text=f"{d['nota_desempenho']}/10", width=150).pack(side="left", padx=5)
            ctk.CTkLabel(f, text=f"{d['indice_satisfacao']}/5", width=150).pack(side="left", padx=5)

    def salvar_avaliacao(self):
        try:
            cid = self.colab_map[self.combo_colab_av.get()]
            nota = self.sld_nota.get()
            sat = int(self.sld_sat.get())
            if self.dao.registrar_avaliacao(cid, nota, sat):
                messagebox.showinfo("Sucesso", "Avaliação registrada!")
                self.carregar_desempenho()
                if hasattr(self.parent, "atualizar_dados_dashboard"): self.parent.atualizar_dados_dashboard()
        except: messagebox.showerror("Erro", "Verifique os dados.")
