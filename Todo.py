import tkinter as tk
from tkinter import messagebox, ttk
from bson.objectid import ObjectId
from pymongo import MongoClient


#CONNECT TO MONGODB
try:
    client = MongoClient("MONGODB_connection_URI")
    db = client["db_Todo"]
    tasks_collection = db["tasks"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise


#TASK OPERATIONS
def add_task(title, description):
    """Add a new task to the database."""
    try:
        tasks_collection.insert_one({"title": title, "description": description, "status": "Pending"})
        messagebox.showinfo("Success", "Task added successfully.")
        refresh_tasks()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add task: {e}")

def view_tasks():
    """Retrieve all tasks from the database."""
    try:
        return list(tasks_collection.find())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve tasks: {e}")
        return []

def update_task_status(task_id, status):
    """Update the status of a task."""
    try:
        result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"status": status}})
        if result.modified_count > 0:
            messagebox.showinfo("Success", "Task updated successfully.")
        else:
            messagebox.showwarning("Not Found", "Task not found.")
        refresh_tasks()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update task: {e}")

def delete_task(task_id):
    """Delete a task from the database."""
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Task deleted successfully.")
        else:
            messagebox.showwarning("Not Found", "Task not found.")
        refresh_tasks()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete task: {e}")


#GUI FUNCTIONS
def add_task_gui():
    """Handle adding a task via the GUI."""
    title, description = title_entry.get(), description_entry.get()
    if not title or not description:
        messagebox.showwarning("Input Error", "Please enter both title and description.")
        return
    add_task(title, description)
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

def refresh_tasks():
    """Refresh the displayed task list."""
    for item in tree.get_children():
        tree.delete(item)
    for task in view_tasks():
        tree.insert("", tk.END, iid=str(task["_id"]), values=(task["title"], task["description"], task["status"]))

def update_status_gui():
    """Handle updating task status via the GUI."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task to update.")
        return
    update_task_status(selected_item[0], status_combobox.get())

def delete_task_gui():
    """Handle deleting a task via the GUI."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")
        return
    delete_task(selected_item[0])

#SETING UP GUI
app = tk.Tk()
app.title("To-Do List Application")
app.geometry("600x400")

frame = tk.Frame(app)
frame.pack(pady=10)

tk.Label(frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(frame, width=40)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
description_entry = tk.Entry(frame, width=40)
description_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame, text="Add Task", command=add_task_gui).grid(row=2, column=0, columnspan=2, pady=10)

#TASK LIST
columns = ("Title", "Description", "Status")
tree = ttk.Treeview(app, columns=columns, show="headings", height=10)
tree.heading("Title", text="Title")
tree.heading("Description", text="Description")
tree.heading("Status", text="Status")
tree.column("Title", width=150)
tree.column("Description", width=250)
tree.column("Status", width=100)
tree.pack(pady=10)

#UPDATE & DELETE CONTROLS
update_frame = tk.Frame(app)
update_frame.pack(pady=10)

tk.Label(update_frame, text="Update Status:").grid(row=0, column=0, padx=5, pady=5)
status_combobox = ttk.Combobox(update_frame, values=["Pending", "Completed"])
status_combobox.grid(row=0, column=1, padx=5, pady=5)

tk.Button(update_frame, text="Update Status", command=update_status_gui).grid(row=0, column=2, padx=5, pady=5)
tk.Button(update_frame, text="Delete Task", command=delete_task_gui).grid(row=0, column=3, padx=5, pady=5)

#INITIALIZING TASK LIST
refresh_tasks()

#RUNNING APPLICATION
app.mainloop()
