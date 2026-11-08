"""
AlgoScope Comprehensive Test Suite
Tests all algorithm logic, step generation, data structures, and Tkinter UI instantiation.
"""

import sys
import unittest
import tkinter as tk

# Core models & themes
from core.theme import COLOR_BLACK, COLOR_SURFACE_1
from core.base_algorithm import Step
from core.animation_engine import AnimationEngine

# Algorithms
from algorithms.sorting import (
    bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort
)
from algorithms.searching import (
    linear_search, binary_search, jump_search, interpolation_search
)
from algorithms.graphs import (
    bfs, dfs, dijkstra, a_star, prim_mst, kruskal_mst
)
from algorithms.trees import TreeManager
from algorithms.data_structures import (
    VisualStack, VisualQueue, VisualCircularQueue, VisualLinkedList, VisualHashTable
)
from algorithms.benchmarks import run_benchmark

# UI modules
from main import AlgoScopeApp

class TestAlgoScopeLogic(unittest.TestCase):
    def test_sorting_algorithms(self):
        sample = [42, 17, 93, 8, 25, 60, 4, 31]
        expected_asc = sorted(sample)
        expected_desc = sorted(sample, reverse=True)

        for algo_fn in [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort]:
            # Ascending
            gen = algo_fn(sample, ascending=True)
            last_step = None
            for step in gen:
                self.assertIsInstance(step, Step)
                last_step = step
            self.assertEqual(last_step.state, expected_asc, f"Failed asc for {algo_fn.__name__}")

            # Descending
            gen_desc = algo_fn(sample, ascending=False)
            last_desc_step = None
            for step in gen_desc:
                last_desc_step = step
            self.assertEqual(last_desc_step.state, expected_desc, f"Failed desc for {algo_fn.__name__}")

    def test_searching_algorithms(self):
        arr = [3, 8, 14, 22, 35, 47, 59, 71, 88, 96]
        target = 47

        for search_fn in [linear_search, binary_search, jump_search, interpolation_search]:
            gen = search_fn(arr, target)
            found = False
            for step in gen:
                if step.action == "found":
                    found = True
                    self.assertEqual(step.metrics.get("found_index"), 5)
            self.assertTrue(found, f"Target not found in {search_fn.__name__}")

            # Missing target
            gen_miss = search_fn(arr, 100)
            not_found = False
            for step in gen_miss:
                if step.action == "not_found":
                    not_found = True
            self.assertTrue(not_found, f"Miss target not handled in {search_fn.__name__}")

    def test_graph_algorithms(self):
        graph = {
            "A": [("B", 4.0), ("C", 2.0)],
            "B": [("A", 4.0), ("C", 1.0), ("D", 5.0)],
            "C": [("A", 2.0), ("B", 1.0), ("D", 8.0)],
            "D": [("B", 5.0), ("C", 8.0)]
        }
        pos = {"A": (0, 0), "B": (10, 0), "C": (0, 10), "D": (10, 10)}

        # BFS
        steps_bfs = list(bfs(graph, "A", "D"))
        self.assertTrue(len(steps_bfs) > 0)
        self.assertEqual(steps_bfs[-1].action, "done")

        # DFS
        steps_dfs = list(dfs(graph, "A", "D"))
        self.assertTrue(len(steps_dfs) > 0)
        self.assertEqual(steps_dfs[-1].action, "done")

        # Dijkstra
        steps_dijk = list(dijkstra(graph, "A", "D"))
        self.assertTrue(len(steps_dijk) > 0)
        self.assertEqual(steps_dijk[-1].action, "done")
        self.assertEqual(steps_dijk[-1].state["path"], ["A", "C", "B", "D"] or ["A", "B", "D"])

        # A*
        steps_astar = list(a_star(graph, pos, "A", "D"))
        self.assertTrue(len(steps_astar) > 0)
        self.assertEqual(steps_astar[-1].action, "done")

        # Prim
        steps_prim = list(prim_mst(graph, "A"))
        self.assertTrue(len(steps_prim) > 0)
        self.assertEqual(steps_prim[-1].action, "done")

        # Kruskal
        steps_kruskal = list(kruskal_mst(graph))
        self.assertTrue(len(steps_kruskal) > 0)
        self.assertEqual(steps_kruskal[-1].action, "done")

    def test_tree_algorithms(self):
        # BST
        bst = TreeManager(is_avl=False)
        for k in [50, 30, 70, 20, 40]:
            list(bst.insert(k))
        self.assertIsNotNone(bst.root)
        self.assertEqual(bst.root.key, 50)

        # Search BST
        search_steps = list(bst.search(40))
        self.assertEqual(search_steps[-1].action, "found")

        # AVL balancing
        avl = TreeManager(is_avl=True)
        # Inserting 10, 20, 30 causes RR rotation at 10
        for k in [10, 20, 30]:
            list(avl.insert(k))
        self.assertEqual(avl.root.key, 20)  # Rotated!
        self.assertEqual(avl.root.left.key, 10)
        self.assertEqual(avl.root.right.key, 30)

        # Traversals
        in_steps = list(avl.traverse("inorder"))
        self.assertEqual(in_steps[-1].indices, [10, 20, 30])

    def test_data_structures(self):
        # Stack
        st = VisualStack(capacity=3)
        list(st.push(1))
        list(st.push(2))
        list(st.peek())
        pop_steps = list(st.pop())
        self.assertEqual(pop_steps[-1].action, "pop")
        self.assertEqual(st.items, [1])

        # Queue
        q = VisualQueue(capacity=3)
        list(q.enqueue("A"))
        list(q.enqueue("B"))
        deq_steps = list(q.dequeue())
        self.assertEqual(deq_steps[-1].action, "dequeue")
        self.assertEqual(q.items, ["B"])

        # Circular Queue
        cq = VisualCircularQueue(capacity=4)
        list(cq.enqueue(10))
        list(cq.enqueue(20))
        list(cq.dequeue())
        self.assertEqual(cq.size, 1)

        # Linked List
        ll = VisualLinkedList(is_doubly=True)
        list(ll.insert_head(5))
        list(ll.insert_tail(15))
        list(ll.delete(5))
        self.assertEqual(ll.nodes, [15])

        # Hash Table Chaining
        ht = VisualHashTable(capacity=5, mode="chaining")
        list(ht.insert("key1", 100))
        res = list(ht.search("key1"))
        self.assertEqual(res[-1].action, "found")

        # Hash Table Linear Probing
        ht_lp = VisualHashTable(capacity=5, mode="linear_probing")
        list(ht_lp.insert("k1", 10))
        list(ht_lp.insert("k2", 20))
        res_lp = list(ht_lp.search("k2"))
        self.assertEqual(res_lp[-1].action, "found")

    def test_benchmarks(self):
        results = run_benchmark(["Bubble Sort", "Quick Sort"], size=50)
        self.assertIn("Bubble Sort", results)
        self.assertIn("Quick Sort", results)
        self.assertGreaterEqual(results["Bubble Sort"]["comparisons"], 0)


class TestAlgoScopeUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during headless test

    def tearDown(self):
        self.root.destroy()

    def test_ui_navigation_and_views(self):
        app = AlgoScopeApp(self.root)
        self.assertIsNotNone(app.landing_page)

        # Navigate to Dashboard
        app.show_dashboard()
        self.assertIsNone(app.landing_page)
        self.assertIsNotNone(app.current_view)

        # Navigate to all 6 modules sequentially
        modules = ["Sorting", "Searching", "Graphs", "Trees", "Data Structures", "Performance"]
        for m in modules:
            app.navigate_to_module(m)
            self.assertIsNotNone(app.current_view, f"Failed loading view for module {m}")
            # Trigger a small step or state refresh
            app.root.update_idletasks()

        # Return to landing page
        app.show_landing_page()
        self.assertIsNotNone(app.landing_page)

    def test_sliding_pill_nav(self):
        from ui.components import SlidingPillNav
        selected = []
        nav = SlidingPillNav(
            self.root,
            items=["Home", "Design", "Code", "Deploy"],
            initial_index=1,
            on_select=lambda idx, name: selected.append((idx, name))
        )
        self.assertEqual(nav.selected_idx, 1)
        self.assertEqual(nav.items[nav.selected_idx], "Design")

        # Select by index
        nav.set_selected_index(3, trigger_callback=True, animate=True)
        self.assertEqual(nav.selected_idx, 3)
        self.assertEqual(selected[-1], (3, "Deploy"))

        # Select by name
        nav.select_by_name("Code", trigger_callback=True, animate=True)
        self.assertEqual(nav.selected_idx, 2)
        self.assertEqual(selected[-1], (2, "Code"))

        # Advance animations
        for _ in range(20):
            self.root.update_idletasks()
            self.root.update()

    def test_dpi_subsystem(self):
        from core.dpi import setup_high_dpi, configure_root_dpi, get_dpi_scale_factor
        mode = setup_high_dpi()
        self.assertIn(mode, ["per_monitor_v2", "per_monitor_v1", "system_aware", "system_legacy", "non-windows", "unaware"])
        factor = configure_root_dpi(self.root)
        self.assertGreaterEqual(factor, 1.0)
        self.assertEqual(get_dpi_scale_factor(), factor)


if __name__ == "__main__":
    unittest.main()

