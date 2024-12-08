''' 
Nome: Sol Castilho Araújo de Moraes Sêda
Matricula: 1711600
'''

from ply.lex import lex
from ply.yacc import yacc
import sys

# Dicionário de palavras reservadas
reservados = {
    'FACA': 'FACA',
    'SER': 'SER',
    'MOSTRE': 'MOSTRE',
    'SOME': 'SOME',
    'COM': 'COM',
    'REPITA': 'REPITA',
    'VEZES': 'VEZES',
    'FIM': 'FIM',
    'SE': 'SE',
    'ENTAO': 'ENTAO',
    'SENAO': 'SENAO',
    'MULTIPLIQUE': 'MULTIPLIQUE',
    'POR': 'POR'
}

# Tokens
tokens = (
    'NUM', 
    'VAR', 
    'PONTO', 
    'DOISPONTOS'
) + tuple(reservados.values())

# Expressões regulares para tokens os tokens de ponto e dois pontos
t_PONTO = r'\.'
t_DOISPONTOS = r':'

# Números
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identificador (variável ou palavra reservada)
def t_VAR(t):
    r'[a-zA-Z]+'
    t.type = reservados.get(t.value, 'VAR')
    return t

# Ignora espaços e tabs
t_ignore = ' \t\n'

# Tratamento de erros para mostrar caracteres inválidos
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex()

codigo_python = []


def p_programa(regras):
    '''
    programa : cmds
    '''
    regras[0] = '\n'.join(regras[1])
    codigo_python.append(regras[0])

def p_cmds(regras):
    '''
    cmds : cmd cmds
         | cmd
    '''
    regras[0] = [regras[1]] + (regras[2] if len(regras) > 2 else [])

def p_cmd(regras):
    '''
    cmd : atribuicao
        | impressao
        | operacao
        | repeticao
        | condicional
    '''
    regras[0] = regras[1]

def p_atribuicao(regras):
    '''
    atribuicao : FACA VAR SER NUM PONTO
    '''
    regras[0] = f"{regras[2]} = {regras[4]}"

def p_impressao(regras):
    '''
    impressao : MOSTRE VAR PONTO
              | MOSTRE NUM PONTO
    '''
    regras[0] = f"print({regras[2]})"

def p_operacao(regras):
    '''
    operacao : SOME VAR COM VAR PONTO
             | SOME VAR COM NUM PONTO
             | SOME NUM COM VAR PONTO
             | SOME NUM COM NUM PONTO
    '''
    regras[0] = f"{regras[2]} + {regras[4]}"

def p_repeticao(regras):
    '''
    repeticao : REPITA NUM VEZES DOISPONTOS cmds FIM
    '''
    comandos = '\n    '.join(regras[5])
    regras[0] = f"for _ in range({regras[2]}):\n    {comandos}"

def p_condicional(regras):
    '''
    condicional : SE NUM ENTAO cmds FIM
    '''
    comandos_entao = '\n    '.join(regras[4])
    regras[0] = f"if {regras[2]}:\n    {comandos_entao}"

def p_condicional_senao(regras):
    '''
    condicional : SE NUM ENTAO cmds SENAO cmds FIM
    '''
    comandos_entao = '\n    '.join(regras[4])
    comandos_senao = '\n    '.join(regras[6])
    regras[0] = f"if {regras[2]}:\n    {comandos_entao}\nelse:\n    {comandos_senao}"

def p_operacao_mult(regras):
    '''
    operacao : MULTIPLIQUE VAR POR VAR PONTO
             | MULTIPLIQUE VAR POR NUM PONTO
             | MULTIPLIQUE NUM POR VAR PONTO
             | MULTIPLIQUE NUM POR NUM PONTO
    '''
    regras[0] = f"{regras[2]} * {regras[4]}"


def p_error(regras):
    if regras:
        print(f"Erro de sintaxe na linha {regras.lineno}: {regras.value}")
    else:
        print("Erro de sintaxe: Entrada inesperada")

parser = yacc()

if len(sys.argv) != 2:
    print("Uso: python main.py <arquivo.mag>")
    sys.exit(1)

arquivo_mag = sys.argv[1]

# Abrir o arquivo .mag
try:
    with open(arquivo_mag, 'r') as f:
        codigo_mag = f.read()
except FileNotFoundError:
    print(f"Erro: Arquivo {arquivo_mag} não encontrado.")
    sys.exit(1)

# Mostra os tokens gerados para debug
lexer.input(codigo_mag)
print("Tokens gerados:")
for token in lexer:
    print(token)

parser.parse(codigo_mag)

# Gera o arquivo de saida
arquivo_saida = arquivo_mag.replace('.mag', '.py')

try:
    with open(arquivo_saida, 'w') as f:
        f.write("\n".join(codigo_python))
    print(f"Código Python gerado em: {arquivo_saida}")
except IOError:
    print(f"Erro ao salvar o arquivo {arquivo_saida}.")
