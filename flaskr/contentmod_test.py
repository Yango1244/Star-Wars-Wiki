from contentmod import contentChecker
import unittest
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch
import google
import pytest

assert contentChecker('mibun') == False
assert contentChecker('hello') == True
