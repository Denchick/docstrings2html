"""	Генерация списка случайных строк """
import random
import string
import logging
LOGGER_NAME = 'generators.strings_generator'
LOGGER = logging.getLogger(LOGGER_NAME)


class StringGenerator:
    def __init__(self, has_digits, has_upper, has_lower, has_special, count, size):
        self.alphabet = self.get_alphabet(has_digits, has_upper, has_lower, has_special)
        self.count = count
        self.size = size

    def get_random_string(self):
        """ Генератор случайных символов из списка chars диапазона size """
        return ''.join(random.choice(self.alphabet) for _ in range(
            random.randint(self.size[0], self.size[1])))

    @staticmethod
    def get_alphabet(has_digits, has_upper, has_lower, has_special):
        """ Формирует алфавит для генерации строк """
        chars = ''
        if has_digits:
            chars += string.digits
        if has_lower:
            chars += string.ascii_lowercase
        if has_upper:
            chars += string.ascii_uppercase
        if has_special:
            chars += string.punctuation
        if not has_digits and not has_lower and not has_upper and not has_special:
            chars = string.ascii_letters + string.digits + string.punctuation  # = digits + upper + lower + special
            LOGGER.info('Строки будут состоять из цифр, строчных и прописных букв, специальных символов.')
        return chars

    def generate(self):
        """ Генератор случайных строк """
        LOGGER.info('Запуск генерации.')
        result = [self.get_random_string() for _ in range(self.count)]
        LOGGER.info('Сгенерировано {} строк длинами {}.'.format(self.count, self.size))
        return result
