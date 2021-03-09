"""
Домашнее задание №1
Функции и структуры данных
"""


def power_numbers(*args):
    """
    функция, которая принимает N целых чисел,
    и возвращает список квадратов этих чисел
    """
    return [i ** 2 for i in args]


# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"


def is_prime(n):
    if n % 2 == 0:
        return False
    d = 3
    while d ** 2 <= n and n % d != 0:
        d += 2
    return d ** 2 > n


def filter_numbers(array, numbers_filter):
    """
    функция, которая на вход принимает список из целых чисел,
    и возвращает только чётные/нечётные/простые числа
    (выбор производится передачей дополнительного аргумента)
    """
    if numbers_filter == 'odd':
        return [i for i in array if i % 2 == 0]
    elif numbers_filter == 'even':
        return [i for i in array if i % 2 == 1]
    elif numbers_filter == 'prime':
        return list(filter(is_prime, array))
