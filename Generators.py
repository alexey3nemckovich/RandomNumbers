import math
from AttribtutedObject import AttributedObject
from LemerNumbersGenerator import LemerNumbersGenerator


edGenerator = LemerNumbersGenerator(1, 16807, 2 ** 32 - 1)


def get_random_numbers_sum(n):
    res = 0
    for i in range(n):
        res += edGenerator.next_number()
    return res


def get_random_numbers_composition(n):
    res = 1
    for i in range(n):
        res *= edGenerator.next_number()
    return res


class NumbersGenerator:

    def next_number(self):
        raise NotImplementedError()


class EvenNumbersGenerator(NumbersGenerator):

    def __init__(self, parameters):
        self.__a = parameters.a
        self.__b = parameters.b

    def next_number(self):
        r = edGenerator.next_number()
        return self.__a + (self.__b - self.__a) * r


class GaussianNumbersGenerator(NumbersGenerator):

    def __init__(self, parameters):
        self.__m = parameters.m
        self.__s = parameters.s
        self.__sqrt = math.sqrt(2)

    def next_number(self):
        s = get_random_numbers_sum(6)
        return self.__m + self.__s * self.__sqrt * (s - 3)


class ExponentNumbersGenerator(NumbersGenerator):

    def __init__(self, parameters):
        self.__firstFactor = - 1 / parameters.h

    def next_number(self):
        r = edGenerator.next_number()
        return self.__firstFactor * math.log(r)


class HammaNumbersGenerator(NumbersGenerator):

    def __init__(self, parameters):
        self.__firstFactor = - 1 / parameters.h
        self.__c = parameters.c

    def next_number(self):
        m = get_random_numbers_composition(self.__c)
        return self.__firstFactor * math.log(m)


class TriangleNumbersGenerator(NumbersGenerator):

    def __init__(self, parameters):
        self.__a = parameters.a
        self.__b = parameters.b
        if parameters.alg == 'min':
            self.__alg = min
        else:
            self.__alg = max

    def next_number(self):
        r1 = edGenerator.next_number()
        r2 = edGenerator.next_number()
        return self.__a + (self.__b - self.__a) * self.__alg(r1, r2)


class SimpsonNumbersGenerator(EvenNumbersGenerator):

    def __init__(self, parameters):
        args = AttributedObject()
        args.a = parameters.a / 2
        args.b = parameters.b / 2
        EvenNumbersGenerator.__init__(self, args)

    def next_number(self):
        r1 = EvenNumbersGenerator.next_number(self)
        r2 = EvenNumbersGenerator.next_number(self)
        return r1 + r2
