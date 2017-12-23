import csv
import os
import shutil
import logging
import sys
import tempfile

from . import extremum, piece, utils

LOGGER_NAME = 'map_reduce.map_reduce'
LOGGER = logging.getLogger(LOGGER_NAME)


class MapReduce:
    def __init__(self, input_filename: str,
                 output_filename: str,
                 separator: str,
                 temp_directory: str,
                 size_of_one_piece: int,
                 reverse: bool,
                 debug: bool,
                 mode: str,
                 **kwargs):
        """ Конcтруктор класса MapReduce.
        
        Args:
            input_filename(str): название файла для сортировки или None, если данные поступают с stdin.
            output_filename(str): название выходного файла или None, если данные идут в stdout.
            separator(str): разделитель между значениями в сортируемом файле.
            temp_directory(str): папка для хранения временных файлов.
            size_of_one_piece(int): примерное место(нижняя граница) для хранения одного куска файла в памяти.
            case_sensitive(bool): если сортируются строки, учитывается их регистр, иначе параметр не влияет на работу.
            reverse(bool): сортировать данные в обратном порядке
            debug(bool): режим дебаг. logging.debug пишется в лог-файл, temp_directory(если указан не None) не удаляется
            """
        LOGGER.info("Initialization of meta data.")
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.separator = separator

        self.temp_directory_object = tempfile.TemporaryDirectory() if not temp_directory else None
        self.temp_directory = self.temp_directory_object.name if not temp_directory else temp_directory

        self.size_of_one_piece = size_of_one_piece
        if self.size_of_one_piece is None:
            self.size_of_one_piece = utils.determine_size_of_one_piece()
            LOGGER.info("Size of one piece file chosen as {0}.".format(self.size_of_one_piece))

        self.reverse = reverse
        self.debug = debug

        self.mode = mode
        self.initialization_modes_variables(kwargs)

        self.pieces = []

        self.cache_for_output = []
        self.cache_size = 0

        LOGGER.info("OK. Let's start to sorting.")
        self.run_sorting()

    def initialization_modes_variables(self, **kwargs):
        if self.mode == 'numbers':
            self.separator = kwargs['separator']
        elif self.mode == 'strings':
            self.separator = kwargs['separator']
            self.case_sensitive = kwargs['case_sensitive']
        elif self.mode == 'csv':
            self.delimiter = kwargs['delimiter']
            self.column = kwargs['column']
            self.reader_obj = csv.reader(self.input_filename)
        else:
            raise AttributeError("Unrecognised mode: {0}".format(self.mode))

    def run_sorting(self):
        self.mapper()
        self.reducer()
        self.clean_up()

    @property
    def pieces_is_empty(self):
        """ Проверяет, остались ли еще хоть в одном кусочке элементы.
        
        Returns:
            True, если есть хоть один непрочитанный до конца кусочек, иначе False.
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
        if self.mode == 'numbers':
            if utils.is_number(obj):
                try:
                    return int(obj)
                except ValueError:
                    return float(obj)
            else:
                raise RuntimeError('Got not a number in "numbers" mode: {0}'.format(obj))

        elif self.mode == 'strings':
            if isinstance(obj, str):
                if self.case_sensitive:
                    return obj
                return obj.lower()
            else:
                raise RuntimeError('Got not a string in "strings" mode: {0}'.format(obj))
        elif self.mode == 'csv':
            return obj[self.column]
        else:
            raise RuntimeError('kek')

        raise TypeError("I can't compare objects' {0} type!".format(type(obj)))

    def mapper(self):
        """ Разделяет большой файл на несколько файлов, записывая их в папку temp_directory. 
        Если такой папки нет, то она будет создана.
        Внутри каждого кусочка значения разделяются переносом строки и сортируются в соответствии с параметрами.
        Размер одного кусочка не меньше, чем size_of_one_piece байт.
                    
        Raises:
            RuntimeError: если папка для временных файлов оказалась непуста. 
        """
        LOGGER.info('Mapper is start.')
        if not isinstance(self.reverse, bool):
            raise TypeError("Reverse flag must be a bool, but got {0}:{1}".format(type(self.reverse), self.reverse))

        os.makedirs(self.temp_directory, exist_ok=True)

        with self.get_opened_file_in_mapper() as source_file:
            LOGGER.info('Mapping...')
            if self.mode == 'csv':
                self.reader_obj = csv.reader(source_file, delimiter=self.delimiter)
                self.initialization_header(source_file)
            while True:
                piece_data = self.get_next_data_piece(source_file)
                if not piece_data:
                    LOGGER.info('Reached the end of file.')
                    break
                piece_data = self.get_sorted_piece_data(piece_data)
                self.create_new_piece(piece_data)
        LOGGER.info('Mapping is done!')

    def create_new_piece(self, piece_data):
        if self.mode == 'csv':
            raise NotImplementedError
        else:
            self.pieces.append(
                piece.Piece(len(self.pieces), piece_data, self.temp_directory))

    def get_sorted_piece_data(self, piece_data):
        sorted_data = sorted(piece_data.split(self.separator), reverse=self.reverse, key=self.key_sort_piece)
        if self.mode == 'csv':
            self.separator.join([self.delimiter.join(i) for i in sorted_data])
        return self.separator.join(sorted_data)

    def initialization_header(self, csvfile):
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csvfile.read(2048))
        csvfile.seek(0)

        self.header = self.reader_obj.__next__() if has_header else None

    def get_opened_file_in_mapper(self):
        if self.input_filename is not None:
            return open(self.input_filename, 'r')
        return sys.stdin

    def reducer(self):
        """ Сливает много отсортированных файлов обратно в 1 файл. 
        Среди всех кусков смотрится верхний еще не добавленный в файл элемент, и из них выбирается экстремум - 
        наибольший или наименьший элемент, в зависимости от настройки алгоритма, а в соответствующем куске указатель
        на верхний элемент сдвигается на следующий после него элемент. Если кусок прочитан до конца, то он становится 
        None. Алгоритм заканчивает свою работу, когда все кусочки были дочитаны до конца, то есть стали None.
        """
        LOGGER.info('Reducer is  start...')
        with self.get_opened_file_in_reducer() as output:
            while True:
                LOGGER.info("Let's find an extremum among pieces.")
                extr = self.get_extremum_among_pieces()
                if extr is None or extr.data is None:
                    LOGGER.info("All of pieces is empty.")
                    break
                LOGGER.info("Extremum is {0}".format(extr.data))
                self.write_data_to_output(extr.data, output)
                extr.piece_obj.delete_up_element(self.temp_directory, self.separator)
                if extr.piece_obj.is_empty(self.temp_directory):
                    self.pieces[extr.piece_obj.index] = None
        LOGGER.info('Reducing is done!')

    def get_opened_file_in_reducer(self):
        if self.output_filename:
            return open(self.output_filename, 'w')
        return sys.stdout

    def write_data_to_output(self, data, file):
        if self.mode == 'csv':
            data = self.delimiter.join(data)
        self.cache_size += sys.getsizeof(data)
        self.cache_for_output.append(str(data))

        if self.cache_size >= self.size_of_one_piece / 2:
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
            element = piece.get_up_element(self.temp_directory, self.separator, self.mode)
            if self.mode == 'csv':

                pass
                ## преобразуем в список


            # костыль
            expression = extr is None or self.key_sort_piece(extr.data) < self.key_sort_piece(element) if \
                self.reverse else extr is None or self.key_sort_piece(extr.data) > self.key_sort_piece(element)
            if expression:
                extr = extremum.Extremum(element, piece)
        return extr

    def get_next_data_piece(self, file):
        """ Возвращает кусок данных из открытого на чтение файла file, размера 
        минимум size_of_piece, пока не встретит separator или EOF.

        Args:
            file(readable object): файл, открытый на чтение. В общем случае, объект, для которого определен метод read().

        Returns:    
            Строку str - следующий фрагмент файла.

        Raises:
            AttributeError: если file не имеет атрибут read().
            """
        if self.mode == 'csv':
            try:
                return self.reader_obj.__next__()
            except StopIteration:
                return ''

        try:
            result = file.read(self.size_of_piece)
            if result.endswith(self.separator):
                result = result[:-len(self.separator)]
            else:
                current = file.read(1)
                while current != '' and current != self.separator:
                    result += current
                    current = file.read(1)
            return result
        except AttributeError:
            raise AttributeError("'file' attribute must have a read() method")

    def clean_up(self):
        if self.temp_directory_object is not None:
            self.temp_directory_object.cleanup()
        elif not self.debug:
            shutil.rmtree(self.temp_directory)
            LOGGER.info("Delete temp files.")
