import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.warning_active = False
        self.withdraw()  # Esconde a janela principal
        self.time_count()

    # AJUSTE: A função agora recebe a janela que deve ser fechada
    def button_callbck(self, window_to_close):
        print("Botão clicado - Reset do estado")
        self.warning_active = False 
        window_to_close.destroy() # DESTROI APENAS A TOPLEVEL, NÃO O APP

    def time_count(self):
        self.after(5000, self.time_count) 
        if not self.warning_active:
            print("Abrindo novo aviso...")
            self.open_warning()
        else:
            print("Aviso ignorado: utilizador ainda não fechou o anterior.")

    def open_warning(self):
        self.warning_active = True
        warning_window = customtkinter.CTkToplevel(self)
        warning_window.geometry("300x200")
        warning_window.title("Warning")
        warning_window.attributes("-topmost", True)

        label = customtkinter.CTkLabel(warning_window, text="Time to take a break!")
        label.pack(pady=20)

        # AJUSTE: Usamos lambda para passar a 'warning_window' como argumento
        button = customtkinter.CTkButton(
            warning_window, 
            text="Ok, já vi!", 
            command=lambda: self.button_callbck(warning_window)
        )
        button.pack(padx=20, pady=10)
        
        # BOAS PRÁTICAS: Se o utilizador fechar no "X", reseta o estado também
        warning_window.protocol("WM_DELETE_WINDOW", lambda: self.button_callbck(warning_window))

app = App()
app.mainloop()