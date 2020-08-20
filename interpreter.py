class Interpreter:
    variables = {
        '샌즈이긴횟수': 0,
        '인디게임': ''
    }
    funcs = {
        
    }

    def run(self, text: str) -> bool:
        text = text.split('\n')
        for line in text: 
            try: res = self.run_line(line)
            except Exception as e: 
                print(e)
                raise self.SyntaxError
            if res != '키키': return res
        return '키키'

    def run_line(self, line):
        cmd = line.split(' ')[0]
        line = list(line)
        del line[0:len(cmd) + 1]
        line = ''.join(line)
        if cmd == '와!':
            if line[0] != '{': raise self.SyntaxError('Need an Variable')
            b = line[1:line.rindex('}')]
            line = list(line)
            del line[0:''.join(line).rindex('}') + 1]
            line = ''.join(line)
            c = self.get_string(line)
            self.variables[b] = c
        elif cmd == '샌즈':
            print(self.get_string(line), end = '')
        elif cmd == '파피루스':
            c = input()
            if line[0] != '{': raise self.SyntaxError('Need an Variable')
            b = line[1:line.rindex('}')]
            line = list(line)
            del line[1:''.join(line).rindex('}') + 1]
            line = ''.join(line)
            self.variables[b] = c
        elif cmd == '않임?':
            do = str(line.split('면')[1][1:]).replace(' 헐 ', '\n')
            line = line.split('면')[0]
            first = line.split('가')[0] 
            second = line.split('가')[1]
            if self.get_string(first) == self.get_string(second): self.run(do)
        elif cmd == '머멍이':
            do = str(line.split('동안')[1][1:]).replace(' 헐 ', '\n')
            whilel = int(self.get_string(line.split('동안')[0]))
            for _ in range(whilel): 
                self.run(do)
                self.variables['샌즈이긴횟수'] += 1
        elif cmd == '토비폭스': 
            if line[0] != '<': raise self.SyntaxError('Need an FUNCTION')
            b = line[1:line.rindex('>')]
            line = list(line)
            del line[0:''.join(line).rindex('>') + 1]
            line = ''.join(line)
            self.funcs[b] = line[1:]
        if cmd == '샌즈더스켈레톤': return self.get_string(line)
        else: return '키키'
    def get_string(self, string):
        if len(string) < 2: raise self.NotaString
        stri = string
        inmunjayer = 0 
        while stri:
            if stri[0] in ['(', '{']: inmunjayer += 1
            if stri[0] in [')', '}']: inmunjayer -= 1
            if stri[0] == ' ' and not inmunjayer: 
                stri = list(stri)
                del stri[0]
                stri = ''.join(stri)
            stri = list(stri)
            del stri[0]
            stri = ''.join(stri)
        a = ''
        while string:
            b = string[0]
            if b == '{':
                c = string[1:string.rindex('}')]
                string = list(string)
                del string[1:''.join(string).rindex('}') + 1]
                string = ''.join(string)
                if c not in self.variables.keys(): raise self.NoVariable(c)
                a += str(self.variables[c])
            elif b == '(':
                c = string[1:string.rindex(')')]
                string = list(string)
                del string[1:''.join(string).rindex(')') + 1]
                string = ''.join(string)
                a += str(c)
            elif b == '[':
                c = string[1:string.rindex(']')]
                string = list(string)
                del string[1:''.join(string).rindex(']') + 1]
                string = ''.join(string)
                if c not in self.variables.keys(): raise self.NoVariable(c)
                a += str(len(str(self.variables[c])))
            elif b == '<':
                c = string[1:string.rindex('>')]
                string = list(string)
                del string[1:''.join(string).rindex('>') + 1]
                string = ''.join(string)
                res = self.run(str(self.funcs[c]).replace(' 헐 ', '\n'))
                a += res
            string = list(string)
            del string[0]
            string = ''.join(string)
        return str(a).replace(' 헐 ', '\n')

    class NotaString(Exception): 
        def __init__(self): super().__init__('Not A string')
    
    class NoVariable(Exception): 
        def __init__(self, name: str):
            self.name = str(name)
            super().__init__(f'Variable {name} Not Exist')
    
    class SyntaxError(Exception): pass
