import customtkinter as ctk

class BotaoPersonalizado(ctk.CTkButton):

    def __init__(self, master, texto, comando, **kwargs):
        # Definimos valores padrão
        config = {
            "text": texto,
            "command": comando,
            "corner_radius": 8,
            "font": ("Arial", 13, "bold"),
            "fg_color": "#1f77b4",
            "hover_color": "#145a8a",
            "height": 35
        }
        # Atualizamos os padrões com o que vier no kwargs
        config.update(kwargs)
        
        super().__init__(master, **config)


class CardMetrica(ctk.CTkFrame):
    """Card visual para exibição de indicadores (KPIs)."""

    def __init__(self, master, titulo, valor, cor_valor="#2ecc71", **kwargs):
        super().__init__(master, fg_color="#2b2b2b", corner_radius=10, **kwargs)

        lbl_titulo = ctk.CTkLabel(self, text=titulo, font=("Arial", 12), text_color="#aaaaaa")
        lbl_titulo.pack(pady=(10, 2), padx=15)

        self.lbl_valor = ctk.CTkLabel(self, text=str(valor), font=("Arial", 22, "bold"), text_color=cor_valor)
        self.lbl_valor.pack(pady=(0, 10), padx=15)

    def atualizar_valor(self, novo_valor):
        self.lbl_valor.configure(text=str(novo_valor))
