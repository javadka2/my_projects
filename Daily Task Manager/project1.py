import json
import os

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            try:
                tasks = json.load(f)
                if not isinstance(tasks, list):
                    print("file's format isn't correct.")
                    return []
                return tasks
            except json.JSONDecodeError:
                print("failed to read the file. file is empty or corrupted")
                return []
    else:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)
    print("tasks saved correctly")

def add_task(tasks):
    task_description = input("pls add new task description: ")
    if task_description:
        tasks.append({"id": len(tasks) + 1, "description": task_description, "done": False})
        print(f"task: {task_description} added")
    else:
        print("task description can't be empty")

def delete_task(tasks):
    try:
        task_id_to_delete = int(input("pls enter ID of the task that u wanna delete: "))
        initial_length = len(tasks)
        tasks1 = []
        for task in tasks:
            if task["id"] != task_id_to_delete:
                tasks1.append(task)
        tasks[:] = tasks1
        if len(tasks) < initial_length:
            print(f"task with ID: {task_id_to_delete} has deleted")
            for i, task in enumerate(tasks):
                task["id"] = i + 1
        else:
            print(f"task with ID: {task_id_to_delete} didn't find")
    except ValueError:
        print("Uncorrect type. pls enter numbers")
    except Exception as e:
        print(f"Erorr while deleting the task: {e}")

def show_tasks(tasks):
    if not tasks:
        print("No tasks to show.")
        return
    else:
        print("\n--- Task's list ---")
    for task in tasks:
        status = "Done" if task.get("done", False) else "Not done"
        print(f"ID: {task['id']} | Description: {task['description']} | Status: {status}")
    print("------------------\n")

def display_menu():
    print("\n===== Managing daily tasks =====")
    print("1. Add a task")
    print("2. Delete a task")
    print("3. Show all the tasks")
    print("4. Quit")
    print("================================")

def main():
    tasks = load_tasks()

    while True:
        display_menu()
        choice = input("Pls enter a number (1-4): ")

        if choice == '1':
            add_task(tasks)
            save_tasks(tasks) 
        elif choice == '2':
            if not tasks:
                print("No tasks to show or delete.")
            else:
                show_tasks(tasks)
                delete_task(tasks)
                save_tasks(tasks)
 
        elif choice == '3':
            show_tasks(tasks)
        elif choice == '4':
            print("Bye")
            break
        else:
            print("Invaild number. Pls enter a correct number")

if __name__ == "__main__":
    main()