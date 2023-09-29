import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class HiddenPrintsHiddenErrors:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        # This is a natural exit leaving the scope instead of an error/exception happening
        if exc_type is None and exc_val is None and exc_tb is None:
            sys.stdout.close()
            sys.stdout = self._original_stdout