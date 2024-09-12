import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class StartIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Start Code IDE")
        self.file_name = None

        self.text_editor = tk.Text(self.root, wrap="none", undo=True)
        self.text_editor.pack(fill=tk.BOTH, expand=1)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text)
        self.clear_button.pack(side=tk.RIGHT)

        self.output_box = tk.Text(self.root, height=8, wrap="none", state=tk.DISABLED)
        self.output_box.pack(fill=tk.BOTH, expand=1)

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

if __name__ == '__main__':
    root = tk.Tk()
    ide = StartIDE(root)
    root.geometry("800x600")
    root.mainloop()
