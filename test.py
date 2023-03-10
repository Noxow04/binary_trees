import unittest

from main import Tree


class TestTree(unittest.TestCase):
    def test_instance(self):
        self.assertIsInstance(Tree(), Tree)
        self.assertIsInstance(Tree(None), Tree)
        self.assertIsInstance(Tree(3), Tree)
        self.assertEqual(Tree(), Tree())
        self.assertIsNot(Tree(), Tree())
        v = 2
        self.assertEqual(Tree(v), Tree(v))
        self.assertIsNot(Tree(v), Tree(v))
        n = Tree.Node(2)
        t1 = Tree()
        t1.root = n
        t2 = Tree()
        t2.root = n
        self.assertEqual(t1, t2)
        self.assertIsNot(t1, t2)

    def test_depth(self):
        with self.assertRaises(SyntaxError):
            _ = Tree().depth
        self.assertEqual(Tree(1).depth, 1)
        t = Tree(3)
        t.root.left = Tree.Node(2)
        self.assertEqual(t.depth, 2)

    def test_calculate_depth(self):
        with self.assertRaises(SyntaxError):
            Tree().calculate_depth()
        t = Tree(3)
        t.root.left = Tree.Node(2)
        self.assertEqual(t.calculate_depth(include_root_in_depth=False), 1)
        self.assertEqual(t.calculate_depth(), 2)

    def test_root(self):
        t = Tree(1)
        self.assertEqual(t.root, Tree.Node(1))
        with self.assertRaises(SyntaxError):
            t.root = Tree.Node(2)

    def test_replace_root(self):
        t = Tree(1)
        self.assertEqual(t.root, Tree.Node(1))
        t.replace_root(Tree.Node(2))
        self.assertEqual(t.root, Tree.Node(2))

    def test_iter():
        tree = Tree.build_from_values(1,2,4,5,8,7,6,allow_duplicates=True)
        for elt, E in zip(tree._browse(),tree):
            self.assertEqual(elt,E)

if __name__ == '__main__':
    unittest.main()
