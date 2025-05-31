import unittest


class VerboseTestResult(unittest.TextTestResult):
    # 256-color ANSI codes (foreground)
    GREEN = "\033[38;5;40m"  # True green
    RED = "\033[38;5;196m"  # Bright red
    YELLOW = "\033[38;5;220m"  # Bright yellow
    CYAN = "\033[38;5;45m"  # Bright cyan
    RESET = "\033[0m"

    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"{self.GREEN}{test} => PASSED{self.RESET}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"{self.RED}{test} => FAILED{self.RESET}")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"{self.RED}{test} => ERROR{self.RESET}")

    def printErrors(self):
        if self.failures:
            print(f"\n{self.YELLOW}Failures:{self.RESET}")
            for test, err in self.failures:
                print(f"{self.RED}{test}{self.RESET}")
                print(f"{self.YELLOW}{err}{self.RESET}")
        if self.errors:
            print(f"\n{self.YELLOW}Errors:{self.RESET}")
            for test, err in self.errors:
                print(f"{self.RED}{test}{self.RESET}")
                print(f"{self.YELLOW}{err}{self.RESET}")


class VerboseTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return VerboseTestResult(self.stream, self.descriptions, self.verbosity)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("src")
    runner = VerboseTestRunner(verbosity=2)
    runner.run(suite)
