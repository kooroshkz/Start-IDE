import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from tkinter.font import Font
import os

class StartIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Start Code IDE")
        self.file_name = None

        self.root.configure(bg='#282c34')
        self.custom_font = Font(family="Consolas", size=12)

        self.text_editor = tk.Text(self.root, wrap="none", undo=True, font=self.custom_font, bg="#1e1e1e", fg="#ffffff", insertbackground="white")
        self.text_editor.pack(fill=tk.BOTH, expand=1)

        self.button_frame = tk.Frame(self.root, bg='#282c34')
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

    def clear_text(self):
        self.text_editor.delete(1.0, tk.END)

    def run_code(self):
        self.file_name = 'code.start'
        with open(self.file_name, 'w') as file:
            file.write(self.text_editor.get(1.0, tk.END))

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

    def update_status_bar(self, event=None):
        row, col = self.text_editor.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Line: {row} | Column: {col}")

if __name__ == '__main__':
    root = tk.Tk()
    ide = StartIDE(root)
    root.geometry("800x600")
    root.mainloop()
