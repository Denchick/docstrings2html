import os
import shutil
import logging
import sys
import tempfile

from . import extremum, piece, utils

LOGGER_NAME = 'map_reduce.map_reduce'
LOGGER = logging.getLogger(LOGGER_NAME)


class MapReduce:
    def __init__(self,
                 input_filename: str,
                 output_filename: str,
                 separator: str,
                 temp_directory: str,
                 size_of_one_piece: int,
                 ignore_case: bool,
                 numeric_sort: bool,
                 reverse: bool,
                 debug: bool):
        """ Конcтруктор класса MapReduce.

        Args:
            input_filename(str): название файла для сортировки или None,
                если данные поступают с stdin.
            output_filename(str): название выходного файла или None,
                если данные идут в stdout.
            separator(str): разделитель между значениями в сортируемом файле.
            temp_directory(str): папка для хранения временных файлов.
            size_of_one_piece(int): примерное место(нижняя граница) для
                хранения одного куска файла в памяти.
            ignore_case(bool): если сортируются строки, то регистр
                не учитывается, иначе параметр не влияет на работу.
            numeric_sort(bool): сортировать значения как числа
            reverse(bool): сортировать данные в обратном порядке
            debug(bool): режим дебаг. logging.debug пишется в лог-файл,
                temp_directory(если указан не None) не удаляется
            """
        LOGGER.info("Initialization of meta data.")
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.separator = separator

        self.temp_directory_object = tempfile.TemporaryDirectory() \
            if not temp_directory else None
        self.temp_directory = self.temp_directory_object.name \
            if not temp_directory else temp_directory

        self.size_of_one_piece = size_of_one_piece
        if self.size_of_one_piece is None:
            self.size_of_one_piece = utils.determine_size_of_one_piece()
            LOGGER.info("Size of one piece file chosen as {0}.".format(
                self.size_of_one_piece))

        self.reverse = reverse
        self.debug = debug

        self.numeric_sort = numeric_sort
        self.ignore_case = ignore_case

        self.pieces = []

        self.cache_for_output = []
        self.cache_size = 0

        LOGGER.info("OK. Let's start to sorting.")
        self.run_sorting()

    def run_sorting(self):
        self.mapper()
        self.reducer()
        self.clean_up()

    @property
    def pieces_is_empty(self):
        """ Проверяет, остались ли еще хоть в одном кусочке элементы.

        Returns:
            True, если есть хоть один непрочитанный до конца кусочек,
            иначе False.
        """
        for p in self.pieces:
            if p is not None:
                return False
        return True

    def key_sort_piece(self, obj):
        """ Ключ для сортировки

        Returns:
             comparable object.
        """
        if self.numeric_sort:
            if utils.is_number(obj):
                try:
                    return int(obj)
                except ValueError:
                    return float(obj)
            else:
                raise RuntimeError(
                    'Got not a number in "numbers" mode: {0}'.format(obj))

        else:
            if isinstance(obj, str):
                if self.ignore_case:
                    return obj.lower()
                return obj
            else:
                raise RuntimeError(
                    'Got not a string in "strings" mode: {0}'.format(obj))

    def mapper(self):
        """ Разделяет большой файл на несколько файлов, записывая их в
        папку temp_directory.
        Если такой папки нет, то она будет создана.
        Внутри каждого кусочка значения разделяются переносом строки и
        сортируются в соответствии с параметрами.
        Размер одного кусочка не меньше, чем size_of_one_piece байт.

        Raises:
            RuntimeError: если папка для временных файлов оказалась непуста.
        """
        LOGGER.info('Mapper is start.')
        if not isinstance(self.reverse, bool):
            raise TypeError(
                "Reverse flag must be a bool, but got {0}:{1}".format(
                    type(self.reverse), self.reverse))

        os.makedirs(self.temp_directory, exist_ok=True)

        with open(self.input_filename, 'r') \
                if self.input_filename is not None else sys.stdin as source:
            LOGGER.info('Mapping...')
            while True:
                piece_data = utils.get_next_data_piece(
                    source, self.size_of_one_piece, self.separator)
                if not piece_data:
                    LOGGER.info('Reached the end of file.')
                    break
                piece_data = self.separator.join(
                    sorted(piece_data.split(self.separator),
                           reverse=self.reverse,
                           key=self.key_sort_piece))
                self.pieces.append(
                    piece.Piece(len(self.pieces),
                                piece_data,
                                self.temp_directory))
        LOGGER.info('Mapping is done!')

    def reducer(self):
        """ Сливает много отсортированных файлов обратно в 1 файл.
        Среди всех кусков смотрится верхний еще не добавленный в файл элемент,
        и из них выбирается экстремум - наибольший или наименьший элемент,
        в зависимости от настройки алгоритма, а в соответствующем куске
        указатель на верхний элемент сдвигается на следующий после него
        элемент. Если кусок прочитан до конца, то он становится  None.
        Алгоритм заканчивает свою работу, когда все кусочки были дочитаны до
        конца, то есть стали None.
        """
        LOGGER.info('Reducer is  start...')
        with open(self.output_filename, 'w') if self.output_filename \
                else sys.stdout as output:
            while True:
                LOGGER.info("Let's find an extremum among pieces.")
                extr = self.get_extremum_among_pieces()
                if extr is None or extr.data is None:
                    LOGGER.info("All of pieces is empty.")
                    break
                LOGGER.info("Extremum is {0}".format(extr.data))
                self.write_data_to_output(extr.data, output)
                extr.piece_obj.delete_up_element(self.temp_directory,
                                                 self.separator)
                if extr.piece_obj.is_empty(self.temp_directory):
                    self.pieces[extr.piece_obj.index] = None
            self.write_data_to_output('', output, reducer_is_end=True)
        LOGGER.info('Reducing is done!')

    def write_data_to_output(self, data, file, reducer_is_end=False):
        self.cache_size += sys.getsizeof(data)
        self.cache_for_output.append(str(data))

        if reducer_is_end or self.cache_size >= self.size_of_one_piece / 2:
            cache = self.separator.join(self.cache_for_output)
            self.cache_size = 0
            self.cache_for_output = []
            print(cache, end=self.separator, file=file)

    def get_extremum_among_pieces(self):
        """
        Ищет экстремум среди всех верхних элементов кусков
        Returns:
            Extremum obj: если экстремум найден
            None: если экстремума нет, то есть все куски прочитаны до конца
        """
        extr = None  # Найдем экстремум.
        for piece in self.pieces:
            if piece is None:
                continue
            element = piece.get_up_element(self.temp_directory,
                                           self.separator)
            if self.get_comparison(extr, element):
                extr = extremum.Extremum(element, piece)
        return extr

    def get_comparison(self, extr, element):
        if extr is None:
            return True
        if self.reverse:
            return self.key_sort_piece(
                extr.data) < self.key_sort_piece(element)
        return self.key_sort_piece(extr.data) > self.key_sort_piece(element)

    def clean_up(self):
        """
        Удаляет после работы утилиты временные файлы
        """
        if self.temp_directory_object is not None:
            self.temp_directory_object.cleanup()
        elif not self.debug:
            shutil.rmtree(self.temp_directory)
            LOGGER.info("Temp files are deleted.")
