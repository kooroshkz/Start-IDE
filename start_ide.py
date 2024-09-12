import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from tkinter.font import Font

class StartIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Start Code IDE")
        self.file_name = None

        self.custom_font = Font(family="Consolas", size=12)

        # Create the line number bar and text editor first
        self.create_editor()

        # Now create the menu after defining the editor
        self.create_menu()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)

        self.run_button = tk.Button(self.button_frame, text="Run", command=self.run_code, font=self.custom_font, bg="#61afef", fg="white")
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_text, font=self.custom_font, bg="#e06c75", fg="white")
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.output_box = tk.Text(self.root, height=8, wrap="none", state=tk.DISABLED, font=self.custom_font, bg="#1e1e1e", fg="#98c379", insertbackground="white")
        self.output_box.pack(fill=tk.BOTH, expand=1)

        self.status_bar = tk.Label(self.root, text="Line: 1 | Column: 1", bd=1, relief=tk.SUNKEN, anchor=tk.E, bg='#3e4451', fg='white', font=self.custom_font)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.text_editor.bind("<KeyRelease>", self.update_status_bar)
        self.text_editor.bind("<KeyRelease>", self.update_line_numbers)
        self.text_editor.bind("<MouseWheel>", self.update_line_numbers)

    def create_editor(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=1)

        self.line_numbers = tk.Text(self.text_frame, width=4, bg='#3e4451', fg='white', font=self.custom_font, state=tk.DISABLED)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_editor = tk.Text(self.text_frame, wrap="none", undo=True, font=self.custom_font, bg="#1e1e1e", fg="#ffffff", insertbackground="white")
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scroll_bar = tk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)

        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_editor.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_editor.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_editor.event_generate("<<Paste>>"))

    def new_file(self):
        self.text_editor.delete(1.0, tk.END)
        self.file_name = None

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".start", filetypes=[("Start files", "*.start"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, file.read())
            self.file_name = file_path
            self.update_line_numbers()

    def save_file(self):
        if self.file_name:
            with open(self.file_name, 'w') as file:
                file.write(self.text_editor.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".start", filetypes=[("Start files", "*.start"), ("All Files", "*.*")])
        if file_path:
            self.file_name = file_path
            with open(file_path, 'w') as file:
                file.write(self.text_editor.get(1.0, tk.END))

    def run_code(self):
        if not self.file_name:
            self.save_as_file()
            if not self.file_name:
                return

        compile_command = f'python -m start_compiler.compile {self.file_name}'
        run_command = f'python {self.file_name.replace(".start", ".py")}'

        try:
            self.output_box.config(state=tk.NORMAL)
            self.output_box.delete(1.0, tk.END)

            compile_output = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
            if compile_output.returncode != 0:
                self.output_box.insert(tk.END, "Compilation Error:\n" + compile_output.stderr)
                return

            run_output = subprocess.run(run_command, shell=True, capture_output=True, text=True)
            if run_output.returncode == 0:
                self.output_box.insert(tk.END, "Program Output:\n" + run_output.stdout)
            else:
                self.output_box.insert(tk.END, "Runtime Error:\n" + run_output.stderr)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.output_box.config(state=tk.DISABLED)

    def clear_text(self):
        self.text_editor.delete(1.0, tk.END)

    def update_status_bar(self, event=None):
        row, col = self.text_editor.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Line: {row} | Column: {col}")

    def update_line_numbers(self, event=None):
        line_count = self.text_editor.index(tk.END).split('.')[0]
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        for i in range(1, int(line_count)):
            self.line_numbers.insert(tk.END, f"{i}\n")
        self.line_numbers.config(state=tk.DISABLED)

root = tk.Tk()
ide = StartIDE(root)
root.geometry("900x600")
root.mainloop()
