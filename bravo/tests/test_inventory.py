import unittest

import bravo.blocks
import bravo.inventory

class TestInventoryInternals(unittest.TestCase):

    def setUp(self):
        self.i = bravo.inventory.Inventory(0, 45)

    def test_trivial(self):
        pass

    def test_add_to_inventory(self):
        self.assertEqual(self.i.holdables, [None] * 9)
        self.assertTrue(self.i.add(2, 1))
        self.assertEqual(self.i.holdables[0], (2, 0, 1))

    def test_add_to_inventory_sequential(self):
        self.assertEqual(self.i.holdables, [None] * 9)
        self.assertTrue(self.i.add(2, 1))
        self.assertEqual(self.i.holdables[0], (2, 0, 1))
        self.assertTrue(self.i.add(2, 1))
        self.assertEqual(self.i.holdables[0], (2, 0, 2))
        self.assertEqual(self.i.holdables[1], None)

    def test_consume_holdable(self):
        self.i.holdables[0] = (2, 0, 1)
        self.assertTrue(self.i.consume(2))
        self.assertEqual(self.i.holdables[0], None)

    def test_consume_holdable_empty(self):
        self.assertFalse(self.i.consume(2))

    def test_consume_holdable_second_slot(self):
        self.i.holdables[1] = (2, 0, 1)
        self.assertTrue(self.i.consume(2))
        self.assertEqual(self.i.holdables[1], None)

    def test_select_stack(self):
        self.i.holdables[0] = (2, 0, 1)
        self.i.holdables[1] = (2, 0, 1)
        self.i.select(37)
        self.i.select(36)
        self.assertEqual(self.i.holdables[0], (2, 0, 2))
        self.assertEqual(self.i.holdables[1], None)

    def test_select_switch(self):
        self.i.holdables[0] = (2, 0, 1)
        self.i.holdables[1] = (3, 0, 1)
        self.i.select(36)
        self.i.select(37)
        self.i.select(36)
        self.assertEqual(self.i.holdables[0], (3, 0, 1))
        self.assertEqual(self.i.holdables[1], (2, 0, 1))

class TestCraftingWood(unittest.TestCase):
    """
    Test basic crafting functionality.

    Assumes that the basic log->wood recipe is present and enabled. This
    recipe was chosen because it is the simplest and most essential recipe
    from which all crafting is derived.
    """

    def setUp(self):
        self.i = bravo.inventory.Inventory(0, 45)

    def test_trivial(self):
        pass

    def test_check_crafting(self):
        self.i.crafting[0] = (bravo.blocks.blocks["log"].slot, 0, 1)
        # Force crafting table to be rechecked.
        self.i.select(2)
        self.assertTrue(self.i.recipe)
        self.assertEqual(self.i.recipe_offset, (0, 0))
        self.assertEqual(self.i.crafted[0],
            (bravo.blocks.blocks["wood"].slot, 0, 4))

    def test_check_crafting_multiple(self):
        self.i.crafting[0] = (bravo.blocks.blocks["log"].slot, 0, 2)
        # Force crafting table to be rechecked.
        self.i.select(2)
        # Only checking count of crafted table; the previous test assured that
        # the recipe was selected.
        self.assertEqual(self.i.crafted[0],
            (bravo.blocks.blocks["wood"].slot, 0, 8))

    def test_check_crafting_offset(self):
        self.i.crafting[1] = (bravo.blocks.blocks["log"].slot, 0, 1)
        # Force crafting table to be rechecked.
        self.i.select(1)
        self.assertTrue(self.i.recipe)
        self.assertEqual(self.i.recipe_offset, (0, 1))

class TestCraftingSticks(unittest.TestCase):
    """
    Test basic crafting functionality.

    Assumes that the basic wood->stick recipe is present and enabled. This
    recipe was chosen because it is the simplest recipe with more than one
    ingredient.
    """

    def setUp(self):
        self.i = bravo.inventory.Inventory(0, 45)

    def test_trivial(self):
        pass

    def test_check_crafting(self):
        self.i.crafting[0] = (bravo.blocks.blocks["wood"].slot, 0, 1)
        self.i.crafting[2] = (bravo.blocks.blocks["wood"].slot, 0, 1)
        # Force crafting table to be rechecked.
        self.i.select(2)
        self.assertTrue(self.i.recipe)
        self.assertEqual(self.i.recipe_offset, (0, 0))
        self.assertEqual(self.i.crafted[0],
            (bravo.blocks.items["stick"].slot, 0, 4))

    def test_check_crafting_multiple(self):
        self.i.crafting[0] = (bravo.blocks.blocks["wood"].slot, 0, 2)
        self.i.crafting[2] = (bravo.blocks.blocks["wood"].slot, 0, 2)
        # Force crafting table to be rechecked.
        self.i.select(2)
        # Only checking count of crafted table; the previous test assured that
        # the recipe was selected.
        self.assertEqual(self.i.crafted[0],
            (bravo.blocks.items["stick"].slot, 0, 8))

    def test_check_crafting_offset(self):
        self.i.crafting[1] = (bravo.blocks.blocks["wood"].slot, 0, 1)
        self.i.crafting[3] = (bravo.blocks.blocks["wood"].slot, 0, 1)
        # Force crafting table to be rechecked.
        self.i.select(1)
        self.assertTrue(self.i.recipe)
        self.assertEqual(self.i.recipe_offset, (0, 1))

class TestInventoryIntegration(unittest.TestCase):

    def setUp(self):
        self.i = bravo.inventory.Inventory(0, 45)

    def test_trivial(self):
        pass

    def test_craft_wood_from_log(self):
        self.i.add(bravo.blocks.blocks["log"].slot, 1)
        # Select log from holdables.
        self.i.select(36)
        self.assertEqual(self.i.selected,
            (bravo.blocks.blocks["log"].slot, 0, 1))
        # Select log into crafting.
        self.i.select(1)
        self.assertEqual(self.i.crafting[0],
            (bravo.blocks.blocks["log"].slot, 0, 1))
        self.assertTrue(self.i.recipe)
        self.assertEqual(self.i.crafted[0],
            (bravo.blocks.blocks["wood"].slot, 0, 4))
        # Select wood from crafted.
        self.i.select(0)
        self.assertEqual(self.i.selected,
            (bravo.blocks.blocks["wood"].slot, 0, 4))
        self.assertEqual(self.i.crafting[0], None)
        self.assertEqual(self.i.crafted[0], None)
        # And select wood into holdables.
        self.i.select(36)
        self.assertEqual(self.i.selected, None)
        self.assertEqual(self.i.holdables[0],
            (bravo.blocks.blocks["wood"].slot, 0, 4))
        self.assertEqual(self.i.crafting[0], None)
        self.assertEqual(self.i.crafted[0], None)