import os
import json

class ToDoListManager:
    def __init__(self, file_name="todo_list.json"):
        self.file_name = file_name
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(self.file_name, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, task):
        self.tasks.append({"task": task, "completed": False})
        self.save_tasks()
        print(f"Task added: {task}")

    def list_tasks(self):
        print("\nTo-Do List:")
        for index, task in enumerate(self.tasks, start=1):
            status = "[x]" if task["completed"] else "[ ]"
            print(f"{index}. {status} {task['task']}")

    def complete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]["completed"] = True
            self.save_tasks()
            print(f"Task {task_number} marked as completed.")
        else:
            print("Invalid task number.")

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            removed_task = self.tasks.pop(task_number - 1)
            self.save_tasks()
            print(f"Task removed: {removed_task['task']}")
        else:
            print("Invalid task number.")

    def clear_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.save_tasks()
        print("Completed tasks cleared.")

if __name__ == "__main__":
    manager = ToDoListManager()

    while True:
        print("\nOptions:")
        print("1. Add a task")
        print("2. List tasks")
        print("3. Complete a task")
        print("4. Delete a task")
        print("5. Clear completed tasks")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter a new task: ")
            manager.add_task(task)
        elif choice == "2":
            manager.list_tasks()
        elif choice == "3":
            try:
                task_number = int(input("Enter task number to complete: "))
                manager.complete_task(task_number)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "4":
            try:
                task_number = int(input("Enter task number to delete: "))
                manager.delete_task(task_number)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "5":
            manager.clear_completed_tasks()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
