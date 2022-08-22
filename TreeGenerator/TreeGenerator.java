import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class TreeGenerator<T> {

    public List<TreeNode<T>> generateTrees(int treeSize, T value) {

        // Returns the roots of all trees of the 
        // given size treeSize with the given value 

        List<TreeNode<T>> trees = new ArrayList<>();

        if (treeSize == 0) {

            trees.add(null);
            
            return trees;
        }

        for (int leftSubtreeSize = 0; leftSubtreeSize < treeSize; 
        leftSubtreeSize++) {

            int rightSubtreeSize = treeSize - 1 - leftSubtreeSize;

            List<TreeNode<T>> leftSubtrees 
            = generateTrees(leftSubtreeSize, value);
            List<TreeNode<T>> rightSubtrees 
            = generateTrees(rightSubtreeSize, value);

            for (TreeNode<T> leftSubtree : leftSubtrees) {

                for (TreeNode<T> rightSubtree : rightSubtrees) {

                    // Create a new tree with the given subtrees 
                    TreeNode<T> newTree = new TreeNode<>(value);
                    newTree.left = leftSubtree;
                    newTree.right = rightSubtree;

                    trees.add(newTree);
                }
            }
        }

        return trees;
    }

    public static void main(String[] args) {

        int treeSize = 3;

        TreeGenerator<Integer> aTreeGenerator = new TreeGenerator<>();

        List<TreeNode<Integer>> trees = aTreeGenerator
        .generateTrees(treeSize, 0);

        for (TreeNode<Integer> tree : trees) {

            System.out.println(tree.inOrder());
        }
    }
}

class TreeNode<T> {

    public T value;
    public TreeNode<T> left = null;
    public TreeNode<T> right = null;

    public TreeNode(T value) {

        this.value = value;
    }

    public List<TreeNode<T>> inOrder() {

        // Returns the in order traversal of the 
        // given tree 

        List<TreeNode<T>> inOrder = new ArrayList<>();

        inOrder(this, inOrder);

        return inOrder;
    }

    public void inOrder(TreeNode<T> root, List<TreeNode<T>> inOrder) {

        if (root == null) {

            return;
        }

        // Add left, curr, right 
        inOrder(root.left, inOrder);
        inOrder.add(root);
        inOrder(root.right, inOrder);
    }

    public String toString() {

        return this.value.toString();
    }
}