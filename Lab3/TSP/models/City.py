class City:
    
    def __init__(self):
        self.__index = None
        self.__x = None
        self.__y = None
        
    @property
    def index(self):
        return self.__index
    
    @index.setter
    def index(self, index):
        self.__index = index
        
    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, x):
        self.__x = x
        
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, y):
        self.__y = y
        
    def __str__(self):
        return f'City {self.__index} having coordinates: ({self.__x}, {self.__y})'