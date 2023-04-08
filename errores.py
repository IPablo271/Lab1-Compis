import re

filename = "ejemplo2.yal"

# patrón regex para validar definiciones de expresiones regulares
regex_def = re.compile(r"let\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*\[.*?\]")

# patrón regex para validar reglas con nombre
regex_rule_with_name = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\[.*?\]")

# patrón regex para validar reglas sin nombre
regex_rule_without_name = re.compile(r"\[.*?\]")

# contador de errores
error_count = 0

with open(filename, "r") as f:
    for line_num, line in enumerate(f, start=1):
        # elimina comentarios
        line = line.split("#")[0].strip()

        if not line:
            continue  # salta líneas vacías

        # busca definiciones de expresiones regulares
        if line.startswith("let"):
            if not regex_def.match(line):
                print(f"Error en línea {line_num}: Definición de expresión regular inválida")
                error_count += 1

        # busca reglas con nombre
        elif "[" in line and "]" in line:
            match = regex_rule_with_name.search(line)
            if match:
                rule_name = match.group(1)
                if not match.group().endswith("{"):
                    print(f"Error en línea {line_num}: Cuerpo de la regla '{rule_name}' no encontrado")
                    error_count += 1
            else:
                print(f"Error en línea {line_num}: Regla inválida")
                error_count += 1

        # busca reglas sin nombre
        elif "[" in line or "]" in line:
            print(f"Error en línea {line_num}: Regla inválida")
            error_count += 1

print(f"Se encontraron {error_count} errores en el archivo.")