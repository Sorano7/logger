from logger import logger as lg
from datetime import datetime
import pytest
from unittest.mock import patch

@pytest.fixture
def runner():
  return lg.runner

@pytest.fixture
def log_data():
  return {
    "level": "DEBUG",
    "msg": "This is a test.",
    "time": datetime(2025, 5, 9, 21, 4, 54),
    "name": "Test",
    "file": "test_logger.py",
    "line": 15,
  }
  
def test_runner_should_print(runner):
  runner.level = 20
  assert runner.should_print("DEBUG") == False
  assert runner.should_print("INFO") == True
  assert runner.should_print("not a key") == False
  
def test_runner_set_level(runner):
  runner.set_level("DEBUG")
  assert runner.level == 10
  runner.set_level("WARNING")
  assert runner.level == 30
  runner.set_level("not a key")
  assert runner.level == 0
  
def test_runner_format_log(runner, log_data):
  level, msg, time, name, file, line = list(log_data.values())
  runner.set_format("time(%H:%M:%S) msg")
  assert runner.format_log(level, msg, time, name, file, line) == "21:04:54 This is a test."
  
  runner.set_format("<level> ++name++ 'msg'")
  assert runner.format_log(level, msg, time, name, file, line) == "<DEBUG> ++Test++ 'This is a test.'"
  
def test_logger_log(runner, capsys):
  runner.set_format("[time(%H:%M)] [level] [file] [name] msg")
  logger_debug = lg.get_logger("Debug", "DEBUG")
  with patch('logger.logger.datetime') as mock_datetime:
    mock_datetime.now.return_value = datetime(2025, 5, 9, 21, 4, 54)
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
    logger_debug.debug("This is a debug.")
    assert capsys.readouterr().out.strip() == "[21:04] [DEBUG] [test_logger.py:49] [Debug] This is a debug."
  
