import tkinter as tk
from tkinter import ttk




class SimpleApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simple Tkinter App")
        self.geometry("650x600")

        # Create a frame
        taskbar = ttk.Frame(self, width=300, height=300)
        taskbar.pack(anchor='w')# Left Aligned NavBar
        
        # Prevents frame from shrinking to fit content
        taskbar.pack_propagate(False)
        
        
        
         # Stack buttons using grid
        tk.Button(taskbar, text="Home").grid(row=0, column=0, sticky="ew")
        tk.Button(taskbar, text="Tasks").grid(row=1, column=0, sticky="ew")
        tk.Button(taskbar, text="Timers").grid(row=2, column=0, sticky="ew")
        tk.Button(taskbar, text="Notes").grid(row=3, column=0, sticky="ew")
        
        # Make buttons stretch horizontally
        taskbar.columnconfigure(0, weight=1)
        
        
if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()

