def dfs_stack(root):
    if not node:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        if node.left:
            stack.append(root.left)
        if node.right:
            stack.append(root.right)


