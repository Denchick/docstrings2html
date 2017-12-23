"""Модуль со вспомогательными функциями"""
import cProfile
import os


def is_number(value):
    """ Проверяет, является ли value целым числом или вещественным. 

    Args:
        value (object): значение, которое нужно проверить.
         
    Returns:
        True, если value int или float, иначе False.
    """
    try:
        float(value)
        return True
    except Exception:
        return False







def determine_size_of_one_piece():
    try:
        import psutil
        return psutil.virtual_memory().free // 10
    except ImportError:
        return 2 * 1024 * 1024 * 1024 // 10

