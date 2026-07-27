# -*- coding: utf-8 -*-
"""Os outros vinte concílios ecuménicos (todos excepto o Vaticano II, tratado
à parte com documentos completos). Para cada um: resumo original em
português, e — quando o concílio produziu uma fórmula doutrinal célebre e
estável (credos, definições) — o texto latino original, a tradução
portuguesa e a referência Denzinger-Hünermann (DH), conforme pedido.

Estes textos latinos são fórmulas fixas e amplamente atestadas (repetidas
identicamente em qualquer edição do Denzinger-Hünermann ou do Mansi); não
foram obtidos por download automático de um site específico — ao contrário
do Vaticano II, cujos 16 documentos completos vieram de vatican.va — porque
não encontrámos, no tempo disponível, uma fonte com estrutura previsível
para automatizar essa coleta. Ver README para a nota completa sobre este
recorte."""

CONCILIOS = [
    # ---------------------------------------------------------- Eixo 1
    {
        "numero": 1, "nome": "Niceia I", "ano": "325", "eixo": 1,
        "resumo": (
            "Convocado pelo imperador Constantino para resolver a crise ariana "
            "(que negava a plena divindade do Filho), definiu que o Filho é "
            "«consubstancial» (homoousios) ao Pai — a mesma substância divina, "
            "não uma criatura, por mais elevada que fosse. Fixou também a data "
            "comum da Páscoa e vinte cânones disciplinares, entre eles sobre a "
            "hierarquia dos grandes sés (Roma, Alexandria, Antioquia)."
        ),
        "citacao_latina": (
            "Credimus in unum Deum, Patrem omnipotentem […] Et in unum Dominum "
            "Iesum Christum, Filium Dei […] natum, non factum, consubstantialem "
            "Patri (homoousion to Patri), per quem omnia facta sunt."
        ),
        "traducao": (
            "Cremos em um só Deus, Pai todo-poderoso […] E em um só Senhor Jesus "
            "Cristo, Filho de Deus […] gerado, não feito, consubstancial ao Pai, "
            "por quem tudo foi feito."
        ),
        "referencia": "DH 125",
    },
    {
        "numero": 2, "nome": "Constantinopla I", "ano": "381", "eixo": 1,
        "resumo": (
            "Convocado para responder ao pneumatomaquismo (que negava a "
            "divindade do Espírito Santo), completou o Símbolo de Niceia com o "
            "artigo sobre o Espírito Santo, «Senhor que dá a vida, que procede do "
            "Pai, e que com o Pai e o Filho é adorado e glorificado». Deu origem "
            "ao Símbolo Niceno-Constantinopolitano, rezado até hoje na liturgia."
        ),
        "citacao_latina": (
            "Et in Spiritum Sanctum, Dominum et vivificantem, qui ex Patre "
            "procedit, qui cum Patre et Filio simul adoratur et conglorificatur."
        ),
        "traducao": (
            "E no Espírito Santo, Senhor que dá a vida, que procede do Pai, que "
            "com o Pai e o Filho é adorado e glorificado."
        ),
        "referencia": "DH 150",
    },
    {
        "numero": 3, "nome": "Éfeso", "ano": "431", "eixo": 1,
        "resumo": (
            "Condenou o nestorianismo, que separava de tal modo as duas naturezas "
            "de Cristo que parecia postular duas pessoas. Definiu a unidade "
            "pessoal de Cristo e, como consequência directa, proclamou Maria "
            "Theotokos — «Mãe de Deus» — pois quem ela gerou é o próprio Verbo "
            "encarnado, não apenas um homem unido a Deus."
        ),
        "citacao_latina": "Sancta Virgo Deipara est (Theotokos).",
        "traducao": "A Santa Virgem é Mãe de Deus (Theotokos).",
        "referencia": "DH 251-252",
    },
    {
        "numero": 4, "nome": "Calcedônia", "ano": "451", "eixo": 1,
        "resumo": (
            "Diante do monofisismo de Êutiques (que via em Cristo uma só natureza "
            "após a união), formulou a definição clássica da cristologia: em "
            "Cristo há duas naturezas, divina e humana, unidas numa só Pessoa "
            "(hipóstase), «sem confusão, sem mudança, sem divisão, sem "
            "separação» — os quatro advérbios que continuam a orientar toda a "
            "cristologia católica."
        ),
        "citacao_latina": (
            "Unum eundemque Christum […] in duabus naturis inconfuse, "
            "immutabiliter, indivise, inseparabiliter agnoscendum."
        ),
        "traducao": (
            "Um só e o mesmo Cristo […] deve ser reconhecido em duas naturezas, "
            "sem confusão, sem mudança, sem divisão, sem separação."
        ),
        "referencia": "DH 302",
    },
    {
        "numero": 5, "nome": "Constantinopla II", "ano": "553", "eixo": 1,
        "resumo": (
            "Convocado por Justiniano para tentar reconciliar os monofisitas, "
            "reafirmou Calcedônia e condenou os «Três Capítulos» (escritos "
            "considerados de tendência nestoriana), precisando ainda mais a "
            "unidade hipostática: é lícito dizer que uma das Pessoas da "
            "Santíssima Trindade sofreu na carne."
        ),
        "citacao_latina": None,
        "traducao": None,
        "referencia": "DH 421-438",
    },
    {
        "numero": 6, "nome": "Constantinopla III", "ano": "680–681", "eixo": 1,
        "resumo": (
            "Condenou o monotelismo (a tese de que Cristo teria só uma vontade, "
            "a divina) e definiu que Cristo possui duas vontades — divina e "
            "humana — e duas operações naturais, correspondentes às suas duas "
            "naturezas, sem que a vontade humana se oponha à divina, mas antes "
            "se lhe submeta livremente."
        ),
        "citacao_latina": (
            "Duas naturales voluntates […] et duas naturales operationes "
            "indivise, inconvertibiliter, inseparabiliter, inconfuse."
        ),
        "traducao": (
            "Duas vontades naturais […] e duas operações naturais, sem divisão, "
            "sem mudança, sem separação, sem confusão."
        ),
        "referencia": "DH 556",
    },
    {
        "numero": 7, "nome": "Niceia II", "ano": "787", "eixo": 1,
        "resumo": (
            "Encerrou a primeira fase da crise iconoclasta, definindo a "
            "legitimidade do culto às imagens sagradas: a veneração prestada à "
            "imagem passa ao seu protótipo, e quem venera a imagem venera a "
            "pessoa nela representada — distinção fundamental entre a "
            "«veneração» (proskynesis) devida às imagens e a «adoração» "
            "(latria) devida só a Deus."
        ),
        "citacao_latina": (
            "Honor qui imagini exhibetur, ad prototypum pertransit, et qui "
            "adorat imaginem, adorat in ea depicti subsistentiam."
        ),
        "traducao": (
            "A honra prestada à imagem transmite-se ao seu protótipo, e quem "
            "venera a imagem venera nela a pessoa que está representada."
        ),
        "referencia": "DH 601",
    },

    # ---------------------------------------------------------- Eixo 2
    {
        "numero": 8, "nome": "Constantinopla IV", "ano": "869–870", "eixo": 2,
        "resumo": (
            "Encerrou a controvérsia foviana em torno da deposição e "
            "restituição do patriarca Fócio de Constantinopla, reafirmando a "
            "primazia romana. A sua recepção como concílio ecuménico é "
            "contestada pela Ortodoxia oriental até hoje."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "DH 638-664",
    },
    {
        "numero": 9, "nome": "Latrão I", "ano": "1123", "eixo": 2,
        "resumo": (
            "Primeiro concílio ecuménico celebrado no Ocidente latino, encerrou "
            "formalmente a Questão das Investiduras (o conflito entre papas e "
            "imperadores sobre a nomeação de bispos), ratificando o Concordato "
            "de Worms (1122): a investidura espiritual (báculo e anel) cabe "
            "exclusivamente à Igreja."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "—",
    },
    {
        "numero": 10, "nome": "Latrão II", "ano": "1139", "eixo": 2,
        "resumo": (
            "Encerrou o cisma causado pelo antipapa Anacleto II, e legislou "
            "sobre disciplina clerical, condenando a usura e reforçando a "
            "obrigação do celibato para ordens maiores no Ocidente."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "—",
    },
    {
        "numero": 11, "nome": "Latrão III", "ano": "1179", "eixo": 2,
        "resumo": (
            "Reagiu à seita cátara/albigense e regulou a eleição papal: exigiu "
            "maioria de dois terços dos cardeais para a validade da eleição — "
            "regra que, com ajustes, permanece na base do conclave até hoje."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "—",
    },
    {
        "numero": 12, "nome": "Latrão IV", "ano": "1215", "eixo": 2,
        "resumo": (
            "Um dos concílios medievais mais importantes: definiu formalmente o "
            "termo «transubstanciação» para a mudança eucarística do pão e do "
            "vinho no Corpo e Sangue de Cristo, impôs a confissão e comunhão "
            "anuais mínimas aos fiéis, e organizou a repressão das heresias "
            "cátara e valdense."
        ),
        "citacao_latina": (
            "Corpus et sanguis […] transsubstantiatis pane in corpus, et vino in "
            "sanguinem potestate divina."
        ),
        "traducao": (
            "O corpo e o sangue […] transubstanciados o pão em corpo e o vinho "
            "em sangue, pelo poder divino."
        ),
        "referencia": "DH 802",
    },
    {
        "numero": 13, "nome": "Lyon I", "ano": "1245", "eixo": 2,
        "resumo": (
            "Convocado por Inocêncio IV em plena luta entre o Papado e o "
            "imperador Frederico II, decretou a deposição do imperador e tratou "
            "de organizar uma nova cruzada e o apoio ao império latino do "
            "Oriente."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "—",
    },
    {
        "numero": 14, "nome": "Lyon II", "ano": "1274", "eixo": 2,
        "resumo": (
            "Buscou (sem êxito duradouro) a união com a Igreja bizantina, que "
            "por breve tempo aceitou a profissão de fé latina, incluindo o "
            "Filioque e o primado romano. Regulou também o conclave, impondo "
            "clausura aos cardeais eleitores para evitar sedes vacantes "
            "prolongadas."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "DH 850-861",
    },
    {
        "numero": 15, "nome": "Viena", "ano": "1311–1312", "eixo": 2,
        "resumo": (
            "Decretou a supressão da Ordem dos Templários, sob pressão do rei "
            "Filipe IV de França, e tratou de reforma do clero e das ordens "
            "religiosas."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "—",
    },
    {
        "numero": 16, "nome": "Constança", "ano": "1414–1418", "eixo": 2,
        "resumo": (
            "Encerrou o Grande Cisma do Ocidente (havia então três pretendentes "
            "ao papado), depondo ou aceitando a renúncia dos rivais e elegendo "
            "Martinho V como papa único reconhecido, restaurando a unidade "
            "visível da Igreja latina."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "—",
    },
    {
        "numero": 17, "nome": "Basileia–Ferrara–Florença", "ano": "1431–1445", "eixo": 2,
        "resumo": (
            "Concílio de longa e complexa história (mudou de sede três vezes e "
            "chegou a gerar um cisma conciliarista em Basileia). Na fase de "
            "Florença, alcançou breves acordos de união com as Igrejas grega, "
            "arménia e copta, reafirmando a primazia do Romano Pontífice e a "
            "doutrina sobre o Purgatório e os sete sacramentos."
        ),
        "citacao_latina": (
            "Romanum Pontificem […] successorem beati Petri principis "
            "Apostolorum, et verum Christi vicarium, totiusque Ecclesiae caput."
        ),
        "traducao": (
            "O Romano Pontífice […] sucessor do bem-aventurado Pedro, príncipe "
            "dos Apóstolos, e verdadeiro vigário de Cristo, e cabeça de toda a "
            "Igreja."
        ),
        "referencia": "DH 1307",
    },
    {
        "numero": 18, "nome": "Latrão V", "ano": "1512–1517", "eixo": 2,
        "resumo": (
            "Último grande concílio antes da Reforma protestante, tratou "
            "sobretudo de reformas disciplinares (ainda insuficientes para "
            "evitar a crise que rebentaria poucos anos depois) e definiu contra "
            "certas correntes filosóficas averroístas a imortalidade pessoal da "
            "alma humana como verdade de fé."
        ),
        "citacao_latina": None, "traducao": None, "referencia": "DH 1440",
    },
    {
        "numero": 19, "nome": "Trento", "ano": "1545–1563", "eixo": 2,
        "resumo": (
            "A resposta doutrinal e disciplinar da Igreja Católica à Reforma "
            "Protestante, e o concílio mais extenso antes do Vaticano II. "
            "Definiu a relação entre Escritura e Tradição como fontes conjuntas "
            "da Revelação, a doutrina da justificação (contra o «só a fé» "
            "luterano, sem negar a gratuidade da graça), a realidade dos sete "
            "sacramentos e a presença real na Eucaristia, e promoveu uma vasta "
            "reforma disciplinar — seminários diocesanos, residência "
            "obrigatória dos bispos, catecismo unificado — que deu forma à "
            "Igreja Católica moderna até ao Vaticano II."
        ),
        "citacao_latina": (
            "Si quis dixerit, solam fidem […] sufficere ad iustificationem "
            "obtinendam […] anathema sit."
        ),
        "traducao": (
            "Se alguém disser que só a fé […] basta para se obter a "
            "justificação […] seja excomungado."
        ),
        "referencia": "DH 1560",
    },

    # ---------------------------------------------------------- Eixo 3
    {
        "numero": 20, "nome": "Vaticano I", "ano": "1869–1870", "eixo": 3,
        "resumo": (
            "Interrompido pela invasão de Roma durante a unificação italiana "
            "(e por isso nunca formalmente encerrado, só suspenso), produziu "
            "duas constituições doutrinais decisivas: Dei Filius, sobre a "
            "possibilidade de conhecer Deus pela razão natural e a relação "
            "entre fé e razão; e Pastor Aeternus, que definiu o primado de "
            "jurisdição universal do Papa sobre toda a Igreja e a sua "
            "infalibilidade, sob condições precisas, quando fala ex cathedra "
            "em matéria de fé e moral."
        ),
        "citacao_latina": (
            "Romanus Pontifex, cum ex cathedra loquitur […] ea infallibilitate "
            "pollet, qua divinus Redemptor Ecclesiam suam […] instructam esse "
            "voluit."
        ),
        "traducao": (
            "O Romano Pontífice, quando fala ex cathedra […] goza daquela "
            "infalibilidade com que o divino Redentor quis que a sua Igreja "
            "fosse dotada."
        ),
        "referencia": "DH 3074",
    },
]
