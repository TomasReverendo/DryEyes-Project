from click import progressbar
import customtkinter
import pyautogui

TIME_WITHOUT_WARNING = 5000 # Time in milliseconds without showing the warning window
TIME_WITH_WARNING = 20000 # Time in milliseconds to wait before eliminating the warning window if no movement is detected

class App(customtkinter.CTk):

    # main function
    def __init__(self):
        super().__init__()
        self.warning_active = False
        self.withdraw()  # Hides the main window 
        self.after(TIME_WITHOUT_WARNING, self.time_count)


    # manage if is necessary to create a warning window
    def time_count(self):
        
        # only create the warning window if is not already created
        if self.warning_active == False:
            print("Warning window will be open")
            self.open_warning()
        else:
            print("Warning window is already open!")
        
        
        # Schedule the next check
        self.after(TIME_WITHOUT_WARNING, self.time_count)


    # create the warning window
    def open_warning(self):
        self.warning_active = True
        current_pos = pyautogui.position()

        self.warning_window = customtkinter.CTkToplevel(self)
        self.warning_window.geometry("500x150")
        self.warning_window.title("Warning")
        self.warning_window.overrideredirect(True) # This line removes the top bar (X, Minimize, Maximize, and Title)
        self.warning_window.attributes("-topmost", True) # overlap other windows


        label = customtkinter.CTkLabel(self.warning_window, text="Time to take a break!\n Don´t move your mouse for 20s, go walk around, or do some eye exercises!", font=customtkinter.CTkFont(size=14))
        label.pack(pady=20)

        self.progressbar = customtkinter.CTkProgressBar(self.warning_window, orientation="horizontal")
        self.progressbar.pack(pady=20, padx=20, fill="x")
        self.progressbar.set(0) # Começa vazia

        count = 0
        self.after(1000, lambda: self.windowElimination(current_pos, count))


    # manage if is time to eliminate the warning window and creates the progress bar
    def windowElimination(self, initial_pos,count):

        self.progressbar.set(count/TIME_WITH_WARNING) # Update progress bar value

        if (initial_pos == pyautogui.position() and count >= TIME_WITH_WARNING ): # Mouse hasn't moved 
            print("No movement detected.Deleting Warning Window...")
            self.warning_window.destroy() # eliminates the warning window
            self.warning_active = False
        elif(initial_pos != pyautogui.position()):
            # Mouse moved! We 'reset' by doing nothing except updating the start_pos
            print("Movement detected. Resetting timer.")
            
            self.after(1000, lambda: self.windowElimination(pyautogui.position(), 0))
        else:
            count += 1000
            self.after(1000, lambda: self.windowElimination(initial_pos, count))



if __name__ == "__main__":
    app = App()
    app.mainloop()