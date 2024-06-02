import sys
from functions import process_text_file, read_file, generate_directed_graph, write_output, draw_graph, process_user_input, find_shortest_path

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "./test.txt"
    
    output_path = "output.txt"
    process_text_file(file_path, output_path)
    print("Successfully output!") 
    content = read_file(output_path)
    graph = generate_directed_graph(content)
    
    for node, edges in graph.graph.items():
        for edge in edges:
            print(f"{node}→{edge}")

    draw_graph(graph, "output_graph.png")  # Save the graph to "output_graph.png"
    write_output(output_path, graph)

    word1 = input("请输入第一个单词：")
    word2 = input("请输入第二个单词：")
    print(graph.find_bridge_words(word1.lower(), word2.lower()))

    user_input = input("请输入新文本：")
    modified_text = process_user_input(graph, user_input)
    print("修改后的文本：", modified_text)

    # Find shortest path
    word1 = input("请输入第一个单词以计算最短路径：")
    word2 = input("请输入第二个单词以计算最短路径：")
    path, length = find_shortest_path(graph, word1.lower(), word2.lower())
    if path:
        print(f"最短路径为: {' → '.join(path)}, 路径长度为: {length}")
        draw_graph(graph, "output_graph_with_path.png", path)  # Save the graph with highlighted path to "output_graph_with_path.png"
    else:
        print("输入的两个单词之间没有路径。")

    # Random walk
    start_node = input("请输入随机游走的起始节点：")
    walk_path = graph.random_walk(start_node.lower())
    if isinstance(walk_path, str):
        print(walk_path)
    else:
        walk_path_str = ' → '.join(walk_path)
        print(f"随机游走路径为: {walk_path_str}")
        with open("random_walk_output.txt", 'w', encoding='utf-8') as f:
            f.write(walk_path_str)
        draw_graph(graph, "output_graph_with_random_walk.png", walk_path)

if __name__ == "__main__":
    main()
