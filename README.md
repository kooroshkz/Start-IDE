# Start-IDE
An IDE for the Start programming language designed to simplify learning and enhance the understanding of programming concepts. This IDE integrates a compiler, offering a smooth experience for learners to write, run, and debug code all in one place.

## Features
- **Write and Compile Start Code**: Easily write and compile Start code with the built-in editor.
- **Run Start Programs**: Seamlessly run Start programs within the IDE.
- **Debugging Support**: The IDE highlights errors, including line numbers, helping users quickly resolve issues.
- **Hints and Feedback**: Real-time feedback on programming concepts and code issues, aiding students in improving their intuition.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/kooroshkz/Start-IDE.git
cd Start-IDE
```

### 2. Install the Start Compiler
To compile Start code within the IDE, you need to install the `start_compiler`. Run the following command:

```bash
pip install start-compiler
```

### 3. Install Required Python Packages
Ensure you have `Tkinter` (for the graphical interface) installed. If you're on Ubuntu/Debian, you can install it with:

```bash
sudo apt-get install python3-tk
```

Make sure to also have other required dependencies:

```bash
pip install lark pygments
```

### 4. Run the IDE
Once all dependencies are installed, you can launch the IDE by running:

```bash
python start_ide.py
```

## Usage

1. **Write Code**: Type your Start code in the editor window.
2. **Compile**: Click the `Run` button to compile and run your code.
3. **View Output**: Results or error messages will be shown in the output section.

