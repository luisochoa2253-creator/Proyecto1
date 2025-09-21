# LRParserLoader.py
# Esta clase lee el archivo .lr y carga la gramática y las tablas en memoria.

class LRParserLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.grammar = []
        self.action_table = []
        self.goto_table = []
        self.num_terminals = 0

    def load(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        # 1. Leer número de reglas
        num_rules = int(lines[0].strip())
        
        # 2. Leer las reglas de la gramática
        rule_lines = lines[1:num_rules + 1]
        for line in rule_lines:
            parts = line.strip().split()
            lhs = int(parts[0])
            rhs_len = int(parts[1])
            self.grammar.append({'lhs': lhs, 'rhs_len': rhs_len})

        # 3. Leer dimensiones de la tabla
        dims_line = lines[num_rules + 1].strip().split()
        num_states = int(dims_line[0])
        num_symbols = int(dims_line[1])
        
        # Asumimos que los no-terminales son del 24 al 45.
        # (45 - 24 + 1) = 22 no-terminales
        num_non_terminals = 22 
        self.num_terminals = num_symbols - num_non_terminals
        
        # 4. Leer los datos de la tabla
        table_lines = lines[num_rules + 2:]
        full_table = []
        for line in table_lines:
            if line.strip():
                full_table.append([int(x) for x in line.strip().split()])

        # 5. Separar en tabla ACTION y GOTO
        for row in full_table:
            self.action_table.append(row[:self.num_terminals])
            self.goto_table.append(row[self.num_terminals:])
            
        return self.grammar, self.action_table, self.goto_table