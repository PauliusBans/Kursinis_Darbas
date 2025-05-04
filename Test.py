import unittest
from tetris import Field, GameStats, ColorChanger


class TestTetrisCore(unittest.TestCase):

    def test_line_clear(self):
        field = Field()
        field.static_screen[19] = [1] * 10
        cleared = field.clear_full_lines()
        self.assertEqual(cleared, 1)

    def test_clear_multiple_lines(self):
        field = Field()
        field.static_screen[18] = [1] * 10
        field.static_screen[19] = [1] * 10
        cleared = field.clear_full_lines()
        self.assertEqual(cleared, 2)

    def test_collision_bottom(self):
        field = Field()
        tetromino = [[1, 1], [1, 1]]
        x, y = 5, 18
        field.get_dxdy(tetromino, x, y)
        self.assertTrue(field.check_colision_y())

    def test_can_place_valid(self):
        field = Field()
        piece = [[1]]
        self.assertTrue(field.can_place(piece, 5, 5))

    def test_can_place_out_of_bounds(self):
        field = Field()
        piece = [[1]]
        self.assertFalse(field.can_place(piece, -1, 0))

    def test_can_place_blocked(self):
        field = Field()
        field.static_screen[0][0] = 1
        piece = [[1]]
        self.assertFalse(field.can_place(piece, 0, 0))

    def test_level_progression(self):
        stats = GameStats()
        for _ in range(30):  # 30 lines = level 3
            stats.update(1)
        self.assertEqual(stats.level, 3)


    def test_rotation_preserves_shape_size(self):
        shape = [[1, 0], [1, 1]]
        rotated = ColorChanger().rotate(shape)
        self.assertEqual(len(rotated), 2)
        self.assertEqual(len(rotated[0]), 2)


if __name__ == "__main__":
    unittest.main()