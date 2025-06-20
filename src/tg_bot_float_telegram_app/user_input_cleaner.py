class UserInputCleaner:
    @staticmethod
    def check_on_index(max_len: int, index: int) -> bool:
        if 0 <= index - 1 < max_len:
            return True
        return False

    @staticmethod
    def clean(text: str) -> str:
        """
        Normalize the user message by converting it to lowercase, stripping whitespace, and removing quotes.

        Args:
            text (str): The user message to normalize.

        Returns:
            str: The normalized text.
        """
        text = text.lower().strip()
        if '"' in text:
            text = text.replace('"', "")
        if "U+2605" in text:
            text = text.replace("U+2605", "")
        return text
