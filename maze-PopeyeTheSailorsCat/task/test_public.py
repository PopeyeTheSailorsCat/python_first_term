import pytest
from .find_count_steps import count_steps_to_exit, on_border, possible_neighbours


class Case:
    def __init__(self, name: str, input: list, expected: int):
        self._name = name
        self.expected = expected
        self.input = input

    def __str__(self) -> str:
        return 'test_{}'.format(self._name)


TEST_CASES_FOR_COUNT_STEPS = [
    Case(name='simple', input=([[0, 0, 0, 0],
                                [0, 1, 1, 1],
                                [0, 1, 0, 0]], (1, 1)), expected=2),
    Case(name='no_steps', input=([[0, 0, 0, 0],
                                  [0, 1, 0, 1],
                                  [0, 0, 0, 0]], (1, 1)), expected=0),
    Case(name='without_exit', input=([[0, 0, 0, 0, 0],
                                      [0, 1, 1, 1, 0],
                                      [0, 1, 0, 0, 0],
                                      [0, 0, 0, 0, 0]], (1, 1)), expected=0),
    Case(name='cycle_with_exit', input=([[0, 0, 0, 0, 0],
                                         [0, 1, 1, 1, 0],
                                         [0, 1, 0, 1, 0],
                                         [0, 1, 1, 1, 0],
                                         [0, 0, 0, 1, 0]], (1, 1)), expected=6),
    Case(name='cycle_without_exit', input=([[0, 0, 0, 0, 0],
                                            [0, 1, 1, 1, 0],
                                            [0, 1, 0, 1, 0],
                                            [0, 1, 1, 1, 0],
                                            [0, 0, 0, 0, 0]], (1, 1)), expected=0)
]

TEST_CASES_FOR_BORDER = [
    Case(name='in', input=(5, 5, (6, 6)), expected=False),
    Case(name='out', input=(5, 5, (3, 3)), expected=False),
    Case(name='left', input=(5, 4, (4, 3)), expected=True),
    Case(name='right', input=(4, 5, (2, 4)), expected=True),
    Case(name='up', input=(5, 5, (0, 3)), expected=True),
    Case(name='down', input=(5, 5, (2, 0)), expected=True)
]

TEST_CASES_FOR_NEIGHBOURS = [
    Case(name='simple', input=(2, 2), expected=[(2, 3), (3, 2), (2, 1), (1, 2)])
]


@pytest.mark.parametrize('exit', TEST_CASES_FOR_COUNT_STEPS, ids=str)
def test_count_steps_to_exit(exit: Case) -> None:
    answer = count_steps_to_exit(*exit.input)
    assert answer == exit.expected


@pytest.mark.parametrize('border', TEST_CASES_FOR_BORDER, ids=str)
def test_on_border(border: Case) -> None:
    answer = on_border(*border.input)
    assert answer == border.expected


@pytest.mark.parametrize('neighbours', TEST_CASES_FOR_NEIGHBOURS, ids=str)
def test_possible_neighbours(neighbours: Case) -> None:
    answer = possible_neighbours(neighbours.input)
    assert answer == neighbours.expected
