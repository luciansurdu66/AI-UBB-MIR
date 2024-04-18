class Object:

    def __init__(self):
        self.__position = -1
        self.__weight = -1
        self.__value = -1

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        self.__position = new_position

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, new_weight):
        self.__weight = new_weight

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return f"Item position: {self.__position}, value: {self.__value}, weight: {self.__weight} "
