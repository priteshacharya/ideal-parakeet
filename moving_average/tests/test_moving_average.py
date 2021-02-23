import unittest
import json
from concurrent.futures import ThreadPoolExecutor

from moving_average import MovingAverage


class MovingAverageTest(unittest.TestCase):
    def setUp(self):
        self.moving_average = MovingAverage()


class WhenAddingAction(MovingAverageTest):
    def test_shouldStoreCountAndTotalTime(self):
        action1 = '{"action": "jump", "time": 100}'
        action2 = '{"action": "jump", "time": 50}'
        action3 = '{"action": "run", "time": 75}'

        expected1 = {'jump': {'count': 1, 'total_time': 100}}
        expected2 = {'jump': {'count': 2, 'total_time': 150}}
        expected3 = {'jump': {'count': 2, 'total_time': 150}, 'run': {'count': 1, 'total_time': 75}}

        self.moving_average.add_action(action1)
        assert self.moving_average.action == expected1, f'output: {self.moving_average.action} expected: {expected1}'

        self.moving_average.add_action(action2)
        assert self.moving_average.action == expected2, f'output: {self.moving_average.action} expected: {expected2}'

        self.moving_average.add_action(action3)
        assert self.moving_average.action == expected3, f'output: {self.moving_average.action} expected: {expected3}'

    def test_shouldHandleMalformedJSON(self):
        action1 = '"action": "jump", "time": 100}'
        self.moving_average.add_action(action1)
        assert self.moving_average.action == {}, f'output: {self.moving_average.action}'

    def test_shouldHandleInvalidInput(self):
        action1 = '{"action1": "jump", "time": 100}'
        self.moving_average.add_action(action1)
        assert self.moving_average.action == {}, f'output: {self.moving_average.action}'

        action2 = '{"action": "jump", "time": "non_numeric"}'
        self.moving_average.add_action(action2)
        assert self.moving_average.action == {}, f'output: {self.moving_average.action}'


class WhenGettingStats(MovingAverageTest):
    def test_shouldReturnAverage(self):
        self.moving_average.action = {'jump': {'count': 2, 'total_time': 150}, 'run': {'count': 1, 'total_time': 75}}

        expected = json.dumps([{'action': 'jump', 'avg': 75.0}, {'action': 'run', 'avg': 75.0}])
        output = self.moving_average.get_stats()
        assert output == expected, f'output: {output} expected: {expected}'


class MultiThreaded(MovingAverageTest):
    def test_shouldNotHaveRaceCondition(self):
        executor = ThreadPoolExecutor(max_workers=10)
        lst = list()
        for i in range(1, 10):
            action1 = '{"action": "jump", "time":' + str(i * 10) + '}'
            lst.append(executor.submit(self.moving_average.add_action, action1))

        for future in lst:
            future.result()

        executor.shutdown()

        expected = {'jump': {'count': 9, 'total_time': 450}}
        assert self.moving_average.action == expected, f'output: {self.moving_average.action} expected: {expected}'
