from interpreter import Interpreter

def run_string(string: str): Interpreter().run(string)
def run_file(name: str): run_string(open(str(name), 'r', encoding = 'utf-8').read())

run_file('test.sansscript')
run_string('샌즈 (키키)')
