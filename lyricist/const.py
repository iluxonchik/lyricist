def constant(func):
    """ Decorator used to emulate constant values """
    
    def fset(self, value):
        raise TypeError("Cannot modify the value of a constant.")

    def fget(self):
        return func()
    
    return property(fget, fset)
