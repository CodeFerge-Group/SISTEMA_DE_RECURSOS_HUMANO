import customtkinter as ctk
from tkinter import messagebox
from dao.colaborador_dao import ColaboradorDAO
from core.excecoes import ErroConexaoBanco

class JanelaLogin(ctk.CTk):

    def __init__(self, callback_sucesso):
        super().__init__()
        self.callback_sucesso = callback_sucesso
        self.title("Sistema de Gestão RH - Login")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a1a")

        self.inicializar_interface()

    def inicializar_interface(self):
        # Cabeçalho Visual
        self.frame_logo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_logo.pack(pady=40)

        ctk.CTkLabel(self.frame_logo, text="SISTEMA RH", font=("Arial", 28, "bold"), text_color="#3498db").pack()
        ctk.CTkLabel(self.frame_logo, text="GESTÃO E IA", font=("Arial", 10, "bold"), text_color="#aaa").pack()

        # Campos de Input atualizados
        self.ent_email = ctk.CTkEntry(self, placeholder_text="Usuário/E-mail", width=320, height=45, 
                                      corner_radius=8, border_color="#333")
        self.ent_email.pack(pady=10)
        self.ent_email.insert(0, "Admin") # Novo padrão solicitado

        self.ent_senha = ctk.CTkEntry(self, placeholder_text="Palavra-passe", show="*", width=320, height=45, 
                                      corner_radius=8, border_color="#333")
        self.ent_senha.pack(pady=10)
        self.ent_senha.insert(0, "1234") # Novo padrão solicitado

        # Ação
        self.btn_entrar = ctk.CTkButton(self, text="ENTRAR NO SISTEMA", command=self.executar_login, 
                                        width=320, height=50, font=("Arial", 14, "bold"),
                                        fg_color="#3498db", hover_color="#2980b9")
        self.btn_entrar.pack(pady=40)

    def executar_login(self):
        email = self.ent_email.get()
        senha = self.ent_senha.get()

        try:
            dao = ColaboradorDAO()
            colaborador = dao.autenticar(email, senha)

            if colaborador:
                self.withdraw()
                self.callback_sucesso(colaborador)
                self.destroy()
            else:
                messagebox.showwarning("Acesso Negado", "E-mail ou palavra-passe incorretos.")
        
        except ErroConexaoBanco as e:
            messagebox.showerror("Erro de Infraestrutura", f"Erro ao conectar ao banco sistema_RH.\n{e}")
        except Exception as e:
            messagebox.showerror("Erro Fatal", f"Erro: {e}")
