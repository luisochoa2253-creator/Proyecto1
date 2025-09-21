# gui_parser.py
import sys
import re
import tkinter as tk
from tkinter import scrolledtext, font, Frame, Label

# ===================================================================
# PARTE 1: MAPA DE TOKENS (antes en token_map.py)
# ===================================================================
TOKEN_EOF_ID = 23
TOKEN_MAP = {
    'if': 18, 'else': 22, 'while': 19, 'return': 20, 'int': 4, 'float': 4, 'void': 4,
    ';': 12, ',': 13, '(': 14, ')': 15, '{': 16, '}': 17, '=': 8, '+': 5, '-': 5,
    '*': 6, '/': 6, '<': 7, '>': 7, '<=': 7, '>=': 7, '==': 10, '!=': 10,
    '&&': 11, '||': 9, 'id': 0, 'entero': 2, 'flotante': 3, 'cadena': 1,
}
NON_TERMINAL_MAP = {
    24: 'programa', 25: 'Definiciones', 26: 'Definicion', 27: 'DefVar',
    28: 'ListaVar', 29: 'DefFunc', 30: 'Parametros', 31: 'ListaParam',
    32: 'BloqFunc', 33: 'DefLocales', 34: 'DefLocal', 35: 'Sentencias',
    36: 'Sentencia', 37: 'Otro', 38: 'Bloque', 39: 'ValorRegresa',
    40: 'Argumentos', 41: 'ListaArgumentos', 42: 'Termino', 43: 'LlamadaFunc',
    44: 'SentenciaBloque', 45: 'Expresion'
}

# ===================================================================
# PARTE 2: CLASES DE LÓGICA (Loader, Lexer, Parser)
# ===================================================================

class LRParserLoader:
    # ... (Clase exactamente igual que antes) ...
    def __init__(self, filepath):
        self.filepath = filepath
        self.grammar = []
        self.action_table = []
        self.goto_table = []
    def load(self):
        with open(self.filepath, 'r') as f: lines = f.readlines()
        num_rules = int(lines[0].strip())
        rule_lines = lines[1:num_rules + 1]
        for line in rule_lines:
            parts = line.strip().split()
            self.grammar.append({'lhs': int(parts[0]), 'rhs_len': int(parts[1])})
        dims_line = lines[num_rules + 1].strip().split()
        num_symbols = int(dims_line[1])
        num_non_terminals = len(NON_TERMINAL_MAP)
        num_terminals = num_symbols - num_non_terminals
        table_lines = lines[num_rules + 2:]
        full_table = []
        for line in table_lines:
            if line.strip(): full_table.append([int(x) for x in line.strip().split()])
        for row in full_table:
            self.action_table.append(row[:num_terminals])
            self.goto_table.append(row[num_terminals:])
        return self.grammar, self.action_table, self.goto_table

class Token:
    def __init__(self, tipo_id, lexema):
        self.tipo_id = tipo_id
        self.lexema = lexema

class Lexer:
    # ... (Clase exactamente igual que antes) ...
    def __init__(self, source_code):
        self.source_code = source_code
        token_regex = [
            ('flotante', r'\d+\.\d+'), ('entero',   r'\d+'), ('cadena',   r'\".*?\"'),
            ('id', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('op', r'<=|>=|==|!=|&&|\|\||[;,\(\)\{\}\=\+\-\*\/<>]'),
        ]
        self.regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_regex))
    def get_tokens(self):
        tokens_buffer = []
        for match in self.regex.finditer(self.source_code):
            kind, lexema = match.lastgroup, match.group()
            if kind == 'id' and lexema in TOKEN_MAP: tokens_buffer.append(Token(TOKEN_MAP[lexema], lexema))
            elif kind == 'op' and lexema in TOKEN_MAP: tokens_buffer.append(Token(TOKEN_MAP[lexema], lexema))
            else: tokens_buffer.append(Token(TOKEN_MAP[kind], lexema))
        tokens_buffer.append(Token(TOKEN_EOF_ID, '$'))
        return tokens_buffer

class Parser:
    def __init__(self, grammar, action_table, goto_table):
        self.grammar = grammar
        self.action_table = action_table
        self.goto_table = goto_table
        self.pila = [0]

    def analizar(self, tokens):
        """ MÉTODO MODIFICADO: Ahora es un generador que usa 'yield'. """
        token_idx = 0
        while True:
            estado_actual = self.pila[-1]
            token_actual = tokens[token_idx]
            
            pila_str = " ".join(map(str, self.pila))
            entrada_str = " ".join(t.lexema for t in tokens[token_idx:])
            
            accion = self.action_table[estado_actual][token_actual.tipo_id]
            
            if accion == 0:
                accion_str = f"Error de sintaxis con token '{token_actual.lexema}'"
                yield {"pila": pila_str, "entrada": entrada_str, "accion": accion_str, "error": True}
                return

            if accion > 0: # SHIFT
                accion_str = f"Desplazar a estado {accion}"
                yield {"pila": pila_str, "entrada": entrada_str, "accion": accion_str}
                self.pila.append(token_actual.lexema)
                self.pila.append(accion)
                token_idx += 1
            elif accion < 0: # REDUCE
                num_regla = -accion - 1
                regla = self.grammar[num_regla]
                lhs_id, rhs_len = regla['lhs'], regla['rhs_len']
                lhs_name = NON_TERMINAL_MAP.get(lhs_id, f"NT_{lhs_id}")
                accion_str = f"Reducir por regla {num_regla}: {lhs_name} -> ..."
                yield {"pila": pila_str, "entrada": entrada_str, "accion": accion_str}
                
                num_a_sacar = 2 * rhs_len
                if len(self.pila) < num_a_sacar:
                    yield {"pila": pila_str, "entrada": entrada_str, "accion": f"Error Crítico: Pila insuficiente para R{num_regla}", "error": True}
                    return

                for _ in range(num_a_sacar): self.pila.pop()
                
                estado_anterior = self.pila[-1]
                self.pila.append(lhs_name)
                
                goto_idx = lhs_id - min(NON_TERMINAL_MAP.keys())
                nuevo_estado = self.goto_table[estado_anterior][goto_idx]
                self.pila.append(nuevo_estado)

                if num_regla == 0:
                    pila_str = " ".join(map(str, self.pila))
                    entrada_str = " ".join(t.lexema for t in tokens[token_idx:])
                    yield {"pila": pila_str, "entrada": entrada_str, "accion": "Aceptar"}
                    return

# ===================================================================
# PARTE 3: INTERFAZ GRÁFICA (GUI)
# ===================================================================

class ParserGUI(tk.Tk):
    def __init__(self, grammar, action_table, goto_table):
        super().__init__()
        self.parser_logic = Parser(grammar, action_table, goto_table)
        self.parser_generator = None
        
        self.title("Visualizador de Análisis Sintáctico LR")
        self.geometry("1000x800")

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto para el código
        self.source_text = scrolledtext.ScrolledText(main_frame, height=12, font=("Courier New", 12))
        self.source_text.pack(fill=tk.X, pady=(0, 10))
        self.source_text.insert(tk.END, "int variable;\n\nint main() {\n  return 0;\n}")

        # Botón de análisis
        analyze_button = tk.Button(self, text="▶ Iniciar Análisis Animado", font=("Arial", 12, "bold"), command=self.start_analysis)
        analyze_button.pack(fill=tk.X, padx=10, pady=5)

        # Área de resultados con cabeceras
        results_frame = Frame(main_frame, relief="sunken", borderwidth=1)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        header_font = font.Font(family="Courier New", size=11, weight="bold")
        Label(results_frame, text="PILA", font=header_font, anchor='w').grid(row=0, column=0, sticky='w', padx=5)
        Label(results_frame, text="ENTRADA", font=header_font, anchor='w').grid(row=0, column=1, sticky='w', padx=5)
        Label(results_frame, text="SALIDA", font=header_font, anchor='w').grid(row=0, column=2, sticky='w', padx=5)
        results_frame.grid_columnconfigure(0, weight=3)
        results_frame.grid_columnconfigure(1, weight=2)
        results_frame.grid_columnconfigure(2, weight=2)
        
        self.output_frame = results_frame # Guardamos referencia para añadir filas

    def start_analysis(self):
        # Limpiar resultados anteriores
        for widget in self.output_frame.winfo_children():
            if widget.grid_info()['row'] > 0: # No borrar las cabeceras
                widget.destroy()

        source_code = self.source_text.get("1.0", tk.END)
        lexer = Lexer(source_code)
        tokens = lexer.get_tokens()
        
        # Reiniciar parser y obtener el generador
        self.parser_logic.pila = [0]
        self.parser_generator = self.parser_logic.analizar(tokens)
        
        # Iniciar la animación
        self.update_step()

    def update_step(self):
        try:
            # Pedir el siguiente paso al parser
            paso = next(self.parser_generator)
            
            # Crear y añadir una nueva fila a la tabla de resultados
            row_index = self.output_frame.grid_size()[1]
            font_color = "red" if paso.get("error") else "black"
            
            pila_label = Label(self.output_frame, text=paso["pila"], font=("Courier New", 10), anchor='w', fg=font_color)
            pila_label.grid(row=row_index, column=0, sticky='w', padx=5)
            
            entrada_label = Label(self.output_frame, text=paso["entrada"], font=("Courier New", 10), anchor='w', fg=font_color)
            entrada_label.grid(row=row_index, column=1, sticky='w', padx=5)
            
            accion_label = Label(self.output_frame, text=paso["accion"], font=("Courier New", 10), anchor='w', fg=font_color)
            accion_label.grid(row=row_index, column=2, sticky='w', padx=5)
            
            # Si el paso no es el final (aceptar o error), programar el siguiente
            if paso.get("error") or paso["accion"] == "Aceptar":
                if paso["accion"] == "Aceptar":
                    accion_label.config(fg="green", font=("Courier New", 10, "bold"))
                return # Detener animación
            
            self.after(350, self.update_step) # Espera 350ms para el siguiente paso

        except StopIteration:
            # El generador terminó sin llegar a "Aceptar" o "Error"
            pass

# ===================================================================
# PARTE 4: EJECUCIÓN DEL PROGRAMA
# ===================================================================

if __name__ == "__main__":
    try:
        # Cargar las tablas desde el archivo .lr
        loader = LRParserLoader('compilador.lr')
        grammar, action_table, goto_table = loader.load()
        
        # Iniciar la aplicación gráfica
        app = ParserGUI(grammar, action_table, goto_table)
        app.mainloop()

    except FileNotFoundError:
        print("Error: No se encontró el archivo 'compilador.lr'.")
        print("Asegúrate de que el archivo esté en la misma carpeta que este script.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")