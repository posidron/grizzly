# coding=utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os.path

from ..args import CommonArgs


class ReducerArgs(CommonArgs):

    def __init__(self):
        CommonArgs.__init__(self)
        self.parser.add_argument(
            "--sig",
            help="Signature to reduce (JSON)")
        self.parser.add_argument(
            "--no-harness", action="store_true",
            help="Don't use the harness for sapphire redirection")
        self.parser.add_argument(
            "--any-crash", action="store_true",
            help="Any crash is interesting, not only crashes which match the original first crash")
        self.parser.add_argument(
            "--skip", type=int, default=0,
            help="Return interesting = False for the first n reductions (default: %(default)s)")
        self.parser.add_argument(
            "--repeat", type=int, default=1,
            help="Try to run the testcase multiple times, for intermittent testcases (default: %(default)sx)")
        self.parser.add_argument(
            "--min-crashes", type=int, default=1,
            help="Require the testcase to crash n times before accepting the result. (default: %(default)sx)")
        self.parser.add_argument(
            "--idle-timeout", type=int, default=60,
            help="Number of seconds to wait before polling testcase for idle (default: %(default)s)")
        self.parser.add_argument(
            "--idle-poll", type=int, default=3,
            help="Number of seconds to poll the process before evaluating threshold (default: %(default)s)")
        self.parser.add_argument(
            "--idle-threshold", type=int, default=25,
            help="CPU usage threshold to mark the process as idle (default: %(default)s)")
        self.parser.add_argument(
            "--environ",
            help="File containing line separated environment variables (VAR=value) to be set in the firefox process.")
        self.parser.add_argument(
            "--reduce-file",
            help="Value passed to lithium's --testcase option, needed for testcase cache (default: input param)")
        self.parser.add_argument(
            "--no-cache", action="store_true",
            help="Disable testcase caching")

    def sanity_check(self, args):
        CommonArgs.sanity_check(self, args)

        if not (os.path.isdir(args.input)
                or (os.path.isfile(args.input) and args.input.endswith(".zip"))):
            self.parser.error("Testcase should be a folder or zip")

        if args.sig is not None and not os.path.isfile(args.sig):
            self.parser.error("file not found: %r" % args.sig)

        if args.repeat < 1:
            self.parser.error("'--repeat' value must be positive")

        if args.min_crashes < 1:
            self.parser.error("'--min-crashes' value must be positive")

        if args.environ is not None and not os.path.isfile(args.environ):
            self.parser.error("file not found: %r" % args.environ)

        if args.reduce_file is None:
            args.reduce_file = args.input
