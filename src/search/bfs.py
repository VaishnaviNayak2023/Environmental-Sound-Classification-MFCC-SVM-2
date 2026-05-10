from collections import deque

def bfs_search(tree):
    queue = deque([tree])
    while queue:
        node = queue.popleft()
        if node.get("goal"):
            return node["label"]
        for child in node.get("children", []):
            queue.append(child)
    return None