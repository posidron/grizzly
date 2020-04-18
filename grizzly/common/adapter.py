# coding=utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import abc
import os

import six

from .storage import TestFile

__all__ = ("Adapter", "AdapterError")
__author__ = "Tyson Smith"
__credits__ = ["Tyson Smith"]


class AdapterError(Exception):
    """The base class for exceptions raised by an Adapter"""


@six.add_metaclass(abc.ABCMeta)
class Adapter(object):
    HARNESS_FILE = os.path.join(os.path.dirname(__file__), "harness.html")
    IGNORE_UNSERVED = True  # Only report test cases with served content
    NAME = None  # must be set to a unique 'str' by subclass
    RELAUNCH = 0  # maximum iterations between Target relaunches (<1 use default)
    TEST_DURATION = 30  # maximum execution time per test

    #############################
    # Built-ins do NOT overload!
    #############################

    def __init__(self):
        if self.NAME is None:
            raise NotImplementedError("NAME member must be set by subclass")
        assert isinstance(self.NAME, str), "NAME must be a 'str'"
        self._harness = None
        self.fuzz = dict()
        self.monitor = None
        # remaining can be used to indicate the number of TestCases remaining to process
        self.remaining = None

    def cleanup(self):
        """Automatically called once at shutdown.

        Args:
            None

        Returns:
            None
        """
        if self._harness is not None:
            self._harness.close()
            self._harness = None
        self.shutdown()

    def enable_harness(self, file_path=None):
        """Enable use of a harness during fuzzing. By default no harness is used.

        Args:
            file_path (str): Path to file to use as a harness. If None the default harness is used.

        Returns:
            None
        """
        if self._harness is not None:
            self._harness.close()
        self._harness = TestFile.from_file(
            self.HARNESS_FILE if file_path is None else file_path,
            "grizzly_fuzz_harness.html")

    def get_harness(self):
        """Get the harness. Used internally by Grizzly.

        Args:
            None

        Returns:
            TestFile: The current harness
        """
        return self._harness

    #############################
    # Methods to overload
    #############################

    @abc.abstractmethod
    def generate(self, testcase, server_map):
        """Automatically called. Populate testcase here.

        Args:
            testcase (TestCase): TestCase intended to be populated
            server_map (ServerMap): A ServerMap

        Returns:
            None
        """

    def on_served(self, testcase, served):
        """Optional. Automatically called after a test case is successfully served.

        Args:
            testcase (TestCase): TestCase that was served
            served (list): A list of file names served from testcase

        Returns:
            None
        """

    def on_timeout(self, testcase, served):
        """Optional. Automatically called if timeout occurs attempting to serve a test case.

        Args:
            testcase (TestCase): TestCase that was served
            served (list): A list of file names served from testcase

        Returns:
            None
        """
        self.on_served(testcase, served)

    def pre_launch(self):
        """Optional. Automatically called before launching the Target.

        Args:
            None

        Returns:
            None
        """

    def setup(self, input_path, server_map):
        """Optional. Automatically called once at startup.

        Args:
            input_path (str): Points to a file or directory passed by the user.
                              None is passed by default.
            server_map (ServerMap): A ServerMap

        Returns:
            None
        """

    def shutdown(self):
        """Optional. Automatically called once at shutdown.

        Args:
            None

        Returns:
            None
        """
