import customtkinter
import pyautogui

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.warning_active = False
        self.withdraw()  # Hides the main window
        self.start_pos = pyautogui.position() 
        self.time_count()

    # AJUSTE: A função agora recebe a janela que deve ser fechada
    #def button_callbck(self, window_to_close):
        #print("Botão clicado - Reset do estado")
        #self.warning_active = False 
        #window_to_close.destroy() # DESTROI APENAS A TOPLEVEL, NÃO O APP

    def time_count(self):
        # Get the position right now
        current_pos = pyautogui.position()
        
        # Check if the mouse moved since the LAST time this function ran
        if current_pos == self.start_pos:
            # Mouse hasn't moved for the entire 'after' duration
            print("No movement detected. Opening warning...")
            self.open_warning()
        else:
            # Mouse moved! We 'reset' by doing nothing except updating the start_pos
            print("Movement detected. Resetting timer.")
        
        # Update the reference point for the NEXT 5 seconds
        self.start_pos = current_pos
        
        # Schedule the next check
        self.after(10000, self.time_count)



    def open_warning(self):
        self.warning_active = True

        warning_window = customtkinter.CTkToplevel(self)
        warning_window.geometry("300x200")
        warning_window.title("Warning")

        warning_window.overrideredirect(True) # This line removes the top bar (X, Minimize, Maximize, and Title)

        warning_window.attributes("-topmost", True) # overlap other windows

        label = customtkinter.CTkLabel(warning_window, text="Time to take a break!")
        label.pack(pady=20)

        # AJUSTE: Usamos lambda para passar a 'warning_window' como argumento
        #button = customtkinter.CTkButton(warning_window, text="Ok, já vi!", command=lambda: self.button_callbck(warning_window))
        #button.pack(padx=20, pady=10)
        
        # BOAS PRÁTICAS: Se o utilizador fechar no "X", reseta o estado também
        #warning_window.protocol("WM_DELETE_WINDOW", lambda: self.button_callbck(warning_window))

    #def delete_exit_button(self):
        #self.destroy()

    def progressBar():
        progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")



app = App()
#app.protocol("WM_DELETE_WINDOW", app.delete_exit_button)
app.mainloop()