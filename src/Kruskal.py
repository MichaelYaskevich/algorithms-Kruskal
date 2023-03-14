import sys


def read_adjacency_array(get_line):
    adjacency_array = [int(x) for x in get_line().split()]
    while adjacency_array[-1] != 32767:
        adjacency_array += [int(x) for x in get_line().split()]
    return adjacency_array


def read(get_line):
    n = int(get_line())
    adjacency_array = read_adjacency_array(get_line)
    all_edges = set()
    i = 0
    vertexes = []
    while adjacency_array[i] != n:
        start_index = adjacency_array[i]  # i вершина
        end_index = adjacency_array[i + 1]
        v = i + 1
        vertexes.append(v)
        for j in range(start_index, end_index, 2):
            w = adjacency_array[j - 1]
            c = adjacency_array[j]
            all_edges.add((min(v, w), max(v, w), c))
        i += 1
    return all_edges, vertexes


def is_cyclic_dfs(path, vertex, adjacency_lists, target):
    for neighbour, _ in adjacency_lists[vertex]:
        if neighbour not in path:
            if neighbour == target or is_cyclic_dfs(path + [neighbour], neighbour, adjacency_lists, target):
                return True
    return False


def is_cyclic(v, adjacency_lists):
    for neighbour, _ in adjacency_lists[v]:
        for neighbour2, _ in adjacency_lists[neighbour]:
            if neighbour2 == v:
                continue
            if is_cyclic_dfs([neighbour, neighbour2], neighbour2, adjacency_lists, v):
                return True
    return False


def kruskal_algo(edges, vertexes):
    adjacency_lists = {v: [] for v in vertexes}
    weight = 0
    for v, w, c in edges:
        weight += c
        adjacency_lists[v].append((w, c))
        adjacency_lists[w].append((v, c))
        if is_cyclic(v, adjacency_lists):
            weight -= c
            adjacency_lists[v].pop()
            adjacency_lists[w].pop()
    return adjacency_lists, weight


def write(write_func, adjacency_lists, weight):
    result = []
    for k, list_k in adjacency_lists.items():
        result.append(str(k) + ' ' + ' '.join((f'{x[0]} {x[1]}' for x in sorted(list_k))) + ' 0')
    result.append(str(weight))
    write_func('\n'.join(result))


INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]


if __name__ == '__main__':
    with open(INPUT_FILE) as f:
        edges, vertexes = read(f.readline)

    edges = sorted(edges, key=lambda x: x[2])
    adjacency_lists, weight = kruskal_algo(edges, vertexes)

    with open(OUTPUT_FILE, 'w') as f:
        write(f.write, adjacency_lists, weight)
