import re
from typing import Callable
from typing import NamedTuple
from typing import Optional


class PatternTranslatorGrouping(NamedTuple):
    regex_pattern: str
    translator: Callable
    regex_flag: Optional[int]


pattern_translator_groupings = [
    PatternTranslatorGrouping(
        r"ensure this value has at least (\d+) characters",
        lambda groups: f"убедитесь, что это значение имеет как минимум {groups[0]} букв",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value has at most (\d+) characters",
        lambda groups: f"убедитесь, что это значение имеет максимум {groups[0]} букв",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure that there are no more than (\d+) digits in total",
        lambda groups: f"убедитесь, что в числе не более {groups[0]} цифр",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure that there are no more than (\d+) decimal places",
        lambda groups: f"убедитесь, что в числе не более {groups[0]} знаков после запятой",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure that there are no more than (\d+) digits before the decimal point",
        lambda groups: f"убедитесь, что в числе не более {groups[0]} цифр до запятой",
        None,
    ),
    PatternTranslatorGrouping(
        r"value is not a valid enumeration member; permitted: (.*)",
        lambda groups: f"значение не является валидным членом перечисления; допустимые значения: {groups[0]}",  # noqa: E501
        re.DOTALL,
    ),
    PatternTranslatorGrouping(
        r"(.+) is not a valid Enum instance",
        lambda groups: f"{groups[0]} не является валидным значением Enum",
        None,
    ),
    (
        r"(.+) is not a valid IntEnum instance",
        lambda groups: f"{groups[0]} не является валидным значением IntEnum",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value has at least (\d+) items",
        lambda groups: f"убедитесь, что это значение имеет как минимум {groups[0]} элементов",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value has at most (\d+) items",
        lambda groups: f"убедитесь, что это значение имеет максимум {groups[0]} элементов",
        None,
    ),
    PatternTranslatorGrouping(
        r"string does not match regex (.*)",
        lambda groups: f"строка не соответствует паттерну регулярного выражения {groups[0]}",
        re.DOTALL,
    ),
    PatternTranslatorGrouping(
        r"(.*) is not callable",
        lambda groups: f"{groups[0]} не является вызываемым объектом",
        re.DOTALL,
    ),
    PatternTranslatorGrouping(
        r"ensure this value is greater than (\d+)",
        lambda groups: f"убедитесь, что это значение больше, чем {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value is greater than or equal to (\d+)",
        lambda groups: f"убедитесь, что это значение больше или равно {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value is less than (\d+)",
        lambda groups: f"убедитесь, что это значение меньше, чем {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value is less than or equal to (\d+)",
        lambda groups: f"убедитесь, что это значение меньше или равно {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"wrong tuple length (\d+), expected (\d+)",
        lambda groups: f"некорректная длина кортежа {groups[0]}, ожидаемая длина {groups[1]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value is a multiple of (\d+)",
        lambda groups: f"убедитесь, что значение делится нацело на {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"ensure this value contains valid import path or valid callable: (.*)",
        lambda groups: f"убедитесь в том, что это значение содержит валидный путь для импорта или вызываемый объект: {groups[0]}",  # noqa: E501
        re.DOTALL,
    ),
    PatternTranslatorGrouping(
        r"URL invalid, extra characters found after valid URL: .*",
        lambda groups: f"невалидный URL, найдены дополнительные символы после валидного URL: {groups[0]}",  # noqa: E501
        re.DOTALL,
    ),
    PatternTranslatorGrouping(
        r"uuid version (\d+) expected",
        lambda groups: f"ожидалась версия uuid {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"instance of (.+) expected",
        lambda groups: f"ожидался экземляр класса {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"subclass of (.+) expected",
        lambda groups: f"ожидался субкласс класса {groups[0]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"instance of (.+), tuple or dict expected",
        lambda groups: f"ожидался экземпляр класса {groups[0]}, кортеж или словарь",
        None,
    ),
    PatternTranslatorGrouping(
        r"value is not a valid color: .*",
        lambda groups: f"значение не является валидным цветом: {groups[0]}",
        re.DOTALL,
    ),
    PatternTranslatorGrouping(
        r"Length for a (\w) card must be (\d+)",
        lambda groups: f"длина номера карты {groups[0]} должна быть {groups[1]}",
        None,
    ),
    PatternTranslatorGrouping(
        r"could not interpret byte unit: .*",
        lambda groups: f"невозможно интерпретировать единицу измерения байтов: {groups[0]}",
        re.DOTALL,
    ),
    PatternTranslatorGrouping(
        r"file or directory at path ([\w\\/]+) does not exist",
        lambda groups: f"файл или папка в пути {groups[0]} не существует",
        None,
    ),
    PatternTranslatorGrouping(
        r"path ([\w\\/]+) does not point to a file",
        lambda groups: f"путь {groups[0]} не указывает на файл",
        None,
    ),
    PatternTranslatorGrouping(
        r"path ([\w\\/]+) does not point to a directory",
        lambda groups: f"путь {groups[0]} не указывает на папку",
        None,
    ),
]
