import json
import logging
import numbers
from threading import Lock


class MovingAverage(object):
    """Class to calculate moving average"""

    def __init__(self):
        """
        action to store count and total_time for each action
        """
        self.action = {}
        self.lock = Lock()

    def add_action(self, action_str: str) -> None:
        """
        This adds action to the action dictionary and maintains count and total_time for each action
        :param input action containing action name and time:
        :return: None
        """
        try:
            action_dict = json.loads(action_str)
            if 'action' in action_dict and 'time' in action_dict and isinstance(action_dict['time'], numbers.Number):
                action_name = action_dict['action']
                with self.lock:
                    if action_name in self.action:
                        self.action[action_name]['count'] += 1
                        self.action[action_name]['total_time'] += action_dict['time']
                    else:
                        self.action[action_name] = {'count': 1,
                                               'total_time': action_dict['time']}
            else:
                logging.debug(f'Invalid data format: {action_dict}')
        except ValueError as e:
            logging.debug(f'Value error: {e}')

    def get_stats(self) -> str:
        """
        This method calculates average for all the action
        :return: returns serialized json of all action with average
        """
        result = []
        with self.lock:
            for key in self.action:
                value = self.action[key]
                stat = {'action': key, 'avg': value['total_time'] / value['count']}
                result.append(stat)
        return json.dumps(result)
