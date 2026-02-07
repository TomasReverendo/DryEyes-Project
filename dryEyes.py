import customtkinter
import pyautogui

class App(customtkinter.CTk):

    # main function
    def __init__(self):
        super().__init__()
        self.warning_active = False
        self.withdraw()  # Hides the main window 
        self.after(30000, self.time_count)


    # manage if is necessary to create a warning window
    def time_count(self):
        
        # only create the warning window if is not already created
        if self.open_warning == False:
            print("Warning window will be open")
            self.open_warning()
        else:
            print("Warning window is already open!")
        
        
        # Schedule the next check
        self.after(30000, self.time_count)


    # create the warning window
    def open_warning(self):
        self.warning_active = True

        current_pos = pyautogui.position()

        warning_window = customtkinter.CTkToplevel(self)
        warning_window.geometry("300x200")
        warning_window.title("Warning")

        warning_window.overrideredirect(True) # This line removes the top bar (X, Minimize, Maximize, and Title)

        warning_window.attributes("-topmost", True) # overlap other windows

        label = customtkinter.CTkLabel(warning_window, text="Time to take a break!")
        label.pack(pady=20)

        self.windowElimination()


    # manage if is time to eliminate the warning window
    def windowElimination(self):

        while(1):
            if current_pos == self.start_pos: # Mouse hasn't moved for the entire 'after' duration
                print("No movement detected. Opening warning...")
                self.open_warning()
                break
            else:
                # Mouse moved! We 'reset' by doing nothing except updating the start_pos
                print("Movement detected. Resetting timer.")
        
            # Update the reference point for the NEXT 5 seconds
            self.start_pos = current_pos
            self.after(10000, self.time_count)

    # create and animate the progression bar
    def progressBar():
        progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")





app = App()
app.mainloop()