class Backpack:

    def __init__(self):
        self.__nr_objects = -1
        self.__max_weight = -1
        self.__objects_list = []

    @property
    def nr_objects(self):
        return self.__nr_objects

    @nr_objects.setter
    def nr_objects(self, new_nr_objects):
        self.__nr_objects = new_nr_objects

    @property
    def max_weight(self):
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, new_max_weight):
        self.__max_weight = new_max_weight

    @property
    def objects_list(self):
        return self.__objects_list

    @objects_list.setter
    def objects_list(self, new_objects_list):
        self.__objects_list = new_objects_list
