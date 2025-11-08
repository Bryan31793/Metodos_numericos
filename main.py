from core.metodos_numericos import MetodosNumericosUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = MetodosNumericosUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()