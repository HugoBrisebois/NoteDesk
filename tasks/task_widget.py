import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from .tasks import Task, TaskManager
from datetime import datetime

class TaskWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.task_manager = TaskManager()
        self.tasks = []
        self.setup_ui()

    def setup_ui(self):
    # Create a horizontal paned window for task and notes side by side
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill="both", expand=True, padx=5, pady=5)
    
    # ---------------- Left side (Tasks) ----------------
        task_side = ttk.Frame(self.paned)
        self.paned.add(task_side, weight=1)
    
    # Tasks List
        list_frame = ttk.LabelFrame(task_side, text="Tasks")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # Create Treeview
        self.tree = ttk.Treeview(list_frame, columns=("Title", "Due Date", "Priority", "Status"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True)

    # Delete Task button under tree
        ttk.Button(list_frame, text="Delete Task", command=self.delete_task).pack(pady=5)

    # Add Task Form at the bottom
        form_frame = ttk.LabelFrame(task_side, text="Add New Task")
        form_frame.pack(fill="x", padx=5, pady=5)

    # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

    # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

    # Due Date
        ttk.Label(form_frame, text="Due Date:").grid(row=2, column=0, padx=5, pady=5)
        self.due_date = DateEntry(form_frame)
        self.due_date.grid(row=2, column=1, padx=5, pady=5)

    # Priority
        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, padx=5, pady=5)
        self.priority = ttk.Combobox(form_frame, values=["Low", "Medium", "High"])
        self.priority.set("Medium")
        self.priority.grid(row=3, column=1, padx=5, pady=5)

    # Add Task button only
        ttk.Button(form_frame, text="Add Task", command=self.add_task).grid(row=4, column=0, columnspan=2, pady=10)

    # ---------------- Right side (Notes) ----------------
        notes_frame = ttk.Frame(self.paned)
        self.paned.add(notes_frame, weight=1)
    
        notes_label_frame = ttk.LabelFrame(notes_frame, text="Notes")
        notes_label_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
        from notes.notes_widget import NotesWidget
        self.notes_widget = NotesWidget(notes_label_frame)
        self.notes_widget.pack(fill="both", expand=True, padx=5, pady=5)

    # ---------------- Final setup ----------------
        self.refresh_task_list()

    # Add right-click menu for tasks
        self.task_menu = tk.Menu(self, tearoff=0)
        self.task_menu.add_command(label="Mark Complete", command=self.mark_complete)
        self.task_menu.add_command(label="Mark Pending", command=self.mark_pending)
        self.task_menu.add_separator()
        self.task_menu.add_command(label="Delete", command=self.delete_task)

    # Bind right-click to tree
        self.tree.bind("<Button-3>", self.show_task_menu)

    # Add double-click to edit
        self.tree.bind("<Double-1>", self.edit_task)

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def add_task(self):
        # Validate inputs
        if not self.title_entry.get().strip():
            tk.messagebox.showerror("Error", "Title is required")
            return
        
        task = Task(
            title=self.title_entry.get().strip(),
            description=self.desc_entry.get().strip(),
            due_date=self.due_date.get_date(),
            priority=self.priority.get(),
            status="Pending"  # Default status
        )
        self.task_manager.add_task(task)
        self.refresh_task_list()
        self.clear_form()
        
        # Show confirmation
        tk.messagebox.showinfo("Success", "Task added successfully!")

    def refresh_task_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all tasks and sort them
        tasks = self.task_manager.get_all_tasks()
        
        # Define priority order
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        
        # Sort tasks by priority and status
        sorted_tasks = sorted(tasks, 
            key=lambda x: (
                0 if x.status == "Pending" else 1,  # Pending tasks first
                priority_order.get(x.priority, 4),   # Then by priority
                x.due_date if x.due_date else datetime.max  # Then by due date
            )
        )
        
        # Insert sorted tasks into the tree
        for task in sorted_tasks:
            self.tree.insert("", "end", values=(
                task.title,
                task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
                task.priority,
                task.status
            ))

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.priority.set("Medium")

    def delete_task(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            return  # Nothing selected
        
        # Get the index of selected item
        index = self.tree.index(selected_item)
        
        # Delete from task manager
        self.task_manager.delete_task(index)
        
        # Refresh the display
        self.refresh_task_list()

    def apply_filter(self, event=None):
        filter_type = self.filter_var.get()
        for task in self.tasks:
            if filter_type == "all":
                task.frame.pack(fill='x', pady=2)
            elif filter_type == "completed" and task.completed:
                task.frame.pack(fill='x', pady=2)
            elif filter_type == "pending" and not task.completed:
                task.frame.pack(fill='x', pady=2)
            else:
                task.frame.pack_forget()

    def apply_sort(self, event=None):
        sort_by = self.sort_var.get()
        if sort_by == "date":
            self.tasks.sort(key=lambda x: x.creation_date)
        elif sort_by == "priority":
            self.tasks.sort(key=lambda x: x.priority, reverse=True)
        elif sort_by == "name":
            self.tasks.sort(key=lambda x: x.description.lower())
        
        # Repack all visible tasks in the new order
        for task in self.tasks:
            task.frame.pack_forget()
        self.apply_filter()

    def show_task_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.task_menu.post(event.x_root, event.y_root)

    def mark_complete(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            index = self.tree.index(item)
            self.task_manager.update_task_status(index, "Completed")
            self.refresh_task_list()

    def mark_pending(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            index = self.tree.index(item)
            self.task_manager.update_task_status(index, "Pending")
            self.refresh_task_list()

    def edit_task(self, event):
        item = self.tree.selection()[0]
        if item:
            # Get task data
            values = self.tree.item(item)['values']
            
            # Create edit window
            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Task")
            edit_window.geometry("300x250")
            
            # Add edit fields
            ttk.Label(edit_window, text="Title:").pack(pady=5)
            title_entry = ttk.Entry(edit_window)
            title_entry.insert(0, values[0])
            title_entry.pack(pady=5)
            
            ttk.Label(edit_window, text="Priority:").pack(pady=5)
            priority_combo = ttk.Combobox(edit_window, values=["Low", "Medium", "High"])
            priority_combo.set(values[2])
            priority_combo.pack(pady=5)
            
            def save_changes():
                index = self.tree.index(item)
                self.task_manager.update_task(
                    index,
                    title=title_entry.get(),
                    priority=priority_combo.get()
                )
                self.refresh_task_list()
                edit_window.destroy()
                
            ttk.Button(edit_window, text="Save", command=save_changes).pack(pady=20)

