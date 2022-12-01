
class V3(object):
    def __init__(self, x , y ,z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return V3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    def __sub__(self, other):
        return V3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return V3(
                self.x * other,
                self.y * other,
                self.z * other
            )
        return V3(
                self.y * other.z - self.z * self.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )

    
    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def lenght(self):
        return( self.x**2 + self.y**2 + self.z**2)**0.5

    def normalize(self):
        return self * (1/self.lenght())


    def __repr__(self):
        return 'V3(%s, %s, %s)' % (self.x, self.y, self.z)
