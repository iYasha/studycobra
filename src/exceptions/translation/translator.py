import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from exceptions.translation.pattern_translator_groupings import (
    PatternTranslatorGrouping,
)


class PydanticErrorTranslator:
    """
    Класс для получения перевода ошибок Pydantic на русский
    """

    def __init__(
        self,
        error_translations: Dict[str, str],
        pattern_translator_groupings: List[PatternTranslatorGrouping],
    ) -> None:
        self.error_translations = error_translations
        self.pattern_translator_groupings = pattern_translator_groupings

    def _search_for_translation(self, message: str) -> Optional[str]:
        """
        Сопоставить ошибку с переводом, используя регулярки.
        Метод используется для перевода ошибок, строящихся по паттернам. Например,
        "ensure this value has at least {limit_value} characters"
        """
        for pattern_translator_grouping in self.pattern_translator_groupings:
            pattern, translator, regex_flag = pattern_translator_grouping

            if regex_flag:
                search_result = re.search(pattern, message, regex_flag)
            else:
                search_result = re.search(pattern, message)

            if search_result:
                return translator(groups=search_result.groups())

        return None

    def _get_message_translation(self, message: str) -> str:
        translation = self.error_translations.get(message)

        if not translation:
            translation = self._search_for_translation(message)

        return translation if translation else message

    def translate(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        translated_errors: List[Dict[str, str]] = []

        for error in errors:
            message = self._get_message_translation(error["msg"])
            error["msg"] = message
            translated_errors.append(error)

        return translated_errors
