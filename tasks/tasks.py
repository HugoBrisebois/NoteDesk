import datetime as time
import json

class Task:
    def __init__(self, title, description="", due_date=None, priority="Medium", status="Pending"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status


    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.tasks.json"
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task):
        self.tasks.remove(task)
        self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def update_task_status(self, index, status):
        if 0 <= index < len(self.tasks):
            self.tasks[index].status = status
            self.save_tasks()

    def update_task(self, index, **kwargs):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.save_tasks()

    def get_all_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = []
                for task_data in tasks_data:
                    task = Task(
                        title=task_data["title"],
                        description=task_data["description"],
                        due_date=time.datetime.fromisoformat(task_data["due_date"]) if task_data["due_date"] else None,
                        priority=task_data["priority"],
                        status=task_data["status"]
                    )
                    self.tasks.append(task)
        except FileNotFoundError:
            self.tasks = []





