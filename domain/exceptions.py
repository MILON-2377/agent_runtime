class InvalidRunTransition(Exception):
    def __init__(self, current_status: str, target_status: str) -> None:
        self.current_status = current_status
        self.target_status = target_status

        message = (f"Invalid Run transition: ", f"{current_status} -> {target_status}")

        super().__init__(message)
