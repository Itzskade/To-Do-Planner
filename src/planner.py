import tkinter as tk
import json
import os

class MinimalistPlanner:
    """A minimalist tactical to-do list and daily planner application."""

    def __init__(self, root):
        """Initializes the planner application, setting up styles, layout, and loading data."""
        self.root = root
        self.root.title("To Do List Planner")
        self.root.geometry("750x880")
        
        DATA_DIR = "data"
        os.makedirs(DATA_DIR, exist_ok=True)
        self.DATA_FILE = os.path.join(DATA_DIR, "planner_data.json")

        self.BG_COLOR = "#F5EFEB" 
        self.TEXT_COLOR = "#1A1A1A"
        self.BORDER_COLOR = "#CCCCCC"
        
        self.set_styles()
        self.create_main_layout()
        self.build_todo_column()
        self.build_right_column()
        self.build_color_palette()
        
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        self.load_data()

    def set_styles(self):
        """Defines the color palette and typography configuration for the application."""
        self.root.configure(bg=self.BG_COLOR)

        self.title_font = ("Times New Roman", 26)
        self.subtitle_font = ("Arial", 11, "bold")
        self.text_font = ("Arial", 11)

    def create_main_layout(self):
        """Creates the primary structures including the top header and body split frame."""
        self.title_label = tk.Label(
            self.root, 
            text="T O   D O   L I S T", 
            font=self.title_font, 
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(45, 30))

        self.body_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.body_frame.grid(row=1, column=0, columnspan=2, padx=40, pady=20, sticky="nsew")
        
        self.body_frame.columnconfigure(0, weight=1, uniform="group1")
        self.body_frame.columnconfigure(1, weight=1, uniform="group1")
        self.body_frame.rowconfigure(0, weight=1)

    def build_todo_column(self):
        """Builds the left column containing the main task input field and scrollable area."""
        self.todo_frame = tk.LabelFrame(
            self.body_frame, 
            text="  TO DO  ", 
            font=self.subtitle_font,
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR,
            labelanchor="n", 
            relief="solid", 
            bd=1
        )
        self.todo_frame.grid(row=0, column=0, padx=(0, 20), sticky="nsew")
        
        self.task_entry = tk.Entry(
            self.todo_frame, 
            font=self.text_font, 
            bd=0, 
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            highlightthickness=1, 
            highlightbackground=self.BORDER_COLOR,
            highlightcolor=self.TEXT_COLOR,
            insertbackground=self.TEXT_COLOR
        )
        self.task_entry.pack(fill="x", padx=20, pady=15)
        self.task_entry.insert(0, " Type here and press Enter...")
        
        self.task_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.task_entry, " Type here and press Enter..."))
        self.task_entry.bind("<Return>", self.add_task)

        self.todo_canvas = tk.Canvas(self.todo_frame, bg=self.BG_COLOR, bd=0, highlightthickness=0)
        self.todo_canvas.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.task_list_frame = tk.Frame(self.todo_canvas, bg=self.BG_COLOR)
        self.todo_canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw")
        self.task_list_frame.bind("<Configure>", lambda e: self.todo_canvas.configure(scrollregion=self.todo_canvas.bbox("all")))

    def build_right_column(self):
        """Builds the right stacked panel for Priorities, Notes, and Reminders."""
        self.right_column = tk.Frame(self.body_frame, bg=self.BG_COLOR)
        self.right_column.grid(row=0, column=1, padx=(20, 0), sticky="nsew")
        
        self.right_column.columnconfigure(0, weight=1)
        self.right_column.rowconfigure(0, weight=0)
        self.right_column.rowconfigure(1, weight=1)
        self.right_column.rowconfigure(2, weight=1)

        self.create_priorities_block(self.right_column)
        self.create_notes_block(self.right_column)
        self.create_reminder_block(self.right_column)

    def build_color_palette(self):
        """Builds the color theme squares section at the bottom."""
        self.palette_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.palette_frame.grid(row=2, column=0, columnspan=2, pady=(10, 35))
        
        themes = {
            "Cream": "#F5EFEB",
            "Blue": "#EBF3F5",
            "Pink": "#F5EBEF",
            "Green": "#EBEFEE"
        }
        
        for name, hex_code in themes.items():
            btn = tk.Label(
                self.palette_frame, 
                text="       ", 
                bg=hex_code, 
                relief="solid", 
                bd=1, 
                cursor="hand2"
            )
            btn.pack(side="left", padx=10)
            btn.bind("<Button-1>", lambda e, color=hex_code, t_name=name: self.apply_theme(color, t_name))

    def apply_theme(self, hex_color, theme_name):
        """Recursively applies a chosen theme color across structural and atomic widgets."""
        self.BG_COLOR = hex_color
        self.current_theme_name = theme_name
        
        self.root.configure(bg=hex_color)
        self.title_label.configure(bg=hex_color)
        self.body_frame.configure(bg=hex_color)
        self.right_column.configure(bg=hex_color)
        self.palette_frame.configure(bg=hex_color)
        
        self.todo_frame.configure(bg=hex_color)
        self.task_entry.configure(bg=hex_color, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR)
        self.todo_canvas.configure(bg=hex_color)
        self.task_list_frame.configure(bg=hex_color)
        
        self.priorities_frame.configure(bg=hex_color)
        self.priority_canvas.configure(bg=hex_color)
        self.priority_list_frame.configure(bg=hex_color)
        
        self.notes_frame.configure(bg=hex_color)
        self.notes_text.configure(bg=hex_color, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR)
        
        self.reminder_frame.configure(bg=hex_color)
        self.reminder_text.configure(bg=hex_color, fg=self.TEXT_COLOR, insertbackground=self.TEXT_COLOR)
        
        def update_child_widgets(widget):
            for child in widget.winfo_children():
                try:
                    child.configure(bg=hex_color, activebackground=hex_color)
                except tk.TclError:
                    pass
                update_child_widgets(child)
                
        update_child_widgets(self.task_list_frame)
        update_child_widgets(self.priority_list_frame)
        
        self.save_data()

    def create_priorities_block(self, container):
        """Creates the ultra-compact priority section with a targeted height of 80 pixels."""
        self.priorities_frame = tk.LabelFrame(
            container, 
            text="  PRIORITIES  ", 
            font=self.subtitle_font,
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR,
            labelanchor="n", 
            relief="solid", 
            bd=1
        )
        self.priorities_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        
        self.priority_canvas = tk.Canvas(self.priorities_frame, bg=self.BG_COLOR, bd=0, highlightthickness=0, height=80)
        self.priority_canvas.pack(fill="x", expand=False, padx=20, pady=4)
        
        self.priority_list_frame = tk.Frame(self.priority_canvas, bg=self.BG_COLOR)
        self.priority_canvas.create_window((0, 0), window=self.priority_list_frame, anchor="nw")
        self.priority_list_frame.bind("<Configure>", lambda e: self.priority_canvas.configure(scrollregion=self.priority_canvas.bbox("all")))

    def create_notes_block(self, container):
        """Creates the text input block dedicated to unstructured daily notes."""
        self.notes_frame = tk.LabelFrame(
            container, 
            text="  NOTES  ", 
            font=self.subtitle_font,
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR,
            labelanchor="n", 
            relief="solid", 
            bd=1
        )
        self.notes_frame.grid(row=1, column=0, pady=10, sticky="nsew")
        
        self.notes_text = tk.Text(
            self.notes_frame, 
            font=self.text_font, 
            bd=0, 
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR,
            insertbackground=self.TEXT_COLOR,
            wrap="word", 
            height=4
        )
        self.notes_text.pack(fill="both", expand=True, padx=20, pady=10)
        self.notes_text.bind("<FocusOut>", lambda e: self.save_data())

    def create_reminder_block(self, container):
        """Creates the text input block dedicated to specific reminders."""
        self.reminder_frame = tk.LabelFrame(
            container, 
            text="  REMINDER  ", 
            font=self.subtitle_font,
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR,
            labelanchor="n", 
            relief="solid", 
            bd=1
        )
        self.reminder_frame.grid(row=2, column=0, pady=(10, 0), sticky="nsew")
        
        self.reminder_text = tk.Text(
            self.reminder_frame, 
            font=self.text_font, 
            bd=0, 
            bg=self.BG_COLOR, 
            fg=self.TEXT_COLOR,
            insertbackground=self.TEXT_COLOR,
            wrap="word", 
            height=4
        )
        self.reminder_text.pack(fill="both", expand=True, padx=20, pady=10)
        self.reminder_text.bind("<FocusOut>", lambda e: self.save_data())

    def clear_placeholder(self, entry_widget, placeholder_text):
        """Clears the predefined fallback placeholder text when the user selects the input field."""
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, tk.END)

    def add_task(self, event):
        """Extracts text from the entry element, constructs a new task, and saves the state."""
        text = self.task_entry.get().strip()
        if text and text != "Type here and press Enter...":
            self.create_item(self.task_list_frame, text, is_todo=True)
            self.task_entry.delete(0, tk.END)
            self.save_data()

    def create_item(self, target_frame, text, is_todo, checked=False):
        """Constructs an atomic task row item with contextual triggers (double click, delete, toggle)."""
        row_frame = tk.Frame(target_frame, bg=self.BG_COLOR)
        pady_val = 4 if is_todo else 3
        row_frame.pack(fill="x", pady=pady_val)

        if is_todo:
            check_var = tk.BooleanVar(value=checked)
            cb = tk.Checkbutton(
                row_frame, 
                variable=check_var,
                bg=self.BG_COLOR,
                activebackground=self.BG_COLOR,
                relief="flat",
                bd=0
            )
            cb.pack(side="left")

            lbl = tk.Label(row_frame, text=text, font=self.text_font, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
            lbl.pack(side="left", padx=5)

            def toggle_status():
                """Updates the visual rendering of the text (strikethrough) based on checkbox state."""
                if check_var.get():
                    lbl.config(fg="#999999", font=(self.text_font[0], self.text_font[1], "overstrike"))
                else:
                    lbl.config(fg=self.TEXT_COLOR, font=self.text_font)
                self.save_data()

            cb.config(command=toggle_status)
            toggle_status()
            
            lbl.bind("<Double-Button-1>", lambda e: self.move_item(row_frame, text, to_todo=False))
        else:
            lbl = tk.Label(row_frame, text=text, font=self.text_font, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
            lbl.pack(side="left", padx=5)
            lbl.bind("<Double-Button-1>", lambda e: self.move_item(row_frame, text, to_todo=True))

        def delete_item():
            row_frame.destroy()
            self.root.after(10, self.save_data) 

        delete_btn = tk.Label(row_frame, text="✕", font=self.text_font, bg=self.BG_COLOR, fg="#999999", cursor="hand2")
        delete_btn.pack(side="right", padx=10)
        delete_btn.bind("<Button-1>", lambda e: delete_item())

    def move_item(self, row_frame, text, to_todo):
        """Cycles dynamic records safely between the task column and the priority block."""
        if not to_todo:
            current_priorities = len(self.priority_list_frame.winfo_children())
            if current_priorities >= 3:
                return
                
        row_frame.destroy()
        if to_todo:
            self.create_item(self.task_list_frame, text, is_todo=True)
        else:
            self.create_item(self.priority_list_frame, text, is_todo=False)
        self.root.after(10, self.save_data)

    def save_data(self):
        """Serializes the comprehensive graphical user interface states into JSON."""
        data = {
            "theme_color": self.BG_COLOR,
            "theme_name": getattr(self, "current_theme_name", "Cream"),
            "todo": [],
            "priorities": [],
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "reminder": self.reminder_text.get("1.0", tk.END).strip()
        }
        
        for frame in self.task_list_frame.winfo_children():
            widgets = frame.winfo_children()
            if len(widgets) >= 2:
                cb = widgets[0]
                lbl = widgets[1]
                is_checked = cb.getvar(cb.cget("variable"))
                data["todo"].append({"text": lbl.cget("text"), "checked": bool(int(is_checked))})
                
        for frame in self.priority_list_frame.winfo_children():
            widgets = frame.winfo_children()
            if len(widgets) >= 1:
                lbl = widgets[0]
                data["priorities"].append(lbl.cget("text"))
                
        with open(self.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """De-serializes data models from JSON storage and mounts widgets back into the UI views."""
        if not os.path.exists(self.DATA_FILE):
            return
            
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            saved_color = data.get("theme_color", "#F5EFEB")
            saved_name = data.get("theme_name", "Cream")
            self.apply_theme(saved_color, saved_name)
                
            for item in data.get("todo", []):
                self.create_item(self.task_list_frame, item["text"], is_todo=True, checked=item["checked"])
                
            for text in data.get("priorities", []):
                self.create_item(self.priority_list_frame, text, is_todo=False)
                
            self.notes_text.insert("1.0", data.get("notes", ""))
            self.reminder_text.insert("1.0", data.get("reminder", ""))
        except Exception as e:
            print(f"Failed to load persistence storage payload: {e}")

    def run(self):
        """Registers system interception routines and boots up the main loop engine."""
        self.root.protocol("WM_DELETE_WINDOW", lambda: [self.save_data(), self.root.destroy()])
        self.root.mainloop()
