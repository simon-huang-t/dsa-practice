"""
Tests for DisjointSetUnion in lessons/graph/advanced_graphs/disjoint_set_union.py.

NOTE: The source file contains module-level code with a bare `return` statement
(example usage snippet left outside a function, lines 24-28), which causes a
SyntaxError on direct import.  We work around this by extracting only the class
definition using Python's `ast` module, compiling it, and executing it into a
local namespace.  All tests target the DisjointSetUnion class defined in that file.
"""

import ast
import os
import sys
import textwrap

import pytest

# ---------------------------------------------------------------------------
# Load the DisjointSetUnion class from the source file, bypassing the
# module-level SyntaxError caused by loose example code in the file.
# ---------------------------------------------------------------------------

_SOURCE_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../../../lessons/graph/advanced_graphs/disjoint_set_union.py",
)


def _load_class_from_source(path: str):
    """Parse the source file with ast, extract the DisjointSetUnion class
    definition, compile it, and return the resulting class object."""
    with open(path, "r") as fh:
        source = fh.read()

    # Parse only the valid statements (ast.parse stops at syntax-clean nodes)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # If the whole file is unparseable, extract just the class body lines
        # by splitting on the first blank line after the class block.
        lines = source.splitlines()
        class_lines = []
        in_class = False
        for line in lines:
            if line.startswith("class "):
                in_class = True
            if in_class:
                # Stop collecting when we hit a top-level non-class statement
                if class_lines and line and not line[0].isspace() and not line.startswith("class "):
                    break
                class_lines.append(line)
        class_src = "\n".join(class_lines)
        tree = ast.parse(class_src)

    # Collect only ClassDef nodes named "DisjointSetUnion"
    class_nodes = [
        node for node in ast.walk(tree) if isinstance(node, ast.ClassDef) and node.name == "DisjointSetUnion"
    ]
    assert class_nodes, "DisjointSetUnion class definition not found in source file"

    # Build a minimal module containing only the class definition
    module = ast.Module(body=[class_nodes[0]], type_ignores=[])
    ast.fix_missing_locations(module)
    code = compile(module, filename=path, mode="exec")

    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    return namespace["DisjointSetUnion"]


DisjointSetUnion = _load_class_from_source(_SOURCE_PATH)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestDisjointSetUnionInit:
    def test_parent_initialized_to_self(self):
        dsu = DisjointSetUnion(5)
        assert dsu.parent == [0, 1, 2, 3, 4]

    def test_rank_initialized_to_ones(self):
        dsu = DisjointSetUnion(5)
        assert dsu.rank == [1, 1, 1, 1, 1]

    def test_single_element(self):
        dsu = DisjointSetUnion(1)
        assert dsu.parent == [0]
        assert dsu.rank == [1]

    def test_two_elements(self):
        dsu = DisjointSetUnion(2)
        assert dsu.parent == [0, 1]
        assert dsu.rank == [1, 1]

    def test_large_n(self):
        n = 1000
        dsu = DisjointSetUnion(n)
        assert len(dsu.parent) == n
        assert len(dsu.rank) == n
        assert dsu.parent == list(range(n))
        assert dsu.rank == [1] * n


class TestDisjointSetUnionFind:
    def test_find_self_is_own_root(self):
        dsu = DisjointSetUnion(5)
        for i in range(5):
            assert dsu.find(i) == i

    def test_find_after_union_returns_same_root(self):
        dsu = DisjointSetUnion(5)
        dsu.union(0, 1)
        assert dsu.find(0) == dsu.find(1)

    def test_find_path_compression_updates_parent(self):
        # Manually create a chain: 0 -> 1 -> 2 -> 3 (3 is root)
        dsu = DisjointSetUnion(4)
        dsu.parent = [1, 2, 3, 3]
        dsu.rank = [1, 1, 1, 2]
        root = dsu.find(0)
        assert root == 3
        # Path compression must have pointed 0 directly at the root
        assert dsu.parent[0] == 3

    def test_find_transitivity(self):
        dsu = DisjointSetUnion(4)
        dsu.union(0, 1)
        dsu.union(1, 2)
        # 0, 1, 2 all share a root
        assert dsu.find(0) == dsu.find(1) == dsu.find(2)
        # 3 is still separate
        assert dsu.find(3) != dsu.find(0)

    def test_find_idempotent(self):
        dsu = DisjointSetUnion(3)
        dsu.union(0, 1)
        assert dsu.find(0) == dsu.find(0)

    def test_find_deep_path_compressed_after_query(self):
        # Chain of 10 nodes; after find(0) all nodes should point directly to root
        n = 10
        dsu = DisjointSetUnion(n)
        for i in range(n - 1):
            dsu.union(i, i + 1)
        root = dsu.find(0)
        for i in range(n):
            assert dsu.parent[i] == root


class TestDisjointSetUnionUnion:
    def test_union_different_components_returns_true(self):
        dsu = DisjointSetUnion(3)
        assert dsu.union(0, 1) is True

    def test_union_same_component_returns_false(self):
        dsu = DisjointSetUnion(3)
        dsu.union(0, 1)
        assert dsu.union(0, 1) is False

    def test_union_same_component_after_transitive_merge_returns_false(self):
        dsu = DisjointSetUnion(4)
        dsu.union(0, 1)
        dsu.union(1, 2)
        assert dsu.union(0, 2) is False

    def test_union_self_returns_false(self):
        dsu = DisjointSetUnion(3)
        assert dsu.union(0, 0) is False

    def test_union_rank_lower_attaches_to_higher(self):
        dsu = DisjointSetUnion(4)
        # union(0,1) makes one of them root with rank 2
        dsu.union(0, 1)
        high_root = dsu.find(0)
        # Attach isolated node 2 (rank 1) to the higher-rank component
        dsu.union(2, high_root)
        assert dsu.find(2) == high_root
        # The high-rank root's rank should be unchanged (higher ate lower)
        assert dsu.rank[high_root] == 2

    def test_union_equal_ranks_increments_new_root_rank(self):
        dsu = DisjointSetUnion(2)
        assert dsu.rank[0] == 1
        assert dsu.rank[1] == 1
        dsu.union(0, 1)
        root = dsu.find(0)
        assert dsu.rank[root] == 2

    def test_union_all_elements_in_chain(self):
        dsu = DisjointSetUnion(5)
        for i in range(4):
            dsu.union(i, i + 1)
        root = dsu.find(0)
        assert all(dsu.find(i) == root for i in range(5))

    def test_union_reversed_order_still_connects(self):
        dsu = DisjointSetUnion(4)
        dsu.union(3, 2)
        dsu.union(2, 1)
        dsu.union(1, 0)
        root = dsu.find(3)
        assert all(dsu.find(i) == root for i in range(4))

    def test_union_returns_false_for_chain_endpoint(self):
        # Build 0-1-2-3-4 chain, then union(0,4) — already connected
        dsu = DisjointSetUnion(5)
        for i in range(4):
            dsu.union(i, i + 1)
        assert dsu.union(0, 4) is False


class TestDisjointSetUnionConnectedComponents:
    def test_no_unions_n_components(self):
        n = 5
        dsu = DisjointSetUnion(n)
        components = len(set(dsu.find(i) for i in range(n)))
        assert components == n

    def test_all_unioned_one_component(self):
        n = 5
        dsu = DisjointSetUnion(n)
        for i in range(n - 1):
            dsu.union(i, i + 1)
        assert len(set(dsu.find(i) for i in range(n))) == 1

    def test_two_separate_components(self):
        dsu = DisjointSetUnion(6)
        dsu.union(0, 1)
        dsu.union(1, 2)
        dsu.union(3, 4)
        dsu.union(4, 5)
        assert len(set(dsu.find(i) for i in range(6))) == 2

    def test_star_topology(self):
        n = 6
        dsu = DisjointSetUnion(n)
        for i in range(1, n):
            dsu.union(0, i)
        assert len(set(dsu.find(i) for i in range(n))) == 1

    def test_disjoint_pairs_three_components(self):
        dsu = DisjointSetUnion(6)
        dsu.union(0, 1)
        dsu.union(2, 3)
        dsu.union(4, 5)
        assert len(set(dsu.find(i) for i in range(6))) == 3

    def test_single_node_one_component(self):
        dsu = DisjointSetUnion(1)
        assert len(set(dsu.find(i) for i in range(1))) == 1

    def test_repeated_union_does_not_inflate_component_count(self):
        dsu = DisjointSetUnion(3)
        dsu.union(0, 1)
        dsu.union(0, 1)
        dsu.union(0, 1)
        # Should still be exactly 2 components: {0,1} and {2}
        assert len(set(dsu.find(i) for i in range(3))) == 2

    def test_connectivity_is_symmetric(self):
        dsu = DisjointSetUnion(4)
        dsu.union(1, 0)  # reversed argument order
        assert dsu.find(0) == dsu.find(1)
        assert dsu.find(2) != dsu.find(0)

    def test_graph_with_cycle_counts_correctly(self):
        # Triangle: 0-1, 1-2, 0-2 — one component, last union returns False
        dsu = DisjointSetUnion(3)
        assert dsu.union(0, 1) is True
        assert dsu.union(1, 2) is True
        assert dsu.union(0, 2) is False
        assert len(set(dsu.find(i) for i in range(3))) == 1

    def test_large_graph_correct_component_count(self):
        # 20 nodes in 4 groups of 5
        dsu = DisjointSetUnion(20)
        for group_start in range(0, 20, 5):
            for i in range(group_start, group_start + 4):
                dsu.union(i, i + 1)
        assert len(set(dsu.find(i) for i in range(20))) == 4
