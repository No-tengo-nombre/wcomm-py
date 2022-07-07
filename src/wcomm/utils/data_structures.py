class TreeNode:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def get_children(self):
        return self.left, self.right
