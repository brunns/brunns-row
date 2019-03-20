# encoding=utf-8
import logging

import six

logger = logging.getLogger(__name__)

six.add_move(six.MovedModule("mock", "mock", "unittest.mock"))
