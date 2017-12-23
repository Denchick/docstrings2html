"""	Генерация списка случайных чисел """
import random
import string
import logging
LOGGER_NAME = 'generators.numbers_generator'
LOGGER = logging.getLogger(LOGGER_NAME)


class NumberGenerator:
    def __init__(self, count, range_):
        if count < 0:
            raise ValueError("Нельзя сгенерировать {} значений".format(count))
        self.count = count
        self.range = range_

    def get_random_number(self):
        return str(random.randint(self.range[0], self.range[1]))

    def generate(self):
        LOGGER.info('Запуск генерации.')
        result = [self.get_random_number() for _ in range(self.count)]
        LOGGER.info('Сгенерировано {} значений в диапазоне {}.'.format(self.count, self.range))
        return result

