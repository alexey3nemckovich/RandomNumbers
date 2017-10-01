class LemerNumbersGenerator:

    def __init__(self, r0, a, m):
        self.__r0 = r0
        self.__a = a
        self.__m = m
        self.__lastGeneratedNumber = self.__r0

    def reset(self):
        self.__lastGeneratedNumber = self.__r0

    def set_generator_parameters(self, r0, a, m):
        self.__r0 = r0
        self.__a = a
        self.__m = m

    def next_number(self):
        r = ((self.__lastGeneratedNumber * self.__a) % self.__m) / self.__m
        self.__lastGeneratedNumber = r
        return r
