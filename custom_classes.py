# Question: You are tasked with creating a Rectangle class with the following requirements:

# An instance of the Rectangle class requires length:int and width:int to be initialized.
# We can iterate over an instance of the Rectangle class 
# When an instance of the Rectangle class is iterated over, we first get its length in the format: {'length': <VALUE_OF_LENGTH>} followed by the width {width: <VALUE_OF_WIDTH>}


class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
    
    # __iter__ is used to make an object into iterable
    def __iter__(self):
        # most of the time __iter__ method return the object itself
        # but here in ourcase the situation is differnt so we need to return iterator
        # when this object is iterated
        yield {"length": self.length}        
        yield {"width": self.width}
    

# Example usage:
rectange = Rectangle(100, 50)

# this loop will iterate for 2 time
# In first iteration it prints the lenght
# And in second iteration it prints the width
for dimension in rectange:
    print(dimension, end=" ")

print("")       # to change line at the last
