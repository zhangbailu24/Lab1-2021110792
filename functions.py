import re
import random
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, word1, word2):
        self.graph[word1].append(word2)

    def find_bridge_words(self, word1, word2):
        if word1 not in self.graph or word2 not in self.graph:
            return "No word1 or word2 in the graph!"

        visited = set()
        bridge_words = []

        def dfs(word, target, path):
            if word == target and len(path) > 2:
                bridge_words.extend(path[1:-1])
                return
            visited.add(word)
            for neighbor in self.graph[word]:
                if neighbor not in visited:
                    dfs(neighbor, target, path + [neighbor])

        dfs(word1, word2, [word1])

        if not bridge_words:
            return "No bridge words from word1 to word2!"
        else:
            return "The bridge words from word1 to word2 are: " + ", ".join(bridge_words) + "."

    def get_bridge_words(self, word1, word2):
        bridge_words = []
        for intermediate in self.graph[word1]:
            if word2 in self.graph[intermediate]:
                bridge_words.append(intermediate)
        return bridge_words

    def random_walk(self, start_node):
        if start_node not in self.graph:
            return "The start node does not exist in the graph!"

        visited_edges = set()
        path = [start_node]

        current_node = start_node
        while True:
            if not self.graph[current_node]:
                break

            next_node = random.choice(self.graph[current_node])
            edge = (current_node, next_node)

            if edge in visited_edges:
                break

            visited_edges.add(edge)
            path.append(next_node)
            current_node = next_node

        return path

def process_text_file(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r'[^A-Za-z]+', ' ', content)
        words = content.split()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(word + '\n')
        
        return words
    except FileNotFoundError:
        print("找不到文件夹，请检查文件路径是否正确。")
        return None

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def generate_directed_graph(content):
    words = content.split()
    graph = Graph()
    for i in range(len(words) - 1):
        graph.add_edge(words[i].lower(), words[i + 1].lower())
    return graph

def draw_graph(graph, file_name="graph.png", path=None):
    G = nx.DiGraph()
    for node, edges in graph.graph.items():
        for edge in edges:
            G.add_edge(node, edge)
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    
    if path:
        edges = [(path[n], path[n + 1]) for n in range(len(path) - 1)]
        edge_colors = ["red" if edge in edges else "black" for edge in G.edges()]
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=15, font_weight="bold", arrows=True, edge_color=edge_colors)
    else:
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=15, font_weight="bold", arrows=True)
    
    if path:
        plt.title(f"Directed Graph with Highlighted Path: {' → '.join(path)}")
    else:
        plt.title("Directed Graph")

    plt.savefig(file_name)  # Save the figure to a file
    plt.close()  # Close the plot to avoid conflicts

def write_output(file_path, graph):
    with open(file_path, 'w', encoding='utf-8') as f:
        for node, edges in graph.graph.items():
            for edge in edges:
                f.write(f"{node}→{edge}\n")

def process_user_input(graph, user_input):
    words = user_input.split()
    for i in range(len(words) - 1):
        word1, word2 = words[i].lower(), words[i + 1].lower()
        bridge_words = graph.get_bridge_words(word1, word2)
        if bridge_words:
            selected_bridge_word = random.choice(bridge_words)
            words.insert(i + 1, selected_bridge_word)
    return ' '.join(words)

def find_shortest_path(graph, word1, word2):
    G = nx.DiGraph()
    for node, edges in graph.graph.items():
        for edge in edges:
            G.add_edge(node, edge)
    
    try:
        path = nx.shortest_path(G, source=word1, target=word2)
        length = nx.shortest_path_length(G, source=word1, target=word2)
        return path, length
    except nx.NetworkXNoPath:
        return None, None
