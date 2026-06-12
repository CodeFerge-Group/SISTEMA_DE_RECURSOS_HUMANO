import customtkinter as ctk
from gui.componentes import BotaoPersonalizado
from dao.colaborador_dao import ColaboradorDAO
from models.colaborador import Colaborador
from core.excecoes import ErroPersistencia
from tkinter import messagebox

class JanelaCadastroColaborador(ctk.CTkToplevel):

    def __init__(self, parent, callback_sucesso):
        super().__init__(parent)
        self.title("Novo Registro de Funcionário")
        self.geometry("520x750")
        self.dao = ColaboradorDAO()
        self.callback_sucesso = callback_sucesso
        
        # Manter foco
        self.attributes("-topmost", True)
        self.grab_set()
        self.configure(fg_color="#1e1e1e")
        
        # 1. Título Fixo no Topo
        ctk.CTkLabel(self, text="CADASTRO DE FUNCIONÁRIO", 
                     font=("Arial", 22, "bold"), text_color="#3498db").pack(pady=20)

        # 2. Frame Central com Scroll para os campos
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 3. Frame Fixo no Rodapé para os Botões (Sempre visível)
        self.frame_botoes = ctk.CTkFrame(self, fg_color="#1a1a1a", height=120, corner_radius=0)
        self.frame_botoes.pack(side="bottom", fill="x")
        
        self.inicializar_campos()
        self.inicializar_botoes()

    def inicializar_campos(self):
        self.campos = {}
        config_campos = [
            ("Nome Completo", "ex: Maria Silva"),
            ("Email Corporativo", "ex: maria@rh.ao"),
            ("Senha Temporária", ""),
            ("Cargo", "ex: Analista Pleno"),
            ("Salário Mensal (Kz)", "ex: 450000"),
            ("Data Admissão (AAAA-MM-DD)", "2024-05-20")
        ]

        for label, placeholder in config_campos:
            frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
            frame.pack(fill="x", padx=30, pady=8)
            
            ctk.CTkLabel(frame, text=label, font=("Arial", 11, "bold")).pack(anchor="w")
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder, height=38, border_color="#333")
            if "Senha" in label: entry.configure(show="*")
            entry.pack(fill="x", pady=2)
            self.campos[label] = entry

        # Seleção de Departamento
        frame_dep = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        frame_dep.pack(fill="x", padx=30, pady=8)
        ctk.CTkLabel(frame_dep, text="Departamento", font=("Arial", 11, "bold")).pack(anchor="w")
        
        self.departamentos = self.dao.listar_departamentos()
        nomes_deps = [d['nome'] for d in self.departamentos]
        self.combo_dep = ctk.CTkComboBox(frame_dep, values=nomes_deps, height=38)
        self.combo_dep.pack(fill="x", pady=2)

    def inicializar_botoes(self):
        # Botão de Validação (Sempre Visível)
        BotaoPersonalizado(self.frame_botoes, "🔍 VALIDAR DADOS", self.verificar_dados, 
                           fg_color="#2c3e50", hover_color="#34495e").pack(pady=(15, 5), padx=40, fill="x")

        # Botão de Confirmação Final (Sempre Visível)
        BotaoPersonalizado(self.frame_botoes, "✅ CONFIRMAR REGISTRO", self.executar_cadastro).pack(pady=(0, 15), padx=40, fill="x")

    def criar_objeto_colaborador(self):
        """Instancia o objeto a partir dos campos."""
        try:
            dep_nome = self.combo_dep.get()
            dep_id = next(d['id'] for d in self.departamentos if d['nome'] == dep_nome)
            
            return Colaborador(
                nome=self.campos["Nome Completo"].get(),
                email=self.campos["Email Corporativo"].get(),
                cargo=self.campos["Cargo"].get(),
                salario=self.campos["Salário Mensal (Kz)"].get() or 0,
                data_admissao=self.campos["Data Admissão (AAAA-MM-DD)"].get(),
                departamento_id=dep_id
            )
        except StopIteration:
            raise ValueError("Departamento não selecionado")

    def verificar_dados(self):
        """Validação lógica (POO)."""
        try:
            colab = self.criar_objeto_colaborador()
            if colab.validar():
                messagebox.showinfo("Validação", "Os dados estão em conformidade com as regras de negócio!")
            else:
                messagebox.showwarning("Validação", "Dados inválidos. Verifique os campos obrigatórios.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na validação: {e}")

    def executar_cadastro(self):
        """Persistência no SGBD."""
        try:
            novo_colab = self.criar_objeto_colaborador()
            if not novo_colab.validar():
                messagebox.showwarning("Validação", "Os dados não passaram na validação lógica.")
                return
            
            senha = self.campos["Senha Temporária"].get()
            if not senha:
                messagebox.showwarning("Segurança", "A senha temporária é obrigatória.")
                return

            if self.dao.cadastrar(novo_colab, senha):
                messagebox.showinfo("Sucesso", "Colaborador cadastrado com sucesso!")
                self.callback_sucesso()
                self.destroy()
        except ErroPersistencia as e:
            messagebox.showerror("Erro de Banco", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro crítico: {e}")
