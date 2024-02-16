import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

def add_item():
    item_text = entry.get()
    if item_text:
        item = tk.Frame(todo_list)
        item.grid(sticky="w")

        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(item, variable=checkbox_var, onvalue=True, offvalue=False, command=update_progress)
        checkbox.grid(row=0, column=0)

        system_font = tkFont.nametofont("TkDefaultFont")

        label = tk.Label(item, text=item_text,  wraplength=root.winfo_width(), font=system_font)
        label.grid(row=0, column=1, padx=(0, 10))

        remove_button = tk.Button(item, text="X",  command=lambda item=item, checkbox_var=checkbox_var: remove_item((item, checkbox_var)))
        remove_button.grid(row=0, column=2, sticky="e")
        todo_list.columnconfigure(2, weight=1)
        items.append((item, checkbox_var))
        entry.delete(0, tk.END)
        update_progress()

def remove_item(item_tuple):
    item_frame, _ = item_tuple
    item_frame.destroy()
    items.remove(item_tuple)
    update_progress()

def update_progress():
    total_items = len(items)
    checked_items = sum(1 for _, var in items if var.get())
    progress = (checked_items / total_items) * 100 if total_items != 0 else 0
    progress_var.set(progress)

    # Update the progress label
    progress_label.config(text=f"{progress:.1f}%")

root = tk.Tk()
root.title("ToDo List with Progress Bar")
root.geometry("1024x512")  # Set fixed window size
root.maxsize(1024, 512)
root.minsize(1024, 120)

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

entry = tk.Entry(frame, width=80)  # Adjust width of entry field
entry.grid(row=0, column=0, padx=5, pady=5)

add_button = tk.Button(frame, text="Add Item", command=add_item)
add_button.grid(row=0, column=1, padx=5, pady=5)

todo_list_frame = tk.Frame(root)
# Set sticky option for todo_list frame
todo_list_frame.grid_rowconfigure(0, weight=1)
todo_list_frame.grid_columnconfigure(0, weight=1)
todo_list_frame.grid(row=1, column=0, sticky="nsew")

# Create a canvas
todo_list_canvas = tk.Canvas(todo_list_frame)
todo_list_canvas.grid(row=0, column=0, sticky="nsew")  # Use grid instead of pack

# Create a vertical scrollbar
scrollbar = tk.Scrollbar(todo_list_frame, orient="vertical", command=todo_list_canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Link the scrollbar to the canvas
todo_list_canvas.config(yscrollcommand=scrollbar.set)

# Create a frame within the canvas
todo_list = tk.Frame(todo_list_canvas)
todo_list_canvas.create_window((0, 0), window=todo_list, anchor="nw")

# Ensure canvas can resize with window
todo_list.bind("<Configure>", lambda event, canvas=todo_list_canvas: canvas.configure(scrollregion=canvas.bbox("all")))

items = []
progress_var = tk.DoubleVar()

# Set progress bar width to match window width
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=root.winfo_width(), mode="determinate", variable=progress_var)
progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

# Create a label to display progress percentage with system default font
progress_label = tk.Label(frame, text="", font=("TkDefaultFont", tkFont.nametofont("TkDefaultFont").cget("size")))
progress_label.grid(row=2, column=0, columnspan=2)

# Configure the label to be transparent
progress_label.config(bd=0, highlightthickness=0)

root.columnconfigure(0, weight=1)  # Allow column to expand with window resizing
root.rowconfigure(1, weight=1)     # Allow row to expand with window resizing

root.mainloop()
