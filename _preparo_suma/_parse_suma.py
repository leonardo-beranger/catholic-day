import re, json

lines = open('_toc_full.txt', encoding='utf-8').read().split('\n')

parte_atual = None
tratado_atual = None
questao_atual = None

partes = {}
ordem_partes = []

PARTE_NOMES = ['Prima Pars', 'Pars Prima Secundae', 'Secunda Secundae', 'Tertia Pars', 'Suplemento']
TRATADO_PAT = re.compile(r'^Tratado (.+?)\s*\.{2,}.*?(\d+)\s*$')
QUESTAO_PAT = re.compile(r'^Quest[aã]o\s+(\d+):\s*(.+?)\s*\.{2,}.*?(\d+)\s*$')
ART_PAT = re.compile(r'^Art\.?\s*(\d+)\.?\s*[—\-─.]\s*(.+?)\s*\.{2,}.*?(\d+)\s*$')

def clean(s):
    return s.strip()

for raw in lines:
    l = raw.strip()
    if not l or l.startswith('--- PAGE'):
        continue

    matched_parte = None
    for nome in PARTE_NOMES:
        if l == nome or l.startswith(nome + ' ') or l.startswith(nome + '.'):
            # avoid false positive matches inside longer unrelated lines
            resto = l[len(nome):].strip()
            if resto == '' or re.match(r'^[.\d\s]*$', resto):
                matched_parte = nome
                break
    if matched_parte:
        if matched_parte not in partes:
            partes[matched_parte] = []
            ordem_partes.append(matched_parte)
        parte_atual = matched_parte
        tratado_atual = None
        questao_atual = None
        continue

    m = TRATADO_PAT.match(l)
    if m and parte_atual:
        nome_t = clean(m.group(1))
        pag = int(m.group(2))
        tratado_atual = {'tratado': nome_t, 'pagina': pag, 'questoes': []}
        partes[parte_atual].append(tratado_atual)
        questao_atual = None
        continue

    m = QUESTAO_PAT.match(l)
    if m and parte_atual:
        num = int(m.group(1))
        titulo = clean(m.group(2))
        pag = int(m.group(3))
        if tratado_atual is None:
            tratado_atual = {'tratado': None, 'pagina': pag, 'questoes': []}
            partes[parte_atual].append(tratado_atual)
        questao_atual = {'num': num, 'titulo': titulo, 'pagina': pag, 'artigos': []}
        tratado_atual['questoes'].append(questao_atual)
        continue

    m = ART_PAT.match(l)
    if m and questao_atual is not None:
        num = m.group(1)
        titulo = clean(m.group(2))
        pag = int(m.group(3))
        questao_atual['artigos'].append({'num': num, 'titulo': titulo, 'pagina': pag})
        continue

print('partes encontradas:', ordem_partes)
for p in ordem_partes:
    tqs = sum(len(t['questoes']) for t in partes[p])
    arts = sum(len(q['artigos']) for t in partes[p] for q in t['questoes'])
    print(p, 'tratados=', len(partes[p]), 'questoes=', tqs, 'artigos=', arts)

with open('_suma_estrutura.json', 'w', encoding='utf-8') as f:
    json.dump({'ordem_partes': ordem_partes, 'partes': partes}, f, ensure_ascii=False, indent=1)
print('gravado _suma_estrutura.json')
