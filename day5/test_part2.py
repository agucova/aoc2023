from part2 import find_interval_gaps, map_interval, BinarySearchTree

# Tests
def test_find_interval_gaps():
    assert find_interval_gaps(range(0, 10), [range(2, 5), range(7, 9)]) == [
        range(0, 2),
        range(5, 7),
        range(9, 10),
    ]
    assert find_interval_gaps(range(0, 10), [range(0, 10)]) == []
    assert find_interval_gaps(range(5, 15), [range(0, 10)]) == [range(10, 15)]
    assert find_interval_gaps(range(50, 100), [range(0, 10)]) == [range(50, 100)]
    assert find_interval_gaps(range(80, 150), [range(0, 90)]) == [
        range(90, 150),
    ]


def test_map_interval():
    mapping = BinarySearchTree()
    mapping.insert(range(0, 10), range(10, 20))

    assert map_interval(range(0, 10), mapping) == [range(10, 20)]
    assert map_interval(range(5, 15), mapping) == [range(10, 15), range(15, 20)]
    assert map_interval(range(0, 20), mapping) == [range(10, 20), range(10, 20)]
    assert map_interval(range(0, 5), mapping) == [range(10, 15)]

    mapping.insert(range(20, 30), range(30, 40))
    assert map_interval(range(0, 10), mapping) == [range(10, 20)]
    assert map_interval(range(25, 35), mapping) == [range(30, 35), range(35, 40)]
