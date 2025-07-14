import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from reportlab.pdfgen import canvas
import database

# ---------- Initialize ---------- #
database.connect_db()
app = tb.Window(themename="superhero")
app.title("Cerebra - Smart Notes & Tasks")
app.geometry("850x600")

notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill='both')

# ---------- Notes Tab ---------- #
notes_tab = ttk.Frame(notebook)
notebook.add(notes_tab, value="Notes")

note_title = ttk.Entry(notes_tab, width=40)
note_title.pack(pady=5)
note_title.insert(0, value= "Title")

note_content = tk.Text(notes_tab, width=60, height=5)
note_content.pack(pady=5)

note_tag = ttk.Entry(notes_tab, width=25)
note_tag.pack()
note_tag.insert(0, "#tag")

note_search = ttk.Entry(notes_tab, width=30)
note_search.pack(pady=5)
note_search.insert(0, "Search notes")

note_listbox = tk.Listbox(notes_tab, width=80, height=12)
note_listbox.pack(pady=5)

def refresh_notes():
    notes = database.get_notes(note_search.get())
    note_listbox.delete(0, tk.END)
    for note in notes:
        tag = f" [{note[3]}]" if note[3] else ""
        note_listbox.insert(tk.END, f"[{note[0]}] {note[1]}{tag} - {note[4]}")

def add_note():
    database.add_note(note_title.get(), note_content.get("1.0", tk.END).strip(), note_tag.get())
    note_title.delete(0, tk.END)
    note_content.delete("1.0", tk.END)
    note_tag.delete(0, tk.END)
    refresh_notes()

def delete_note():
    try:
        index = note_listbox.curselection()[0]
        note_id = int(note_listbox.get(index).split("]")[0][1:])
        database.delete_note(note_id)
        refresh_notes()
    except:
        messagebox.showinfo("Select Note", "Please select a note to delete")

def export_note():
    try:
        index = note_listbox.curselection()[0]
        title = note_listbox.get(index)
        content = note_content.get("1.0", tk.END).strip()
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", '*.pdf')])
        if file:
            pdf = canvas.Canvas(file)
            pdf.setFont("Helvetica", 14)
            pdf.drawString(50, 800, title)
            pdf.setFont("Helvetica", 10)
            y = 780
            for line in content.splitlines():
                pdf.drawString(50, y, line)
                y -= 15
            pdf.save()
            messagebox.showinfo("Exported", f"Note exported to {file}")
    except:
        messagebox.showwarning("Export Failed", "Select a note and write content to export.")

note_button_frame = ttk.Frame(notes_tab)
note_button_frame.pack()

add_btn = ttk.Button(note_button_frame, text="Add", command=add_note)
delete_btn = ttk.Button(note_button_frame, text="Delete", command=delete_note)
export_btn = ttk.Button(note_button_frame, text="Export PDF", command=export_note)
search_btn = ttk.Button(note_button_frame, text="Search", command=refresh_notes)

add_btn.grid(row=0, column=0, padx=5)
delete_btn.grid(row=0, column=1, padx=5)
export_btn.grid(row=0, column=2, padx=5)
search_btn.grid(row=0, column=3, padx=5)

# ---------- Tasks Tab ---------- #
tasks_tab = ttk.Frame(notebook)
notebook.add(tasks_tab, text="Tasks")

task_entry = ttk.Entry(tasks_tab, width=40)
task_entry.pack(pady=5)
task_entry.insert(0, "New task")

task_tag = ttk.Entry(tasks_tab, width=25)
task_tag.pack()
task_tag.insert(0, "#tag")

task_search = ttk.Entry(tasks_tab, width=30)
task_search.pack(pady=5)
task_search.insert(0, "Search tasks")

task_listbox = tk.Listbox(tasks_tab, width=80, height=12)
task_listbox.pack(pady=5)

def refresh_tasks():
    tasks = database.get_tasks(task_search.get())
    task_listbox.delete(0, tk.END)
    for task in tasks:
        check = "✔" if task[2] else "✘"
        tag = f" [{task[3]}]" if task[3] else ""
        task_listbox.insert(tk.END, f"[{task[0]}] {check} {task[1]}{tag} - {task[4]}")

def add_task():
    database.add_task(task_entry.get(), task_tag.get())
    task_entry.delete(0, tk.END)
    task_tag.delete(0, tk.END)
    refresh_tasks()

def delete_task():
    try:
        index = task_listbox.curselection()[0]
        task_id = int(task_listbox.get(index).split("]")[0][1:])
        database.delete_task(task_id)
        refresh_tasks()
    except:
        messagebox.showinfo("Select Task", "Please select a task to delete")

def toggle_status():
    try:
        index = task_listbox.curselection()[0]
        task = task_listbox.get(index)
        task_id = int(task.split("]")[0][1:])
        status = 1 if "✔" in task else 0
        database.toggle_task(task_id, status)
        refresh_tasks()
    except:
        messagebox.showwarning("Select Task", "Double-click a task to toggle status")

def export_tasks():
    try:
        tasks = database.get_tasks()
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", '*.pdf')])
        if file:
            pdf = canvas.Canvas(file)
            pdf.setFont("Helvetica", 14)
            pdf.drawString(50, 800, "Task List")
            y = 780
            for task in tasks:
                status = "✔" if task[2] else "✘"
                line = f"{status} {task[1]} ({task[3]}) - {task[4]}"
                pdf.setFont("Helvetica", 10)
                pdf.drawString(50, y, line)
                y -= 15
            pdf.save()
            messagebox.showinfo("Exported", f"Tasks exported to {file}")
    except:
        messagebox.showwarning("Export Failed", "Could not export tasks.")

task_button_frame = ttk.Frame(tasks_tab)
task_button_frame.pack()

task_add_btn = ttk.Button(task_button_frame, text="Add", command=add_task)
task_del_btn = ttk.Button(task_button_frame, text="Delete", command=delete_task)
task_export_btn = ttk.Button(task_button_frame, text="Export PDF", command=export_tasks)
task_search_btn = ttk.Button(task_button_frame, text="Search", command=refresh_tasks)

task_add_btn.grid(row=0, column=0, padx=5)
task_del_btn.grid(row=0, column=1, padx=5)
task_export_btn.grid(row=0, column=2, padx=5)
task_search_btn.grid(row=0, column=3, padx=5)

task_listbox.bind("<Double-Button-1>", lambda e: toggle_status())

refresh_notes()
refresh_tasks()
app.mainloop()
