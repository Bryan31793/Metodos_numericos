import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import simpy as sp

class MetodosNumericosUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')
        
        # Variables para inputs
        self.current_entry = None
        self.input_fields = {}
        
        # Frame principal horizontal
        main_container = tk.Frame(root, bg='#2b2b2b')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo (contenido principal)
        left_frame = tk.Frame(main_container, bg='#2b2b2b')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Frame superior para el menú
        self.menu_frame = tk.Frame(left_frame, bg='#3c3c3c', relief=tk.RAISED, bd=2)
        self.menu_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_menu()
        
        # Frame central para contenido
        self.content_frame = tk.Frame(left_frame, bg='#2b2b2b')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de salida
        output_label = tk.Label(self.content_frame, text="Resultados:", 
                               bg='#2b2b2b', fg='white', font=('Arial', 12, 'bold'))
        output_label.pack(anchor='w')
        
        self.output_text = scrolledtext.ScrolledText(
            self.content_frame, 
            height=12, 
            bg='#1e1e1e', 
            fg='#00ff00',
            font=('Consolas', 10),
            insertbackground='white'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Frame para inputs dinámicos con scroll
        input_container = tk.Frame(self.content_frame, bg='#2b2b2b')
        input_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas y scrollbar para inputs
        self.input_canvas = tk.Canvas(input_container, bg='#2b2b2b', highlightthickness=0)
        input_scrollbar = tk.Scrollbar(input_container, orient="vertical", command=self.input_canvas.yview)
        self.input_frame = tk.Frame(self.input_canvas, bg='#2b2b2b')
        
        self.input_canvas.configure(yscrollcommand=input_scrollbar.set)
        
        input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.input_canvas_window = self.input_canvas.create_window((0, 0), window=self.input_frame, anchor='nw')
        
        self.input_frame.bind('<Configure>', self.on_input_frame_configure)
        self.input_canvas.bind('<Configure>', self.on_input_canvas_configure)
        
        # Frame derecho (teclado matemático - barra lateral)
        right_frame = tk.Frame(main_container, bg='#3c3c3c', relief=tk.RAISED, bd=2, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        self.create_math_keyboard(right_frame)
        
        self.show_main_menu()
    
    def on_input_frame_configure(self, event=None):
        """Actualiza el scrollregion cuando cambia el tamaño del frame"""
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))
    
    def on_input_canvas_configure(self, event):
        """Ajusta el ancho del frame interno al canvas"""
        self.input_canvas.itemconfig(self.input_canvas_window, width=event.width)
    
    def create_menu(self):
        """Crea el menú principal con botones"""
        title = tk.Label(self.menu_frame, text="MÉTODOS NUMÉRICOS", 
                        bg='#3c3c3c', fg='#00ff00', 
                        font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        buttons_frame = tk.Frame(self.menu_frame, bg='#3c3c3c')
        buttons_frame.pack(pady=10)
        
        buttons = [
            ("1. Punto Fijo", self.punto_fijo_ui),
            ("2. Jacobi", self.jacobi_ui),
            ("3. Interpolación Multiple", self.interpolacion_ui),
            ("4. Simpson 3/8", self.simpson_ui),
            ("5. 2da Derivada", self.derivada_ui),
            ("6. Runge-Kutta", self.rk_ui),
            ("7. Sistema EDO", self.sistema_edo_ui),
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 4
            col = i % 4
            btn = tk.Button(buttons_frame, text=text, command=command,
                          bg='#4a4a4a', fg='white', font=('Arial', 10, 'bold'),
                          width=18, height=2, relief=tk.RAISED, bd=3,
                          activebackground='#5a5a5a')
            btn.grid(row=row, column=col, padx=5, pady=5)
    
    def create_math_keyboard(self, parent):
        """Crea el teclado matemático en barra lateral"""
        title = tk.Label(parent, text="TECLADO MATEMÁTICO", 
                        bg='#3c3c3c', fg='#00ff00', 
                        font=('Arial', 12, 'bold'))
        title.pack(pady=10)
        
        # Instrucciones
        info = tk.Label(parent, text="Haz clic en un campo de entrada\ny usa los botones abajo", 
                       bg='#3c3c3c', fg='#ffff00', 
                       font=('Arial', 9, 'italic'), justify=tk.CENTER)
        info.pack(pady=5)
        
        # Definir botones del teclado
        keys = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', ',', '+'],
            ['(', ')', '[', ']'],
            ['x', 'y', 't', 'v'],
            ['x²', 'x³', '**', '√'],
            ['sin', 'cos', 'tan', 'exp'],
            ['log', 'abs', 'pi', 'e'],
            ['np.sin(', 'np.cos(', 'np.tan(', '←'],
            ['np.exp(', 'np.log(', 'np.sqrt(', 'Clear']
        ]
        
        keyboard_grid = tk.Frame(parent, bg='#3c3c3c')
        keyboard_grid.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        for i, row in enumerate(keys):
            for j, key in enumerate(row):
                if key == '←':
                    cmd = self.backspace
                    bg = '#d9534f'
                    display_text = '⌫'
                elif key == 'Clear':
                    cmd = self.clear_entry
                    bg = '#f0ad4e'
                    display_text = 'Limpiar'
                elif key == '√':
                    cmd = lambda: self.insert_text('np.sqrt(')
                    bg = '#5a5a5a'
                    display_text = key
                elif key == 'sin':
                    cmd = lambda: self.insert_text('np.sin(')
                    bg = '#5a5a5a'
                    display_text = key
                elif key == 'cos':
                    cmd = lambda: self.insert_text('np.cos(')
                    bg = '#5a5a5a'
                    display_text = key
                elif key == 'tan':
                    cmd = lambda: self.insert_text('np.tan(')
                    bg = '#5a5a5a'
                    display_text = key
                elif key == 'exp':
                    cmd = lambda: self.insert_text('np.exp(')
                    bg = '#5a5a5a'
                    display_text = key
                elif key == 'log':
                    cmd = lambda: self.insert_text('np.log(')
                    bg = '#5a5a5a'
                    display_text = key
                elif key == 'abs':
                    cmd = lambda: self.insert_text('abs(')
                    bg = '#5a5a5a'
                    display_text = key
                elif key == 'pi':
                    cmd = lambda: self.insert_text('np.pi')
                    bg = '#5a5a5a'
                    display_text = 'π'
                elif key == 'e':
                    cmd = lambda: self.insert_text('np.e')
                    bg = '#5a5a5a'
                    display_text = key
                else:
                    cmd = lambda k=key: self.insert_text(k)
                    bg = '#5a5a5a'
                    display_text = key
                
                btn = tk.Button(keyboard_grid, text=display_text, command=cmd,
                              bg=bg, fg='white', font=('Arial', 10, 'bold'),
                              width=8, height=2, relief=tk.RAISED, bd=2)
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
        
        # Hacer que las columnas se expandan
        for j in range(4):
            keyboard_grid.grid_columnconfigure(j, weight=1)
    
    def insert_text(self, text):
        """Inserta texto en el campo activo"""
        if self.current_entry:
            self.current_entry.insert(tk.INSERT, text)
            self.current_entry.focus()
    
    def backspace(self):
        """Borra el último carácter"""
        if self.current_entry:
            content = self.current_entry.get()
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, content[:-1])
            self.current_entry.focus()
    
    def clear_entry(self):
        """Limpia el campo activo"""
        if self.current_entry:
            self.current_entry.delete(0, tk.END)
            self.current_entry.focus()
    
    def clear_input_frame(self):
        """Limpia todos los widgets del frame de inputs"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.input_fields = {}
        self.current_entry = None
    
    def clear_output(self):
        """Limpia el área de salida"""
        self.output_text.delete(1.0, tk.END)
    
    def print_output(self, text, color='#00ff00'):
        """Imprime texto en el área de salida"""
        self.output_text.insert(tk.END, text + '\n', color)
        self.output_text.see(tk.END)
        self.output_text.update()
    
    def create_entry_field(self, label_text, row, default=""):
        """Crea un campo de entrada con etiqueta"""
        label = tk.Label(self.input_frame, text=label_text, 
                        bg='#2b2b2b', fg='white', font=('Arial', 10))
        label.grid(row=row, column=0, sticky='w', padx=5, pady=5)
        
        entry = tk.Entry(self.input_frame, bg='#3c3c3c', fg='white', 
                        font=('Arial', 10), insertbackground='white', width=50)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        entry.bind('<FocusIn>', lambda e: self.set_current_entry(entry))
        
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        return entry
    
    def set_current_entry(self, entry):
        """Establece el campo de entrada actual"""
        self.current_entry = entry
    
    def show_main_menu(self):
        """Muestra el menú principal"""
        self.clear_input_frame()
        self.clear_output()
        self.print_output("="*70, '#00ff00')
        self.print_output("FCFM")
        self.print_output("Bryan Ramirez Lopez 2103765")
        self.print_output("ANPP gpo: 031")
        self.print_output("BIENVENIDO AL PROGRAMA DE MÉTODOS NUMÉRICOS", '#00ffff')
        self.print_output("="*70, '#00ff00')
        self.print_output("\nSeleccione un método usando los botones superiores:", '#ffff00')
        self.print_output("\nUse el teclado matemático de la derecha para ingresar expresiones", '#ffff00')
    
    # ============ MÉTODO 1: PUNTO FIJO ============
    def punto_fijo_ui(self):
        self.clear_input_frame()
        self.clear_output()
        self.print_output("=== MÉTODO DEL PUNTO FIJO ===\n", '#00ffff')
        self.print_output("Ingrese f(x) = 0 y el método generará g(x) automáticamente\n", '#ffff00')
        
        self.input_fields['f'] = self.create_entry_field("f(x) = 0, donde f(x) =", 0, "x**2 - 2*x - 3")
        
        # Opciones para generar g(x)
        tk.Label(self.input_frame, text="Método para generar g(x):", 
                bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                row=1, column=0, columnspan=2, pady=5, sticky='w', padx=5)
        
        self.metodo_g = tk.StringVar(value="despejar_x")
        
        rb_frame = tk.Frame(self.input_frame, bg='#2b2b2b')
        rb_frame.grid(row=2, column=0, columnspan=2, sticky='w', padx=5)
                
        tk.Radiobutton(rb_frame, text="g(x) = x + α*f(x) (α personalizado)", 
                    variable=self.metodo_g, value="alfa", bg='#2b2b2b', fg='white', 
                    selectcolor='#4a4a4a', font=('Arial', 9)).pack(anchor='w')
        
        tk.Radiobutton(rb_frame, text="g(x) = x - f(x)/f'(x) (Newton)", 
                    variable=self.metodo_g, value="newton", bg='#2b2b2b', fg='white', 
                    selectcolor='#4a4a4a', font=('Arial', 9)).pack(anchor='w')
        
        self.input_fields['alfa'] = self.create_entry_field("α (solo si seleccionó α personalizado):", 3, "-0.1")
        self.input_fields['x0'] = self.create_entry_field("Valor inicial x0:", 4, "1")
        self.input_fields['tol'] = self.create_entry_field("Tolerancia:", 5, "0.0001")
        self.input_fields['max_iter'] = self.create_entry_field("Máx. iteraciones:", 6, "50")
        
        btn = tk.Button(self.input_frame, text="Calcular", command=self.calcular_punto_fijo,
                    bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), 
                    width=20, height=2)
        btn.grid(row=7, column=0, columnspan=2, pady=20)
        
        self.current_entry = self.input_fields['f']
        self.input_fields['f'].focus()

    def calcular_punto_fijo(self):
        try:
            f_str = self.input_fields['f'].get()
            x0 = float(self.input_fields['x0'].get())
            tol = float(self.input_fields['tol'].get())
            max_iter = int(self.input_fields['max_iter'].get())
            metodo = self.metodo_g.get()
            
            # Definir f(x)
            f = lambda x: eval(f_str)
            
            # Generar g(x) según el método seleccionado
            if metodo == "alfa":
                alfa = float(self.input_fields['alfa'].get())
                g = lambda x: x + alfa * f(x)
                g_descripcion = f"g(x) = x + {alfa}*f(x)"
            elif metodo == "newton":
                # Derivada numérica con diferencias centrales
                h = 1e-8
                f_prima = lambda x: (f(x + h) - f(x - h)) / (2 * h)
                g = lambda x: x - f(x) / f_prima(x)
                g_descripcion = "g(x) = x - f(x)/f'(x) (Método de Newton)"
            else:
                messagebox.showerror("Error", "Seleccione un método válido")
                return
            
            self.clear_output()
            self.print_output("=== MÉTODO DEL PUNTO FIJO ===\n", '#00ffff')
            self.print_output(f"f(x) = {f_str}", '#ffff00')
            self.print_output(f"{g_descripcion}\n", '#00ff00')
            
            # Verificar condición de convergencia inicial
            x_test = x0
            try:
                # Estimar |g'(x0)| numéricamente
                h = 1e-6
                g_prima_x0 = abs((g(x_test + h) - g(x_test - h)) / (2 * h))
                self.print_output(f"|g'(x0)| ≈ {g_prima_x0:.6f}", '#ffff00')
                if g_prima_x0 >= 1:
                    self.print_output("⚠ Advertencia: |g'(x0)| ≥ 1, puede no converger\n", '#ff0000')
                else:
                    self.print_output("✓ |g'(x0)| < 1, se espera convergencia\n", '#00ff00')
            except:
                self.print_output("No se pudo verificar convergencia\n", '#ffff00')
            
            self.print_output(f"{'Iter':<8}{'x':<18}{'f(x)':<18}{'g(x)':<18}{'Error':<15}", '#ffff00')
            self.print_output("-"*77, '#ffff00')
            
            x = x0
            for i in range(max_iter):
                try:
                    f_x = f(x)
                    x_nuevo = g(x)
                    error = abs(x_nuevo - x)
                    
                    self.print_output(f"{i:<8}{x:<18.10f}{f_x:<18.10e}{x_nuevo:<18.10f}{error:<15.2e}")
                    
                    if error < tol:
                        self.print_output(f"\n✓ Raíz encontrada: x = {x_nuevo:.10f}", '#00ff00')
                        self.print_output(f"  f({x_nuevo:.10f}) = {f(x_nuevo):.2e}", '#00ff00')
                        self.print_output(f"  Iteraciones: {i+1}", '#00ff00')
                        self.print_output(f"  Error final: {error:.2e}", '#00ff00')
                        return
                    
                    # Detectar divergencia
                    if abs(x_nuevo) > 1e10:
                        self.print_output(f"\n✗ Divergió: |x| > 10^10", '#ff0000')
                        self.print_output(f"  Intente con otro método o valor inicial diferente", '#ff0000')
                        return
                    
                    x = x_nuevo
                    
                except (ZeroDivisionError, OverflowError) as e:
                    self.print_output(f"\n✗ Error numérico en iteración {i}: {str(e)}", '#ff0000')
                    self.print_output(f"  Intente con otro método o valor inicial", '#ff0000')
                    return
            
            self.print_output(f"\n⚠ No convergió en {max_iter} iteraciones", '#ff0000')
            self.print_output(f"  Último valor: x = {x:.10f}", '#ff0000')
            self.print_output(f"  f(x) = {f(x):.2e}", '#ff0000')
            self.print_output(f"\n  Sugerencias:", '#ffff00')
            self.print_output(f"  • Intente otro valor inicial x0", '#ffff00')
            self.print_output(f"  • Pruebe otro método para generar g(x)", '#ffff00')
            self.print_output(f"  • Aumente el número de iteraciones", '#ffff00')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")
    
    # ============ MÉTODO 5: SEGUNDA DERIVADA ============
    def derivada_ui(self):
        self.clear_input_frame()
        self.clear_output()
        self.print_output("=== SEGUNDA DERIVADA NUMÉRICA ===\n", '#00ffff')
        
        self.input_fields['f'] = self.create_entry_field("f(x) =", 0, "x**3")
        self.input_fields['x0'] = self.create_entry_field("Punto x0:", 1, "1")
        self.input_fields['h'] = self.create_entry_field("Paso h:", 2, "0.01")
        
        btn = tk.Button(self.input_frame, text="Calcular", command=self.calcular_derivada,
                       bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
        btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.current_entry = self.input_fields['f']
        self.input_fields['f'].focus()
    
    def calcular_derivada(self):
        try:
            f_str = self.input_fields['f'].get()
            x0 = float(self.input_fields['x0'].get())
            h = float(self.input_fields['h'].get())
            
            f = lambda x: eval(f_str)
            
            f_mas = f(x0 + h)
            f_centro = f(x0)
            f_menos = f(x0 - h)
            
            f_segunda = (f_mas - 2*f_centro + f_menos) / (h**2)
            
            self.clear_output()
            self.print_output("=== RESULTADOS ===\n", '#00ffff')
            self.print_output(f"✓ Segunda derivada:", '#00ff00')
            self.print_output(f"  f''({x0}) ≈ {f_segunda:.10f}", '#00ff00')
            self.print_output(f"\nValores utilizados:", '#ffff00')
            self.print_output(f"  f({x0-h:.4f}) = {f_menos:.8f}")
            self.print_output(f"  f({x0:.4f}) = {f_centro:.8f}")
            self.print_output(f"  f({x0+h:.4f}) = {f_mas:.8f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")
    
    # ============ MÉTODO 6: RUNGE-KUTTA ============
    def rk_ui(self):
        self.clear_input_frame()
        self.clear_output()
        self.print_output("=== RUNGE-KUTTA 2DO ORDEN (EDO 1er Orden) ===\n", '#00ffff')
        self.print_output("Resolver: y' = f(t, y)\n", '#ffff00')
        
        self.input_fields['f'] = self.create_entry_field("f(t, y) =", 0, "-2*y")
        self.input_fields['t0'] = self.create_entry_field("t inicial:", 1, "0")
        self.input_fields['y0'] = self.create_entry_field("y(t0):", 2, "1")
        self.input_fields['tf'] = self.create_entry_field("t final:", 3, "2")
        self.input_fields['h'] = self.create_entry_field("Paso h:", 4, "0.1")
        
        btn = tk.Button(self.input_frame, text="Calcular", command=self.calcular_rk,
                       bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
        btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        self.current_entry = self.input_fields['f']
        self.input_fields['f'].focus()
    
    def calcular_rk(self):
        try:
            f_str = self.input_fields['f'].get()
            t0 = float(self.input_fields['t0'].get())
            y0 = float(self.input_fields['y0'].get())
            tf = float(self.input_fields['tf'].get())
            h = float(self.input_fields['h'].get())
            
            f = lambda t, y: eval(f_str)
            
            n_pasos = int((tf - t0) / h)
            
            t = np.zeros(n_pasos + 1)
            y = np.zeros(n_pasos + 1)
            
            t[0] = t0
            y[0] = y0
            
            self.clear_output()
            self.print_output("=== RESULTADOS ===\n", '#00ffff')
            self.print_output(f"{'Paso':<8}{'t':<15}{'y':<18}", '#ffff00')
            self.print_output("-"*41, '#ffff00')
            
            # Runge-Kutta de 2do orden
            for i in range(n_pasos):
                k1 = f(t[i], y[i])
                t_mid = t[i] + h/2
                y_mid = y[i] + (h/2) * k1
                k2 = f(t_mid, y_mid)
                
                t[i+1] = t[i] + h
                y[i+1] = y[i] + h * k2
                
                if (i+1) % max(1, n_pasos // 10) == 0 or i == n_pasos - 1:
                    self.print_output(f"{i+1:<8}{t[i+1]:<15.6f}{y[i+1]:<18.10f}")
            
            self.print_output(f"\n✓ Solución encontrada:", '#00ff00')
            self.print_output(f"  y({tf}) ≈ {y[-1]:.10f}", '#00ff00')
            self.print_output(f"  Pasos totales: {n_pasos}", '#00ff00')
            
            # Mostrar gráfica
            self.mostrar_grafica_rk(t, y)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")
    
    def mostrar_grafica_rk(self, t, y):
        """Muestra la gráfica de Runge-Kutta"""
        top = tk.Toplevel(self.root)
        top.title("Gráfica - Runge-Kutta")
        top.geometry("800x600")
        
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(t, y, 'b-', linewidth=2, marker='o', markersize=4, label='y(t)')
        ax.set_xlabel('t', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title("Solución de la EDO: y' = f(t, y)", fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # ============ MÉTODO 7: SISTEMA DE EDO ============
    # ============ MÉTODO 7: SISTEMA DE EDO CON EULER ============
    def sistema_edo_ui(self):
        self.clear_input_frame()
        self.clear_output()
        self.print_output("=== SISTEMA DE EDO - MÉTODO DE EULER ===\n", '#00ffff')
        self.print_output("Resolver sistema: y'₁ = f₁(t, y₁, y₂, ...)", '#ffff00')
        self.print_output("                  y'₂ = f₂(t, y₁, y₂, ...)", '#ffff00')
        self.print_output("                  ...\n", '#ffff00')
        
        self.input_fields['n_ecuaciones'] = self.create_entry_field("Número de ecuaciones:", 0, "2")
        
        btn = tk.Button(self.input_frame, text="Continuar", command=self.sistema_edo_config_ui,
                    bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20)
        btn.grid(row=1, column=0, columnspan=2, pady=20)
        
        self.current_entry = self.input_fields['n_ecuaciones']
        self.input_fields['n_ecuaciones'].focus()

    def sistema_edo_config_ui(self):
        try:
            n = int(self.input_fields['n_ecuaciones'].get())
            self.n_sistema = n  # Guardar n como atributo
            self.clear_input_frame()
            
            tk.Label(self.input_frame, text="Ingrese las ecuaciones diferenciales:", 
                    bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                    row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
            
            tk.Label(self.input_frame, text="Use: t para tiempo, y[0], y[1], ... para las variables", 
                    bg='#2b2b2b', fg='#ffff00', font=('Arial', 9, 'italic')).grid(
                    row=1, column=0, columnspan=2, pady=2, sticky='w', padx=5)
            
            self.input_fields['funciones'] = []
            ejemplos = ["y[1]", "-y[0]", "-0.5*y[1]"]
            
            for i in range(n):
                ejemplo = ejemplos[i] if i < len(ejemplos) else f"y[{(i+1)%n}]"
                func_entry = self.create_entry_field(f"y'[{i}] = f{i}(t, y) =", i+2, ejemplo)
                self.input_fields['funciones'].append(func_entry)
            
            # Condiciones iniciales
            tk.Label(self.input_frame, text="Condiciones iniciales:", 
                    bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                    row=n+2, column=0, columnspan=2, pady=5, sticky='w', padx=5)
            
            self.input_fields['y0_vals'] = []
            for i in range(n):
                y0_entry = self.create_entry_field(f"y[{i}](t₀) =", n+3+i, str(1 if i == 0 else 0))
                self.input_fields['y0_vals'].append(y0_entry)
            
            # Parámetros temporales
            self.input_fields['t0_sistema'] = self.create_entry_field("t inicial:", 2*n+3, "0")
            self.input_fields['tf_sistema'] = self.create_entry_field("t final:", 2*n+4, "10")
            self.input_fields['h_sistema'] = self.create_entry_field("Paso h:", 2*n+5, "0.01")
            
            btn = tk.Button(self.input_frame, text="Resolver con Euler", command=self.calcular_sistema_edo,
                        bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
            btn.grid(row=2*n+6, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calcular_sistema_edo(self):
        try:
            n = self.n_sistema  # Usar el atributo guardado
            
            # Leer funciones
            funciones_str = [self.input_fields['funciones'][i].get() for i in range(n)]
            
            # Crear función del sistema
            def sistema(t, y):
                dydt = np.zeros(n)
                for i in range(n):
                    dydt[i] = eval(funciones_str[i])
                return dydt
            
            # Condiciones iniciales
            y0 = np.array([float(self.input_fields['y0_vals'][i].get()) for i in range(n)])
            
            t0 = float(self.input_fields['t0_sistema'].get())
            tf = float(self.input_fields['tf_sistema'].get())
            h = float(self.input_fields['h_sistema'].get())
            
            n_pasos = int((tf - t0) / h)
            
            t = np.zeros(n_pasos + 1)
            y_vals = np.zeros((n_pasos + 1, n))
            
            t[0] = t0
            y_vals[0] = y0
            
            self.clear_output()
            self.print_output("=== MÉTODO DE EULER ===\n", '#00ffff')
            
            # Encabezado
            header = f"{'Paso':<8}{'t':<12}"
            for i in range(n):
                header += f"{'y['+str(i)+']':<15}"
            self.print_output(header, '#ffff00')
            self.print_output("-"*(20 + 15*n), '#ffff00')
            
            # Método de Euler para sistemas
            # y_{n+1} = y_n + h * f(t_n, y_n)
            for i in range(n_pasos):
                y = y_vals[i]  # Estado actual
                
                # Calcular derivadas en el punto actual
                dydt = sistema(t[i], y)
                
                # Actualizar usando Euler
                t[i+1] = t[i] + h
                y_vals[i+1] = y + h * dydt
                
                # Mostrar cada 10% de los pasos o el último
                if (i+1) % max(1, n_pasos // 10) == 0 or i == n_pasos - 1:
                    line = f"{i+1:<8}{t[i+1]:<12.4f}"
                    for j in range(n):
                        line += f"{y_vals[i+1][j]:<15.8f}"
                    self.print_output(line)
            
            self.print_output(f"\n✓ Sistema resuelto exitosamente:", '#00ff00')
            for i in range(n):
                self.print_output(f"  y[{i}]({tf}) ≈ {y_vals[-1][i]:.10f}", '#00ff00')
            self.print_output(f"  Pasos totales: {n_pasos}", '#00ff00')
            self.print_output(f"  Método: Euler (orden 1)", '#00ff00')
            
            # Mostrar gráfica
            self.mostrar_grafica_sistema(t, y_vals, n)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")

    def mostrar_grafica_sistema(self, t, y, n):
        """Muestra la gráfica del sistema de EDO"""
        top = tk.Toplevel(self.root)
        top.title("Gráfica - Sistema de EDO (Euler)")
        top.geometry("1000x600")
        
        # Determinar configuración de subplots
        if n <= 2:
            rows, cols = 1, n + 1
            figsize = (15, 5)
        elif n <= 4:
            rows, cols = 2, 2
            figsize = (12, 10)
        else:
            rows = (n + 2) // 3
            cols = 3
            figsize = (15, 5*rows)
        
        fig = Figure(figsize=figsize, dpi=100)
        
        colors = ['b', 'r', 'g', 'm', 'c', 'y', 'k', 'orange', 'purple', 'brown']
        
        # Gráficas individuales
        for i in range(n):
            ax = fig.add_subplot(rows, cols, i+1)
            ax.plot(t, y[:, i], colors[i % len(colors)] + '-', 
                linewidth=2, label=f'y[{i}](t)')
            ax.set_xlabel('t', fontsize=11)
            ax.set_ylabel(f'y[{i}]', fontsize=11)
            ax.set_title(f'Solución y[{i}](t) - Euler', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
        
        # Si hay 2 variables, añadir plano de fase
        if n == 2:
            ax = fig.add_subplot(rows, cols, n+1)
            ax.plot(y[:, 0], y[:, 1], 'k-', linewidth=2)
            ax.plot(y[0, 0], y[0, 1], 'go', markersize=10, label='Inicio')
            ax.plot(y[-1, 0], y[-1, 1], 'ro', markersize=10, label='Final')
            ax.set_xlabel('y[0]', fontsize=11)
            ax.set_ylabel('y[1]', fontsize=11)
            ax.set_title('Plano de Fase', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
        elif n == 3:
            try:
                from mpl_toolkits.mplot3d import Axes3D
                ax = fig.add_subplot(rows, cols, n+1, projection='3d')
                ax.plot(y[:, 0], y[:, 1], y[:, 2], 'k-', linewidth=2)
                ax.scatter(y[0, 0], y[0, 1], y[0, 2], c='g', s=100, label='Inicio')
                ax.scatter(y[-1, 0], y[-1, 1], y[-1, 2], c='r', s=100, label='Final')
                ax.set_xlabel('y[0]', fontsize=10)
                ax.set_ylabel('y[1]', fontsize=10)
                ax.set_zlabel('y[2]', fontsize=10)
                ax.set_title('Espacio de Fase 3D', fontsize=12)
                ax.legend(fontsize=9)
            except:
                pass
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        
        # ============ MÉTODO 2: JACOBI ============
    def jacobi_ui(self):
        self.clear_input_frame()
        self.clear_output()
        self.print_output("=== MÉTODO DE JACOBI ===\n", '#00ffff')
        
        self.input_fields['n'] = self.create_entry_field("Número de ecuaciones:", 0, "3")
        
        btn = tk.Button(self.input_frame, text="Continuar", command=self.jacobi_matriz_ui,
                        bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20)
        btn.grid(row=1, column=0, columnspan=2, pady=20)
        
        self.current_entry = self.input_fields['n']
        self.input_fields['n'].focus()

    def jacobi_matriz_ui(self):
        try:
            n = int(self.input_fields['n'].get())
            self.n_jacobi = n  # Guardar n como atributo
            self.clear_input_frame()
            
            # Crear campos para la matriz A
            tk.Label(self.input_frame, text="Matriz A (separar por espacios):", 
                    bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                    row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
            
            self.input_fields['A'] = []
            defaults = ["4 1 0", "1 4 1", "0 1 4"]
            for i in range(n):
                default_val = defaults[i] if i < len(defaults) else " ".join(["1" if j == i else "0" for j in range(n)])
                entry = self.create_entry_field(f"Fila {i+1}:", i+1, default_val)
                self.input_fields['A'].append(entry)
            
            # Vector b
            tk.Label(self.input_frame, text="Vector b:", 
                    bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                    row=n+1, column=0, columnspan=2, pady=5, sticky='w', padx=5)
            
            self.input_fields['b'] = self.create_entry_field("b (separar por espacios):", n+2, "6 6 6")
            
            # Parámetros
            self.input_fields['tol'] = self.create_entry_field("Tolerancia:", n+3, "0.0001")
            self.input_fields['max_iter'] = self.create_entry_field("Máx. iteraciones:", n+4, "50")
            
            btn = tk.Button(self.input_frame, text="Calcular", command=self.calcular_jacobi,
                            bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
            btn.grid(row=n+5, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calcular_jacobi(self):
        try:
            n = self.n_jacobi  # Usar el atributo guardado
            
            # Leer matriz A
            A = np.zeros((n, n))
            for i in range(n):
                row_values = list(map(float, self.input_fields['A'][i].get().split()))
                if len(row_values) != n:
                    raise ValueError(f"La fila {i+1} debe tener {n} valores")
                A[i] = row_values
            
            # Leer vector b
            b_values = list(map(float, self.input_fields['b'].get().split()))
            if len(b_values) != n:
                raise ValueError(f"El vector b debe tener {n} valores")
            b = np.array(b_values)
            
            tol = float(self.input_fields['tol'].get())
            max_iter = int(self.input_fields['max_iter'].get())
            
            self.clear_output()
            self.print_output("=== RESULTADOS ===\n", '#00ffff')
            
            # Verificar diagonal dominante
            diag_dom = True
            for i in range(n):
                if abs(A[i][i]) < sum(abs(A[i][j]) for j in range(n) if j != i):
                    diag_dom = False
            
            if not diag_dom:
                self.print_output("⚠ La matriz NO es diagonalmente dominante", '#ff0000')
                self.print_output("  La convergencia no está garantizada\n", '#ff0000')
            
            # Encabezado
            header = f"{'Iter':<8}"
            for i in range(n):
                header += f"{'x'+str(i+1):<15}"
            header += f"{'Error':<15}"
            self.print_output(header, '#ffff00')
            self.print_output("-"*(8 + 15*n + 15), '#ffff00')
            
            x = np.zeros(n)
            for k in range(max_iter):
                x_nuevo = np.zeros(n)
                
                for i in range(n):
                    suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
                    x_nuevo[i] = (b[i] - suma) / A[i][i]
                
                error = np.linalg.norm(x_nuevo - x, np.inf)
                
                line = f"{k:<8}"
                for val in x_nuevo:
                    line += f"{val:<15.8f}"
                line += f"{error:<15.2e}"
                self.print_output(line)
                
                if error < tol:
                    self.print_output(f"\n✓ Solución encontrada:", '#00ff00')
                    for i in range(n):
                        self.print_output(f"  x{i+1} = {x_nuevo[i]:.10f}", '#00ff00')
                    return
                
                x = x_nuevo.copy()
            
            self.print_output(f"\n⚠ No convergió en {max_iter} iteraciones", '#ff0000')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")

    # ============ MÉTODO 3: INTERPOLACIÓN ============
    # ============ MÉTODO 3: INTERPOLACIÓN DE LAGRANGE MULTIVARIABLE ============
    def interpolacion_ui(self):
        self.clear_input_frame()
        self.clear_output()
        self.print_output("=== INTERPOLACIÓN DE LAGRANGE MULTIVARIABLE ===\n", '#00ffff')
        self.print_output("Interpolación en 1D, 2D o 3D usando polinomios de Lagrange\n", '#ffff00')
        
        self.input_fields['n_vars'] = self.create_entry_field("Número de variables (1, 2 o 3):", 0, "1")
        
        btn = tk.Button(self.input_frame, text="Continuar", command=self.interpolacion_config_ui,
                    bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20)
        btn.grid(row=1, column=0, columnspan=2, pady=20)
        
        self.current_entry = self.input_fields['n_vars']
        self.input_fields['n_vars'].focus()

    def interpolacion_config_ui(self):
        try:
            n_vars = int(self.input_fields['n_vars'].get())
            
            if n_vars not in [1, 2, 3]:
                messagebox.showerror("Error", "Solo se soportan 1, 2 o 3 variables")
                return
            
            self.n_vars_interp = n_vars
            self.clear_input_frame()
            
            if n_vars == 1:
                # Interpolación 1D: z = f(x)
                tk.Label(self.input_frame, text="Interpolación 1D: z = f(x)", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['n_puntos'] = self.create_entry_field("Número de puntos:", 1, "4")
                
            elif n_vars == 2:
                # Interpolación 2D: z = f(x, y)
                tk.Label(self.input_frame, text="Interpolación 2D: z = f(x, y)", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['n_puntos_x'] = self.create_entry_field("Puntos en dirección x:", 1, "3")
                self.input_fields['n_puntos_y'] = self.create_entry_field("Puntos en dirección y:", 2, "3")
                
            else:  # n_vars == 3
                # Interpolación 3D: w = f(x, y, z)
                tk.Label(self.input_frame, text="Interpolación 3D: w = f(x, y, z)", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['n_puntos_x'] = self.create_entry_field("Puntos en dirección x:", 1, "2")
                self.input_fields['n_puntos_y'] = self.create_entry_field("Puntos en dirección y:", 2, "2")
                self.input_fields['n_puntos_z'] = self.create_entry_field("Puntos en dirección z:", 3, "2")
            
            btn = tk.Button(self.input_frame, text="Ingresar Datos", command=self.interpolacion_datos_ui,
                        bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20)
            
            if n_vars == 1:
                btn.grid(row=2, column=0, columnspan=2, pady=20)
            elif n_vars == 2:
                btn.grid(row=3, column=0, columnspan=2, pady=20)
            else:
                btn.grid(row=4, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def interpolacion_datos_ui(self):
        try:
            n_vars = self.n_vars_interp
            
            # ======================= 1D =======================
            if n_vars == 1:
                #  Leer antes de limpiar
                n = int(self.input_fields['n_puntos'].get())
                self.n_interp_1d = n
                
                #  Limpiar después de leer
                self.clear_input_frame()
                
                tk.Label(self.input_frame, text="Ingrese los puntos (x, z):", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['x_vals'] = []
                self.input_fields['z_vals'] = []
                
                for i in range(n):
                    x_entry = self.create_entry_field(f"x[{i}]:", 2*i+1, str(i))
                    z_entry = self.create_entry_field(f"z[{i}]:", 2*i+2, str(i**2))
                    self.input_fields['x_vals'].append(x_entry)
                    self.input_fields['z_vals'].append(z_entry)
                
                tk.Label(self.input_frame, text="Evaluar el polinomio en:", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=2*n+1, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['eval_x'] = self.create_entry_field("x =", 2*n+2, "1.5")
                
                btn = tk.Button(self.input_frame, text="Calcular Interpolación", 
                            command=self.calcular_interpolacion,
                            bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
                btn.grid(row=2*n+3, column=0, columnspan=2, pady=20)
            
            
            # ======================= 2D =======================
            elif n_vars == 2:
                #  Leer antes de limpiar
                nx = int(self.input_fields['n_puntos_x'].get())
                ny = int(self.input_fields['n_puntos_y'].get())
                self.nx_interp = nx
                self.ny_interp = ny
                
                #  Limpiar después de leer
                self.clear_input_frame()
                
                tk.Label(self.input_frame, text=f"Ingrese los valores ({nx}x{ny} puntos):", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['x_vals'] = self.create_entry_field(
                    "Valores de x (separados por espacio):", 1, " ".join(str(i) for i in range(nx)))
                
                self.input_fields['y_vals'] = self.create_entry_field(
                    "Valores de y (separados por espacio):", 2, " ".join(str(i) for i in range(ny)))
                
                tk.Label(self.input_frame, text="Matriz Z = f(x, y):", 
                        bg='#2b2b2b', fg='#ffff00', font=('Arial', 10, 'bold')).grid(
                        row=3, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['z_matrix'] = []
                for i in range(ny):
                    z_row = self.create_entry_field(f"Z[{i},:] =", 4+i, 
                                                    " ".join(str(i+j) for j in range(nx)))
                    self.input_fields['z_matrix'].append(z_row)
                
                tk.Label(self.input_frame, text="Evaluar en:", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=4+ny, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['eval_x'] = self.create_entry_field("x =", 5+ny, "0.5")
                self.input_fields['eval_y'] = self.create_entry_field("y =", 6+ny, "0.5")
                
                btn = tk.Button(self.input_frame, text="Calcular Interpolación", 
                            command=self.calcular_interpolacion,
                            bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
                btn.grid(row=7+ny, column=0, columnspan=2, pady=20)
            
            
            # ======================= 3D =======================
            else:  # n_vars == 3
                #  Leer antes de limpiar
                nx = int(self.input_fields['n_puntos_x'].get())
                ny = int(self.input_fields['n_puntos_y'].get())
                nz = int(self.input_fields['n_puntos_z'].get())
                self.nx_interp = nx
                self.ny_interp = ny
                self.nz_interp = nz
                
                #  Limpiar después de leer
                self.clear_input_frame()
                
                tk.Label(self.input_frame, text=f"Ingrese los valores ({nx}x{ny}x{nz} puntos):", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=0, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['x_vals'] = self.create_entry_field(
                    "Valores de x (separados por espacio):", 1, " ".join(str(i) for i in range(nx)))
                
                self.input_fields['y_vals'] = self.create_entry_field(
                    "Valores de y (separados por espacio):", 2, " ".join(str(i) for i in range(ny)))
                
                self.input_fields['z_vals'] = self.create_entry_field(
                    "Valores de z (separados por espacio):", 3, " ".join(str(i) for i in range(nz)))
                
                tk.Label(self.input_frame, text="Tensor W = f(x, y, z):", 
                        bg='#2b2b2b', fg='#ffff00', font=('Arial', 10, 'bold')).grid(
                        row=4, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                tk.Label(self.input_frame, text="Ingrese capa por capa (matrices separadas):", 
                        bg='#2b2b2b', fg='#ffff00', font=('Arial', 9, 'italic')).grid(
                        row=5, column=0, columnspan=2, pady=2, sticky='w', padx=5)
                
                self.input_fields['w_tensor'] = []
                row_counter = 6
                for k in range(nz):
                    tk.Label(self.input_frame, text=f"Capa z[{k}]:", 
                            bg='#2b2b2b', fg='#00ff00', font=('Arial', 9, 'bold')).grid(
                            row=row_counter, column=0, columnspan=2, pady=2, sticky='w', padx=5)
                    row_counter += 1
                    
                    layer = []
                    for i in range(ny):
                        w_row = self.create_entry_field(f"W[{k},{i},:] =", row_counter, 
                                                        " ".join(str(k+i+j) for j in range(nx)))
                        layer.append(w_row)
                        row_counter += 1
                    self.input_fields['w_tensor'].append(layer)
                
                tk.Label(self.input_frame, text="Evaluar en:", 
                        bg='#2b2b2b', fg='#00ffff', font=('Arial', 10, 'bold')).grid(
                        row=row_counter, column=0, columnspan=2, pady=5, sticky='w', padx=5)
                
                self.input_fields['eval_x'] = self.create_entry_field("x =", row_counter+1, "0.5")
                self.input_fields['eval_y'] = self.create_entry_field("y =", row_counter+2, "0.5")
                self.input_fields['eval_z'] = self.create_entry_field("z =", row_counter+3, "0.5")
                
                btn = tk.Button(self.input_frame, text="Calcular Interpolación", 
                            command=self.calcular_interpolacion,
                            bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
                btn.grid(row=row_counter+4, column=0, columnspan=2, pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def calcular_interpolacion(self):
        try:
            n_vars = self.n_vars_interp
            
            if n_vars == 1:
                # Interpolación de Lagrange 1D
                n = self.n_interp_1d
                x = np.array([float(self.input_fields['x_vals'][i].get()) for i in range(n)])
                z = np.array([float(self.input_fields['z_vals'][i].get()) for i in range(n)])
                x_eval = float(self.input_fields['eval_x'].get())
                
                self.clear_output()
                self.print_output("=== INTERPOLACIÓN DE LAGRANGE 1D ===\n", '#00ffff')
                
                # Calcular polinomios de Lagrange
                result = 0.0
                self.print_output("Polinomios de Lagrange:", '#ffff00')
                
                for i in range(n):
                    # L_i(x)
                    L_i = 1.0
                    for j in range(n):
                        if i != j:
                            L_i *= (x_eval - x[j]) / (x[i] - x[j])
                    
                    result += z[i] * L_i
                    self.print_output(f"L_{i}({x_eval:.4f}) = {L_i:.6f},  z[{i}]*L_{i} = {z[i]*L_i:.6f}")
                
                self.print_output(f"\n✓ Resultado de la interpolación:", '#00ff00')
                self.print_output(f"  P({x_eval}) ≈ {result:.10f}", '#00ff00')
                
            elif n_vars == 2:
                # Interpolación de Lagrange 2D
                nx = self.nx_interp
                ny = self.ny_interp
                
                x = np.array(list(map(float, self.input_fields['x_vals'].get().split())))
                y = np.array(list(map(float, self.input_fields['y_vals'].get().split())))
                
                Z = np.zeros((ny, nx))
                for i in range(ny):
                    z_row = list(map(float, self.input_fields['z_matrix'][i].get().split()))
                    if len(z_row) != nx:
                        raise ValueError(f"La fila {i} debe tener {nx} valores")
                    Z[i] = z_row
                
                x_eval = float(self.input_fields['eval_x'].get())
                y_eval = float(self.input_fields['eval_y'].get())
                
                self.clear_output()
                self.print_output("=== INTERPOLACIÓN DE LAGRANGE 2D ===\n", '#00ffff')
                
                # Calcular usando producto tensor de polinomios de Lagrange
                result = 0.0
                
                for i in range(ny):
                    for j in range(nx):
                        # L_i(y_eval) * L_j(x_eval)
                        L_y = 1.0
                        for k in range(ny):
                            if k != i:
                                L_y *= (y_eval - y[k]) / (y[i] - y[k])
                        
                        L_x = 1.0
                        for k in range(nx):
                            if k != j:
                                L_x *= (x_eval - x[k]) / (x[j] - x[k])
                        
                        result += Z[i][j] * L_y * L_x
                
                self.print_output(f"Puntos en x: {x}", '#ffff00')
                self.print_output(f"Puntos en y: {y}", '#ffff00')
                self.print_output(f"\nMatriz Z:")
                for i in range(ny):
                    self.print_output(f"  {Z[i]}")
                
                self.print_output(f"\n✓ Resultado de la interpolación:", '#00ff00')
                self.print_output(f"  P({x_eval}, {y_eval}) ≈ {result:.10f}", '#00ff00')
                
            else:  # n_vars == 3
                # Interpolación de Lagrange 3D
                nx = self.nx_interp
                ny = self.ny_interp
                nz = self.nz_interp
                
                x = np.array(list(map(float, self.input_fields['x_vals'].get().split())))
                y = np.array(list(map(float, self.input_fields['y_vals'].get().split())))
                z = np.array(list(map(float, self.input_fields['z_vals'].get().split())))
                
                W = np.zeros((nz, ny, nx))
                for k in range(nz):
                    for i in range(ny):
                        w_row = list(map(float, self.input_fields['w_tensor'][k][i].get().split()))
                        if len(w_row) != nx:
                            raise ValueError(f"La fila [{k},{i}] debe tener {nx} valores")
                        W[k][i] = w_row
                
                x_eval = float(self.input_fields['eval_x'].get())
                y_eval = float(self.input_fields['eval_y'].get())
                z_eval = float(self.input_fields['eval_z'].get())
                
                self.clear_output()
                self.print_output("=== INTERPOLACIÓN DE LAGRANGE 3D ===\n", '#00ffff')
                
                # Calcular usando producto tensor de polinomios de Lagrange
                result = 0.0
                
                for k in range(nz):
                    for i in range(ny):
                        for j in range(nx):
                            # L_k(z_eval) * L_i(y_eval) * L_j(x_eval)
                            L_z = 1.0
                            for m in range(nz):
                                if m != k:
                                    L_z *= (z_eval - z[m]) / (z[k] - z[m])
                            
                            L_y = 1.0
                            for m in range(ny):
                                if m != i:
                                    L_y *= (y_eval - y[m]) / (y[i] - y[m])
                            
                            L_x = 1.0
                            for m in range(nx):
                                if m != j:
                                    L_x *= (x_eval - x[m]) / (x[j] - x[m])
                            
                            result += W[k][i][j] * L_z * L_y * L_x
                
                self.print_output(f"Puntos en x: {x}", '#ffff00')
                self.print_output(f"Puntos en y: {y}", '#ffff00')
                self.print_output(f"Puntos en z: {z}", '#ffff00')
                self.print_output(f"\nTensor W (por capas):")
                for k in range(nz):
                    self.print_output(f"  Capa z[{k}]:", '#00ff00')
                    for i in range(ny):
                        self.print_output(f"    {W[k][i]}")
                
                self.print_output(f"\n✓ Resultado de la interpolación:", '#00ff00')
                self.print_output(f"  P({x_eval}, {y_eval}, {z_eval}) ≈ {result:.10f}", '#00ff00')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")

    # ============ MÉTODO 4: SIMPSON 3/8 ============
    def simpson_ui(self):
        self.clear_input_frame()
        self.clear_output()
        self.print_output("=== REGLA DE SIMPSON 3/8 COMPUESTA ===\n", '#00ffff')
        
        self.input_fields['f'] = self.create_entry_field("f(x) =", 0, "x**2")
        self.input_fields['a'] = self.create_entry_field("Límite inferior a:", 1, "0")
        self.input_fields['b'] = self.create_entry_field("Límite superior b:", 2, "1")
        self.input_fields['n'] = self.create_entry_field("Subintervalos (múltiplo de 3):", 3, "9")
        
        btn = tk.Button(self.input_frame, text="Calcular", command=self.calcular_simpson,
                        bg='#5cb85c', fg='white', font=('Arial', 11, 'bold'), width=20, height=2)
        btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.current_entry = self.input_fields['f']
        self.input_fields['f'].focus()

    def calcular_simpson(self):
        try:
            f_str = self.input_fields['f'].get()
            a = float(self.input_fields['a'].get())
            b = float(self.input_fields['b'].get())
            n = int(self.input_fields['n'].get())
            
            f = lambda x: eval(f_str)
            
            if n % 3 != 0:
                n = ((n + 2) // 3) * 3
            
            h = (b - a) / n
            
            suma = f(a) + f(b)
            for i in range(1, n):
                x_i = a + i * h
                if i % 3 == 0:
                    suma += 2 * f(x_i)
                else:
                    suma += 3 * f(x_i)
            
            integral = (3 * h / 8) * suma
            
            self.clear_output()
            self.print_output("=== RESULTADOS ===\n", '#00ffff')
            self.print_output(f"✓ Integral calculada:", '#00ff00')
            self.print_output(f"  ∫[{a}, {b}] f(x)dx ≈ {integral:.10f}", '#00ff00')
            self.print_output(f"  Subintervalos: {n}", '#00ff00')
            self.print_output(f"  Paso h: {h:.8f}", '#00ff00')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error")

