import tkinter as tk
from tkinter import ttk

class SimpleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sized Frame")
        self.geometry("600x600")

        # Create a frame with specific size
        taskbar = ttk.Frame(self, width=200, height=300)
        taskbar.pack()
        
        # Prevent the frame from shrinking to fit its contents
        taskbar.pack_propagate(False)
        
        tk.Button(taskbar, text="Button 1").pack()
        tk.Button(taskbar, text="Button 2").pack()

if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()