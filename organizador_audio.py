import os
import re
from collections import deque

EXTENSOES_VALIDAS = ('.mp3', '.wav', '.flac', '.ogg', '.aac')

def extrair_bpm(nome_arquivo):
    bpm = re.findall(r'\d+', nome_arquivo)
    return int(bpm[0]) if bpm else None

class Node:
    def __init__(self, bpm):
        self.bpm = bpm
        self.arquivos = []
        self.left = None
        self.right = None

class ArvoreBPM:
    def __init__(self):
        self.root = None

    def inserir(self, bpm, arquivo):
        self.root = self._inserir(self.root, bpm, arquivo)

    def _inserir(self, node, bpm, arquivo):
        if node is None:
            node = Node(bpm)
            node.arquivos.append(arquivo)
            return node
        if bpm < node.bpm:
            node.left = self._inserir(node.left, bpm, arquivo)
        elif bpm > node.bpm:
            node.right = self._inserir(node.right, bpm, arquivo)
        else:
            node.arquivos.append(arquivo)
        return node

    def em_ordem(self, node):
        if node:
            self.em_ordem(node.left)
            print(f"BPM {node.bpm}: {node.arquivos}")
            self.em_ordem(node.right)

class ListaEncadeada:
    class Node:
        def __init__(self, dado):
            self.dado = dado
            self.proximo = None

    def __init__(self):
        self.cabeca = None

    def inserir(self, dado):
        novo = self.Node(dado)
        if self.cabeca is None:
            self.cabeca = novo
        else:
            atual = self.cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo

    def exibir(self):
        atual = self.cabeca
        while atual:
            print(atual.dado)
            atual = atual.proximo

def ler_arquivos(caminho_pasta):
    arquivos = []
    for raiz, _, files in os.walk(caminho_pasta):
        for file in files:
            if file.lower().endswith(EXTENSOES_VALIDAS):
                arquivos.append(os.path.join(raiz, file))
    return arquivos

from google.colab import drive
drive.mount('/content/drive')

caminho = '/Teste'

arvore = ArvoreBPM()
lista = ListaEncadeada()
fila = deque()
pilha = []

arquivos = ler_arquivos(caminho)

for arquivo in arquivos:
    nome = os.path.basename(arquivo)
    bpm = extrair_bpm(nome)

    if bpm is not None:

        arvore.inserir(bpm, nome)


    lista.inserir(nome)


    fila.append(nome)


    pilha.append(nome)

print("🎧 ▶️ Playlist (Fila):")
print(list(fila))

print("\n🎧 🔄 Playlist Reversa (Pilha):")
print(list(reversed(pilha)))

print("\n🎧 📜 Lista de Arquivos (Lista Encadeada):")
lista.exibir()

print("\n🎧 🌳 Arquivos organizados por BPM (Árvore):")
arvore.em_ordem(arvore.root)
