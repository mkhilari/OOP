
from operator import index


class Book: 

    def __init__(self, index, count):
        
        self.index = index 
        self.count = count 
    
    def __eq__(self, other):
        
        return (self.index == other.index) 
    
    def __str__(self):
        
        return f"Book {self.index} with count {self.count} " 

    
def nth_lowest_selling(sales, n): 

    """
    :param elements: (list) List of book sales.
    :param n: (int) The n-th lowest selling element the function should return.
    :returns: (int) The n-th lowest selling book id in the book sales list.
    """ 

    valueCount = {} 

    for value in sales: 

        if (value not in valueCount): 

            valueCount[value] = 0 
        
        valueCount[value] += 1 

    # Create books 
    books = [] 
    
    for value in valueCount: 

        count = valueCount[value] 

        books.append(Book(value, count)) 
    
    books.sort(key = lambda book : book.count) 

    for book in books:

        print(str(book)) 
    
    return books[n - 1].index 

if __name__ == "__main__": 

    print(nth_lowest_selling([5, 4, 3, 2, 1, 5, 4, 3, 2, 5, 4, 3, 5, 4, 5], 2))