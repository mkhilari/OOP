
import BowlingGame 

def main(): 

    bowlingGame = BowlingGame.BowlingGame() 

    for i in range(7): 

        (rollScore, totalScore) = bowlingGame.roll(2 * i) 

        print(rollScore, totalScore) 



main() 