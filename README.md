## Requirements

Package requirements are handled using setup.py.
To install the package 
`python setup install`

## Unit Tests

Testing is set up using the built in Unit Test framework in Python

Run the tests with `python setup.py test` in the root directory.

Alternatively you can do `python -m unittest discover -s .`


## Usages

```
>>> import moving_average
>>> ma = moving_average.MovingAverage()
>>> ma.add_action('{"action": "jump", "time": 100}')
>>> ma.add_action('{"action": "jump", "time": 50}')
>>> ma.get_stats()
'[{"action": "jump", "avg": 75.0}]'
```
