!pip install networkx matplotlib ipywidgets --quiet

import networkx as nx
import matplotlib.pyplot as plt
from ipywidgets import Text, Button, VBox, HBox, Output, Layout
from IPython.display import display, clear_output

G = nx.Graph()
output = Output()

def malgrange_dfs(grafo):
    visitados = set()
    componentes = []

    def dfs(no, comp):
        visitados.add(no)
        comp.append(no)
        for vizinho in grafo.neighbors(no):
            if vizinho not in visitados:
                dfs(vizinho, comp)

    for no in grafo.nodes():
        if no not in visitados:
            comp_corrente = []
            dfs(no, comp_corrente)
            componentes.append(comp_corrente)

    return componentes

def desenhar_grafo(grupos=None):
    plt.figure(figsize=(8,6))
    pos = nx.spring_layout(G, seed=42)
    color_map = []
    node_group = {}
    if grupos is not None:
        for idx, grupo in enumerate(grupos):
            for nodo in grupo:
                node_group[nodo] = idx
        for node in G.nodes():
            color_map.append(node_group.get(node, -1))
        nx.draw(G, pos, with_labels=True, node_color=color_map, cmap=plt.cm.Set1, node_size=800, font_size=12)
    else:
        nx.draw(G, pos, with_labels=True, node_color='blue', node_size=800, font_size=12)
    plt.show()

def add_user(name):
    name = name.strip()
    if len(name) < 1:
        with output:
            print('Nome de participante vazio. Tente novamente!')
        return
    if name in G.nodes:
        with output:
            print(f'Participante "{name}" já existe no grafo.')
        return
    G.add_node(name)
    with output:
        print(f'Participante adicionado: {name}')
    desenhar_grafo()

def add_connection(p1, p2):
    p1 = p1.strip()
    p2 = p2.strip()
    if p1 == p2:
        with output:
            print('A ligação deve ser entre dois participantes diferentes!')
        return
    if not (p1 in G.nodes and p2 in G.nodes):
        with output:
            print('Ambos os participantes precisam existir no grafo!')
        return
    if G.has_edge(p1, p2):
        with output:
            print(f'Ligação entre "{p1}" e "{p2}" já existe.')
        return
    G.add_edge(p1, p2)
    with output:
        print(f'Aresta/ligação criada entre: {p1} e {p2}')
    desenhar_grafo()

def detectar_panelinhas():
    panelinhas = malgrange_dfs(G)
    with output:
        clear_output()
        print('Panelinhas/grupos encontrados:')
        for i, grupo in enumerate(panelinhas, 1):
            print(f'Grupo {i}: {sorted(grupo)}')
    desenhar_grafo(panelinhas)

def resetar():
    G.clear()
    with output:
        clear_output()
        print("Grafo reiniciado!")
    desenhar_grafo()

user_box = Text(placeholder='Nome do participante', description='Participante:', layout=Layout(width='60%'))
user_btn = Button(description='Adicionar participante', button_style='success')

conn_box1 = Text(placeholder='Participante 1', description='De:', layout=Layout(width='40%'))
conn_box2 = Text(placeholder='Participante 2', description='Para:', layout=Layout(width='40%'))
conn_btn = Button(description='Adicionar ligação', button_style='info')

panelinha_btn = Button(description='Detectar Panelinhas', button_style='primary')
reset_btn = Button(description='Reiniciar grafo', button_style='danger')

def on_add_user(b):
    with output:
        clear_output()
    add_user(user_box.value)
    user_box.value = ''

def on_add_connection(b):
    with output:
        clear_output()
    add_connection(conn_box1.value, conn_box2.value)
    conn_box1.value = ''
    conn_box2.value = ''

def on_detect_panelinhas(b):
    detectar_panelinhas()

def on_resetar(b):
    resetar()

user_btn.on_click(on_add_user)
conn_btn.on_click(on_add_connection)
panelinha_btn.on_click(on_detect_panelinhas)
reset_btn.on_click(on_resetar)

ui = VBox([
    HBox([user_box, user_btn]),
    HBox([conn_box1, conn_box2, conn_btn]),
    HBox([panelinha_btn, reset_btn]),
    output
])

display(ui)
desenhar_grafo()



