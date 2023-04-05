import re

class Yalex:
    def __init__(self, filename):
        self.filename = filename
        self.lines = self._read_file()
        self.tokens = {}
        self.regex_dict = {}
        self.identDict = {}
        self.regex_list = []
        self.getRegexes()
        self.regexlist_final = []
        self.regexfinal = None
        

    def _read_file(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        return lines
    
    def getRegexes(self):

        pattern = r"let\s+(\w+)\s*=\s*(.*)"

        for i, line in enumerate(self.lines):
            match = re.match(pattern, line)
            if match:
                self.regex_dict[match.group(1)] = match.group(2)
            if line.startswith("rule"):
                for j,sub_line in enumerate(self.lines[i+1:]):
                      # Remove comments enclosed in '(**)'
                    # sub_line = re.sub(r'\(\*.*?\*\)', '', sub_line)
                    sub_line = sub_line.lstrip()

                    if sub_line.startswith("(*") and re.search(r"\*\)$", sub_line):
                        continue  # skip to next iteration if line is a comment
                    
                    # check if the line has curly braces '{}'
                    if "{" in sub_line and "}" in sub_line:
                        # extract the content inside the curly braces
                        brace_content = re.search(r'\{(.+?)\}', sub_line).group(1)
                        # use the content inside the braces as the key in the dictionary
                        self.identDict[brace_content] = ""
                        # remove the content inside the braces from the line
                        sub_line = re.sub(r'\{.*?\}', '', sub_line)
                    
                    regex = ""
                     # Remove comments enclosed in '(**)'
                    sub_line = re.sub(r'\(\*.*?\*\)', '', sub_line)
                    if j == 0:
                        # Remove actions enclosed in '{}'
                        sub_line = re.sub(r'\{.*?\}', '', sub_line)
                        if sub_line.startswith("|"):
                            sub_line = sub_line[1:].lstrip()
                        regex += sub_line
                        self.regex_list.append(regex.strip())
                        if brace_content:
                            self.identDict[brace_content] = regex.strip()
                            brace_content = None
                    else:
                        if sub_line.startswith("|"):
                            # Remove actions enclosed in '{}'
                            sub_line = re.sub(r'\{.*?\}', '', sub_line)
                            regex += sub_line.strip()[1:]
                            self.regex_list.append(regex.strip())
                            # print(f"Found regex: {regex}")
                            if brace_content:
                                self.identDict[brace_content] = regex.strip()
                                brace_content = None
                        else:
                            break

        # print("\nDICCIONARIO IDENT - Identificacion de los tokens:")
        # print(self.identDict)
        

        self.regex_list = [x.replace(' ', '') for x in self.regex_list]
        print("\nPRIMERA LISTA - Regexes Originales:")
        print(self.regex_list)
        print("\nDICCIONARIO IDENT - Regexes Original")
        print(self.identDict)

        for key in reversed(list(self.regex_dict.keys())):
            value = self.regex_dict[key]
            for inner_key, inner_value in self.regex_dict.items():
                if inner_key in value:
                    value = value.replace(inner_key, inner_value)
            self.regex_dict[key] = value
        

        
        
        for i in range(len(self.regex_list)):
            for key in self.regex_dict.keys():
                list2 = self.regex_list[i].split(" ")
                for j in range(len(list2)):
                    if key in list2[j]:
                        list2[j] = list2[j].replace(key, self.regex_dict[key])
        
        for key, value in self.regex_dict.items():
            self.regex_dict[key] = value.replace("'", "")  # Reemplazar todas las comillas dentro del valor
        
        for key, value in self.regex_dict.items():
            if '.' in value:
                self.regex_dict[key] = value.replace(".", ",") 
        
        
        for key, value in self.regex_dict.items():
            self.regex_dict[key] = re.sub(r'\[0-9\]', '(0|1|2|3|4|5|6|7|8|9)', self.regex_dict[key])
            self.regex_dict[key] = re.sub(r'\[a-z\]', '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)', self.regex_dict[key])
            self.regex_dict[key] = re.sub(r"\[a-zA-Z\]", '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)', self.regex_dict[key])
            self.regex_dict[key] = re.sub(r'\[ \\t\\n\]', '( |\t|\n)', self.regex_dict[key])
            
        

        lista = []
        for key, value in self.regex_dict.items():
            lista.append(value)
        
    
        self.regexlist_final = lista
        print(self.regexlist_final)
        resultado = ""
        for i in range(len(lista)):
            resultado += lista[i]
            if i != len(lista) - 1:
                resultado += "|"

        print(resultado)

