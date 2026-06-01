class PrintSummary:
    def __init__(self):
        self._print_height = 0
        self._print_errors = []

    @property
    def print_height(self) -> float:
        return self._print_height
    @print_height.setter
    def print_height(self, value: float) -> None:
        self._print_height = value

    def add_error(self, error: str):
        self._print_errors.append(error)
    def get_errors(self):
        return self._print_errors