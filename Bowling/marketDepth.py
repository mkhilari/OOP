
from enum import Enum 

class NotFoundException(Exception): 
    pass 

class DuplicateException(Exception): 
    pass 

class Action(Enum): 

    ADD = 1 
    MOD = 2 
    DEL = 3 

class Diff: 

    def __init__(self, price, vol, action): 

        self.price = price 
        self.vol = vol 
        self.action = action 

    def __repr__(self): 

        return f"d: {self.action} {self.vol}@{self.price})" 


class Depth: 

    def __init__(self):
        
        self.priceVols = {} 
    
    def apply_actions(self, actions): 

        try: 

            return self.applyDiffs(actions) 
        except Exception as e: 

            print(f"A {e.__class__} occured ") 

    def applyDiffs(self, diffs): 

        """
        actions: a list of Diff actions
        returns: a map of price/vol
        """ 

        for diff in diffs: 

            if (diff.action == Action.ADD): 

                self.add(diff.price, diff.vol) 
            
            elif (diff.action == Action.DEL): 

                self.delete(diff.price) 
            
            elif (diff.action == Action.MOD):

                self.modify(diff.price, diff.vol) 
        
        return self.priceVols 

    
    def add(self, price, vol): 

        if (price in self.priceVols): 

            raise DuplicateException() 
        
        self.priceVols[price] = vol 
    
    def delete(self, price): 

        if (price not in self.priceVols): 

            raise NotFoundException() 
        
        self.priceVols.pop(price) 
    
    def modify(self, price, vol): 

        self.delete(price) 
        self.add(price, vol) 


depth = Depth() 

actions = [Diff(100, 10, Action.ADD),
           Diff(101, 10, Action.ADD),
           Diff(102, 10, Action.ADD),
           Diff(103, 10, Action.ADD),
           Diff(104, 10, Action.ADD)
          ] 

print (depth.apply_actions(actions)) 


actions = [Diff(100, 9, Action.MOD),
           Diff(104, 10, Action.DEL)
          ] 

print (depth.apply_actions(actions)) 