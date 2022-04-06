
from numpy import roll


class BowlingGame:

    maxNumPins = 10 

    strikeBonusRolls = 2 
    spareBonusRolls = 1 

    def __init__(self): 

        self.rollIndex = 0 
        self.frameIndex = 0 

        self.totalScore = 0 

        self.strikeBonus = 0 
        self.spareBonus = 0 
    
    def roll(self, numPins): 

        """Returns a tuple (rollScore, totalScore) after a roll 
        taking down numPins """ 

        # Update totalScore 
        rollMultiplier = 1 

        if (self.strikeBonus > 0): 

            self.strikeBonus += -1 
            rollMultiplier += 1 
        
        if (self.spareBonus > 0): 
            
            self.spareBonus += -1 
            rollMultiplier += 1 
        
        rollScore = rollMultiplier * numPins 
        self.totalScore += rollScore 

        # Get if strike or spare 
        if (numPins == BowlingGame.maxNumPins): 

            if (self.rollIndex == 0): 

                # Strike 
                self.rollIndex += 1 
                self.strikeBonus += BowlingGame.strikeBonusRolls 
            
            else: # (self.rollIndex == 1) 

                # Spare 
                self.spareBonus += BowlingGame.spareBonusRolls 
        
        # Move to next roll 
        self.rollIndex = (self.rollIndex + 1) % 2 
        
        if (self.rollIndex == 0):

            self.frameIndex += 1 
        
        return (rollScore, self.totalScore) 
        
    