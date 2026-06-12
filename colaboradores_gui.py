import customtkinter as ctk
from gui.componentes import BotaoPersonalizado
from dao.colaborador_dao import ColaboradorDAO
from gui.cadastro_colaborador_gui import JanelaCadastroColaborador
from tkinter import messagebox


class JanelaColaboradores(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Colaboradores")
        self.geometry("900x600")
        self.dao = ColaboradorDAO()
        self.parent = parent
        
        self.inicializar_interface()
        self.carregar_dados()

    def inicializar_interface(self):
        # Top Bar
        self.top_bar = ctk.CTkFrame(self, height=60)
        self.top_bar.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.top_bar, text="Lista de Funcionários Ativos", font=("Arial", 18, "bold")).pack(side="left", padx=15)
        
        BotaoPersonalizado(self.top_bar, "+ Adicionar Funcionário", self.abrir_formulario_cadastro).pack(side="right", padx=15)

        # Container da Tabela
        self.container_tabela = ctk.CTkScrollableFrame(self)
        self.container_tabela.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho da Tabela
        self.header = ctk.CTkFrame(self.container_tabela, fg_color="#1a1a1a")
        self.header.pack(fill="x", pady=2)
        
        colunas = [("Nome", 200), ("Cargo", 150), ("Departamento", 150), ("Salário", 120), ("Ações", 100)]
        for texto, largura in colunas:
            ctk.CTkLabel(self.header, text=texto, width=largura, font=("Arial", 12, "bold")).pack(side="left", padx=5)

    def carregar_dados(self):
        for widget in self.container_tabela.winfo_children():
            if widget != self.header:
                widget.destroy()
        
        # Método correto: listar_todos_metricas
        colaboradores = self.dao.listar_todos_metricas()
        for colab in colaboradores:
            linha = ctk.CTkFrame(self.container_tabela)
            linha.pack(fill="x", pady=1)
            
            ctk.CTkLabel(linha, text=colab['nome'], width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(linha, text=colab['cargo'], width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(linha, text=colab['departamento'] or "N/D", width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(linha, text=f"{colab['salario']:,.2f} Kz", width=120).pack(side="left", padx=5)
            
            btn_excluir = ctk.CTkButton(linha, text="Remover", fg_color="#e74c3c", hover_color="#c0392b", 
                                        width=80, height=25, command=lambda c=colab: self.excluir_colab(c))
            btn_excluir.pack(side="left", padx=5)

    def abrir_formulario_cadastro(self):
        JanelaCadastroColaborador(self, self.sucesso_no_cadastro)

    def sucesso_no_cadastro(self):
        self.carregar_dados()
        if hasattr(self.parent, "atualizar_dados_dashboard"):
            self.parent.atualizar_dados_dashboard()

    def excluir_colab(self, colab):
        if messagebox.askyesno("Confirmar", f"Inativar funcionário {colab['nome']}?"):
            if self.dao.inativar(colab['id']):
                messagebox.showinfo("Sucesso", "Funcionário removido com sucesso.")
                self.sucesso_no_cadastro()
