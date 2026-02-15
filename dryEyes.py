import customtkinter
import pyautogui
from PIL import Image
import pystray
from pystray import MenuItem as item
import threading

# Constants
TIME_WITHOUT_WARNING = 1000 * 60 * 20 
TIME_WITH_WARNING = 1000 * 10 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.warning_active = False
        self.withdraw()  # Keeps the main "anchor" window hidden
        
        # Start the tray icon in a background thread
        self.setup_tray()
        
        # Start the break timer
        self.after(TIME_WITHOUT_WARNING, self.time_count)

    def setup_tray(self):
        # Create a simple icon (Replace 'icon.png' with your file path)
        # For now, we'll create a small colored square if no image is found
        try:
            image = Image.open("icon.png")
        except:
            image = Image.new('RGB', (64, 64), color=(73, 109, 137))

        menu = (
            item('Status: Active', lambda: None, enabled=False),
            item('Exit', self.quit_app)
        )
        
        self.tray_icon = pystray.Icon("BreakTimer", image, "Break Timer", menu)
        
        # Run tray in a separate thread so it doesn't block Tkinter's mainloop
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def quit_app(self):
        
        self.tray_icon.stop()
        self.destroy()

    def time_count(self):
        if not self.warning_active:
            print("Warning window will be open")
            self.open_warning()
        
        self.after(TIME_WITHOUT_WARNING, self.time_count)

    def open_warning(self):
        self.warning_active = True
        current_pos = pyautogui.position()

        self.warning_window = customtkinter.CTkToplevel(self)
        self.warning_window.geometry("500x150")
        self.warning_window.title("Warning")
        self.warning_window.overrideredirect(True) 
        self.warning_window.attributes("-topmost", True)

        label = customtkinter.CTkLabel(
            self.warning_window, 
            text="Time to take a break!\nDon't move your mouse for 10s!", 
            font=customtkinter.CTkFont(size=14)
        )
        label.pack(pady=20)

        self.progressbar = customtkinter.CTkProgressBar(self.warning_window, orientation="horizontal")
        self.progressbar.pack(pady=20, padx=20, fill="x")
        self.progressbar.set(0)

        count = 0
        self.after(1000, lambda: self.window_elimination(current_pos, count))

    def window_elimination(self, initial_pos, count):
        # Update progress bar
        self.progressbar.set(count / TIME_WITH_WARNING)

        if initial_pos == pyautogui.position() and count >= TIME_WITH_WARNING:
            print("Break complete. Closing...")
            self.warning_window.destroy()
            self.warning_active = False
        elif initial_pos != pyautogui.position():
            print("Movement detected. Resetting timer.")
            self.after(1000, lambda: self.window_elimination(pyautogui.position(), 0))
        else:
            count += 1000
            self.after(1000, lambda: self.window_elimination(initial_pos, count))
   

if __name__ == "__main__":
    app = App()
    app.mainloop()