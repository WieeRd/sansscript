from re import (
    compile,
    Pattern
)

NUMFOR = '샌즈이긴횟수'
NORETURN = '키키'
SET = '와!'
PRINT = '샌즈'
INPUT = '파피루스'
IF = '않임?'
FOR = '머멍이'
FUN = '토비폭스'
REQUIRE = '언더테일'
RETURN = '끝'
NL = ' 헐 '
IS = '면'
THIS = '가'
WHILE = '동안'
FILETYPE = 'sansscript'

varreg = compile(r'\{.+?\}')
funcreg = compile(r'<.+?>')

stringreg = compile(r'((\(.+?\))|(\{.+?\})|(\[.+?\])|(<.+?>)|(/.+?\\))+')
eachstrreg = compile(r'(\(.+?\))|(\{.+?\})|(\[.+?\])|(<.+?>)|(/.+?\\)')
expressionreg = compile(r'-?[0-9]+(\+|\-|\*|\%|\^|\|)-?[0-9]+')
findnumreg = compile(r'-?[0-9]+')
findsignreg = compile(r'\+|\-|\*|\%|\^|\|')

setreg = compile(r'\{.+?\} ((\(.+?\))|(\{.+?\})|(\[.+?\])|(<.+?>)|(/.+?\\))+')
ifreg = compile(r'((\(.+?\))|(\{.+?\})|(\[.+?\])|(<.+?>)|(/.+?\\))+' + THIS + r'((\(.+?\))|(\{.+?\})|(\[.+?\])|(<.+?>)|(/.+?\\))+' + IS + r' .+?')
forreg = compile(r'((\(.+?\))|(\{.+?\})|(\[.+?\])|(<.+?>)|(/.+?\\))+' + WHILE + r' .+?')
funreg = compile(r'<.+?> .+?')
returnreg = compile(r'((\(.+?\))|(\{.+?\})|(\[.+?\])|(<.+?>)|(/.+?\\))+')
requirereg = compile(r'.+?\.' + FILETYPE)

def find(reg: Pattern, string: str) -> list: return list([i.group() for i in reg.finditer(str(string))])
def findc(patternstring: str, string: str) -> list: return list(find(compile(str(patternstring)), str(string)))
def match(reg: Pattern, string: str) -> bool: return bool(reg.match(str(string)))

class Interpreter:
    variables = {
        NUMFOR: 0
    }

    funcs = {

    }

    def run(self, text: str) -> bool:
        text = text.split('\n')
        for line in text: 
            try: res = self.run_line(line)
            except Exception as e: 
                raise self.Error(str(e))
            if res != NORETURN: return res

        return NORETURN

    def run_line(self, line):
        cmd = line.split()[0]
        line = line[len(cmd) + 1:]

        if cmd == SET:
            if not match(setreg, line): raise self.GrammarError('Invalid syntax')
            vn = find(varreg, line)
            if not vn: raise self.GrammarError('Need an Variable')
            vn = vn[0]
            self.variables[vn[1: len(vn) - 1]] = self.get_string(line[len(vn) + 1:])

        elif cmd == PRINT: 
            if not match(stringreg, line): raise self.GrammarError('Invalid syntax')
            print(self.get_string(line))

        elif cmd == INPUT:
            if not match(varreg, line): raise self.GrammarError('Invalid syntax')
            vn = find(varreg, line)
            if not vn: raise self.GrammarError('Need an Variable')
            vn = vn[0]
            self.variables[vn[1: len(vn) - 1]] = input()

        elif cmd == IF:
            if not match(ifreg, line): raise self.GrammarError('Invalid syntax')
            do = str(line.split(IS)[1][1:]).replace(NL, '\n')
            line = line.split(IS)[0]
            if self.get_string(line.split(THIS)[0] ) == self.get_string(line.split(THIS)[1]): self.run(do)

        elif cmd == FOR:
            if not match(forreg, line): raise self.GrammarError('Invalid syntax')
            do = str(line.split(WHILE)[1][1:]).replace(NL, '\n')
            for _ in range(int(self.get_string(line.split(WHILE)[0]))): 
                self.run(do)
                self.variables[NUMFOR] += 1

        elif cmd == FUN: 
            if not match(funreg, line): raise self.GrammarError('Invalid syntax')
            fn = find(funcreg, line)
            if not fn: raise self.GrammarError('Need an FUNCTION')
            fn = fn[0]
            self.funcs[fn[1: len(fn) - 1]] = line[len(fn) + 1:]

        elif cmd == REQUIRE:
            if not match(requirereg, line): raise self.GrammarError('Invalid syntax')
            res = run_file(line)
            self.funcs.update(res.funcs)
            self.variables.update(res.variables)

        if cmd == RETURN: return self.get_string(line)
        else: return NORETURN

    def get_string(self, string):
        res = find(stringreg, string)
        if not res: raise self.NotaString(f'{string} is not a string')
        res = find(eachstrreg, ''.join(res))
        string = ''

        for i in res:
            typ = i[0]
            name = i[1:len(i) - 1]

            if typ == '{':
                if name not in self.variables.keys(): raise self.NoVariable(name)
                string += str(self.variables[name])
            
            elif typ == '(': 
                string += name
            
            elif typ == '[':
                string += str(len(self.get_string(name)))
            
            elif typ == '<':
                if name not in self.funcs.keys(): raise self.NoFunction(name)
                string += str(self.run(str(self.funcs[name]).replace(NL, '\n')))
            
            elif typ == '/':
                expression = str(self.get_string(name))
                if not match(expressionreg, expression): raise self.NotaExpression

                signs = find(findsignreg, expression)
                if len(signs) != 1: raise self.NotaExpression
                sign = signs[0]
                expression = expression.replace(sign, ' ')
                nums = find(findnumreg, expression)
                if len(nums) != 2: raise self.NotaExpression
                a = int(nums[0])
                b = int(nums[1])

                if sign == '+': r = a + b
                elif sign == '-': r = a - b
                elif sign == '*': r = a * b
                elif sign == '|': r = a // b
                elif sign == '%': r = a % b
                elif sign == '^': r = a ** b
                string += str(r)

        return str(string).replace(NL, '\n')

    class NotaString(Exception): 
        def __init__(self, msg = 'Not A string'): super().__init__(msg)
    
    class NotaExpression(Exception): 
        def __init__(self, msg = 'Not A expression'): super().__init__(msg)
    
    class NoVariable(Exception): 
        def __init__(self, name: str):
            self.name = str(name)
            super().__init__(f'Variable {name} Not Exist')
    
    class NoFunction(Exception): 
        def __init__(self, name: str):
            self.name = str(name)
            super().__init__(f'Function {name} Not Exist')
    
    class Error(Exception): pass
    class GrammarError(Exception): pass

def run_string(string: str): 
    a = Interpreter()
    a.run(string)
    return a

def run_file(name: str): return run_string(open(str(name), 'r', encoding = 'utf-8').read())

