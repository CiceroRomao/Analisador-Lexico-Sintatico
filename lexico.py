import pandas

class Lexico:
    def __init__(self, file):
        self.file = open(file)
        self.fileAux = file
        self.saida = pandas.DataFrame(columns=["Lexema","Padrão","Token","Linha"])
        self.errosLexicos = pandas.DataFrame(columns=["Lexema","Linha"])
        self.reservedStrings = [
            "boolean",
            "class",
            "extends",  
            "public",
            "static",
            "void",
            "main",
            "String",
            "return",
            "int",
            "if",
            "else",
            "while",
            "System.out.println",
            "length",
            "true",
            "false",
            "this",
            "new"
            ]
        
        self.operators = [
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            ";",
            ".",
            ",",
            "=",
            "<",
            "==",
            "!=",
            "+",
            "-",
            "*",
            "/",
            "&&",
            "!"
            ]
    
    
    #Função para printar resultado
    def executaLexico(self):
        self.mainClass()
        
        #converte o datagrama para arquivo de texto
        
        #self.saida.to_csv(r'Analise Léxica.txt', header=None, index=None, sep=' ', mode='a')
        #self.errosLexicos.to_csv(r'Erros Léxicos.txt', header=None, index=None, sep=' ', mode='a')
        print(self.saida)
        print(self.errosLexicos)
        print(self.operators)
    
    
    def mainClass(self):
        token = ""
        numLinhas = 0
        fechamento = 0
        for line in self.file:
            numLinhas += 1
            i = 0
            if fechamento == 0 or numLinhas > fechamento:
                while i < len(line):
                    aux = i + 1
                    if line[i] != "" and line[i] != " " and line[i] != "\n":
                        token += line[i]
                        if token in self.reservedStrings or token in self.operators:
                            if token in self.reservedStrings:                                 
                                self.insereLinha(token , numLinhas)   
                                token = ""
                            elif token in self.operators:
                                if token == "/":
                                    if line[aux] != "/" and line[aux] != "*":
                                        self.insereLinha(token, numLinhas)
                                        token = ""
                                    elif line[aux] == "/":
                                        self.saida = self.saida.append(
                                        {"Lexema": "//", "Padrão": "Comment", "Token": "<//,"+ str(numLinhas) +">", "Linha": numLinhas},
                                        ignore_index=True)
                                        token = ""
                                        break
                                    elif line[aux] == "*":
                                        self.saida = self.saida.append(
                                        {"Lexema": "/*", "Padrão": "Comment", "Token": "</*,"+ str(numLinhas) +">", "Linha": numLinhas},
                                        ignore_index=True)
                                        fechamento = self.confereFechamento(numLinhas)
                                        token = ""
                                        break     
                                                                                
                                self.insereLinha(token, numLinhas)
                                token = ""
                                
                        elif line[aux] == "" or line[aux] == " " or line[aux] == "\n" or line[aux] in self.operators:                            
                            if line[aux] == "\n":
                                self.insereErro(token, numLinhas)
                                token = ""
                            elif line[aux] in self.operators or line[aux] == "" or line[aux] == " ":
                                self.insereLinha(token, numLinhas)
                                token = ""
                    i += 1    
                 
            
    def confereFechamento(self, numLinha):
        auxFile = open(self.fileAux)
        numLinhasAtual = 0
        for line in auxFile:
            numLinhasAtual += 1
            if numLinhasAtual >= numLinha:
                if "*/" in line:
                    self.saida = self.saida.append(
                    {"Lexema": "*/", "Padrão": "Comment", "Token": "<*/,"+ str(numLinhasAtual) +">", "Linha": numLinhasAtual},
                    ignore_index=True)
                    return(numLinhasAtual)    
        
        return 0
       
    def insereErro(self, aux, cont):
        self.errosLexicos = self.errosLexicos.append(
        {"Lexema": aux, "Linha": cont},
        ignore_index=True)   
                
    #Função para orgnaizar as linhas no Datagrama
    def insereLinha(self, aux, cont):
        token = self.conferirToken(aux, cont)
        padrao = self.conferePadrao(aux)
        self.saida = self.saida.append(
            {"Lexema": aux, "Padrão": padrao, "Token": token, "Linha": cont},
            ignore_index=True)
    
    #Função para conferir se é um numeral ou indentificador
    def conferirToken(self, aux, cont):
        if aux not in self.reservedStrings and aux not in self.operators:
            if str.isdigit(aux):
                return "<Number,"+ str(cont) +">"
            return "<Identifier,"+ str(cont) +">"
        return "<"+ aux +","+ str(cont) +">"

    #Função para conferir se é simbolo da linguagem ou palavra reservada ou numeral
    def conferePadrao(self, aux):
        for r in self.reservedStrings:
            if (r == aux):
                return "ReserverdString"
        for r in self.operators:
            if r == aux:
                return r
        for r in aux:
            if r >= "0" and r <= "9":
                return "Number"
        return "Identifier"

    

    #função para fechar arquivo aberto
    def close(self):
        self.file.close()
        
        
