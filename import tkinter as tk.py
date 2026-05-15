import tkinter as tk
from tkinter import messagebox

# ================== TO-DO FUNKCE ==================

def add_task():
    task = entry.get()
    if task != "":
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("VAROVANI", "ZADEJ UKOL!")

def delete_task():
    try:
        selected = listbox.curselection()
        listbox.delete(selected)
    except:
        messagebox.showwarning("VAROVANI", "VYBER UKOL!")

def complete_task():
    try:
        selected = listbox.curselection()
        task = listbox.get(selected)
        listbox.delete(selected)
        listbox.insert(tk.END, task + " [OK]")
    except:
        messagebox.showwarning("VAROVANI", "VYBER UKOL!")

def delete_all_tasks():
    if listbox.size() > 0:
        confirm = messagebox.askyesno("POTVRZENI", "SMAZAT VSE?")
        if confirm:
            listbox.delete(0, tk.END)
    else:
        messagebox.showinfo("INFO", "SEZNAM JE PRAZDNY.")

# ================== STOPKY ==================

time_elapsed = 0
running = False

def stopwatch():
    global time_elapsed, running
    if running:
        time_elapsed += 1
        timer_label.config(text=f"CAS: {time_elapsed}s")
        root.after(1000, stopwatch)

def start_timer():
    global running
    if not running:
        running = True
        stopwatch()

def stop_timer():
    global running
    running = False

def reset_timer():
    global time_elapsed, running
    running = False
    time_elapsed = 0
    timer_label.config(text="CAS: 0s")

# ================== GUI ==================

root = tk.Tk()
root.title("RETRO TASK MANAGER")
root.geometry("420x620")
root.configure(bg="black")  # černé pozadí

# Retro font
font_main = ("Courier", 12)
font_big = ("Courier", 14, "bold")

# Vstup
entry = tk.Entry(root, width=30, font=font_main,
                 bg="black", fg="lime",
                 insertbackground="lime")
entry.pack(pady=10)

# Funkce pro styl tlačítek
def retro_button(text, command):
    return tk.Button(root, text=text, command=command,
                     width=18, height=3,
                     font=font_main,
                     bg="black", fg="lime",
                     activebackground="lime",
                     activeforeground="black",
                     bd=2)

# Tlačítka
retro_button("PRIDAT", add_task).pack(pady=5)
retro_button("SPLNENO", complete_task).pack(pady=5)
retro_button("SMAZAT", delete_task).pack(pady=5)
retro_button("SMAZAT VSE", delete_all_tasks).pack(pady=5)

# Seznam
listbox = tk.Listbox(root, width=40, height=10,
                     bg="black", fg="lime",
                     font=font_main,
                     selectbackground="lime",
                     selectforeground="black")
listbox.pack(pady=20)

# ================== STOPKY UI ==================

timer_label = tk.Label(root, text="CAS: 0s",
                       font=font_big,
                       bg="black", fg="lime")
timer_label.pack(pady=10)

retro_button("START", start_timer).pack(pady=5)
retro_button("STOP", stop_timer).pack(pady=5)
retro_button("RESET", reset_timer).pack(pady=5)

# ================== START ==================

root.mainloop()