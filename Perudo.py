
import random
import copy


# Function that resets the dice for each player.
# If lstDice exists, then it will reset the values based on the number of dice has a player has left
# otherwise, it will do the initial set up and do it based on the assigned number of dice.
def setPlayerHands(intNumPlayers, lstDice, intNumDice):
    lstNewDice = []
    for i in range(intNumPlayers):
        lstPlayerHand = []
        print(lstDice)
        if lstDice:
            print('1')
            for k in range(len(lstDice[i])):
                lstPlayerHand.append(random.randint(1,6))
        else:
            print('2')
            for k in range(intNumDice):
                lstPlayerHand.append(random.randint(1,6))
        lstNewDice.append(lstPlayerHand)
    return lstNewDice


# Takes a bet from the user and returns it
def takeBet(intNumPlayers, lstPlayerNumbers,intCurrentPlayerIndex, lstCurrentBet, lstDice):
    lstPlayerBet = []
    strGotBet = "no"
    print("Player", lstPlayerNumbers[intCurrentPlayerIndex], "you're up!")
    while strGotBet == "no":
        if lstCurrentBet:
            showCurrentBet(lstCurrentBet)
        intNumDice = int(input("What # of dice are you betting? "))
        
        intDiceFace = int(input("What face of dice are you betting? "))

        if isBetLegal(lstCurrentBet, intNumDice, intDiceFace):
            strGotBet = "yes"
            lstPlayerBet.append(intNumDice)
            lstPlayerBet.append(intDiceFace)
    
            print(lstPlayerBet)
        else:
            print("Illegal bet, please try again.")
    return lstPlayerBet


# Checks if bet is legal
def isBetLegal(lstCurrentBet, intNumDice, intDiceFace): #2,6  3, 4
    if lstCurrentBet:
        intPrevNumDice = lstCurrentBet[0] #2
        intPrevDiceFace = lstCurrentBet[1] #6
        if intDiceFace > 6 or intDiceFace < 1 or intNumDice < intPrevNumDice or intNumDice < 1: #4 is legal, and 3 is more than 2
            return False
        elif intNumDice == intPrevNumDice: #3 isn't equal to 2
            if intDiceFace > intPrevDiceFace: #if i had put in 2, i would fail here as 4 is less than 6
                return True
            else:
                return False
        elif intNumDice > intPrevNumDice:  # 3 is greater than 2, so it retrns true
                return True
    else:
        if 1 <= intDiceFace <= 6:
            return True
        

#Takes the current info and returns a new player index
def passTurn(intNumPlayers, lstPlayerNumbers, intCurrentPlayerIndex, lstCurrentBet, lstDice):

    intPreviousIndexHolder = intCurrentPlayerIndex
    #INCREASE INDEX BY 1
    intCurrentPlayerIndex += 1
    print(intPreviousIndexHolder)
    print(intCurrentPlayerIndex)

    #IF ITS NOW HIGHER THAN POSSIBLE DUE TO NUMBER OF PLAYERS, RESET IT TO 0
    if intCurrentPlayerIndex > intNumPlayers - 1:
        intCurrentPlayerIndex = 0
        
    # CHECK THAT THE SELECTED PLAYER STILL HAS DICE, OTHERWISE SKIP AHEAD
    while not lstDice[intCurrentPlayerIndex]:
        intCurrentPlayerIndex += 1
        print("FLAG Z")

    # IF WHILE LOOP SKIPS ALL THE WAY THROUGH, GAME HAS ENDED
    
    if intCurrentPlayerIndex == intPreviousIndexHolder:
        #END GAME
        strGameActive = "over"

    return intCurrentPlayerIndex

    

# This function checks if a bs call is accurate. Depending on the result, a player loses a dice.           

def checkBS(intNumPlayers,lstPlayerNumbers, intCurrentPlayerIndex,  lstCurrentBet, lstDice, intPreviousPlayerIndex, intDicePerPlayer):
    print("Player", lstPlayerNumbers[intCurrentPlayerIndex], "you're up!")

    showCurrentBet(lstCurrentBet)
    strBSQuestion = str(input(("Do you call bullshit, or no? (enter bs or hit enter)")))
    
    if strBSQuestion == "bs":

        if callBS(lstCurrentBet, lstDice):
            print("You're RIGHT! It was BS. Player", lstPlayerNumbers[intPreviousPlayerIndex], "loses a dice")
            del lstDice[intPreviousPlayerIndex][-1]

        else:
            print("Wrong! It wasn't BS. You lose a dice Player", lstPlayerNumbers[intCurrentPlayerIndex])
            del lstDice[intCurrentPlayerIndex][-1]
        # If bs is called, the dice need to be changed
        lstDice = setPlayerHands(intNumPlayers, lstDice, intDicePerPlayer)
    return lstDice





# Simple method to show the current bet        
def showCurrentBet(lstCurrentBet):
    print("The current bet is", lstCurrentBet[0], lstCurrentBet[1],"s")


# Sees if BS call is accurate                        
def callBS(lstCurrentBet, lstDice):
    count = 0
    for lstPlayerDice in lstDice:
        count += lstPlayerDice.count(lstCurrentBet[1])
    return not count >= lstCurrentBet[0] #returns true if BS
    


def main():

    intNumPlayers = int(input("How many people are playing? "))
    intDicePerPlayer = 2
    intNumDice = intDicePerPlayer * intNumPlayers
    
    # To deal with losing players, creating a list of player numbers, so that while
    # they can be called by index, they are separate from index
    lstPlayerNumbers = list(range(1, intNumPlayers+1))
    

    lstDice = []
    lstCurrentBet=[]
    intCurrentPlayerIndex = 0
    intPreviousPlayerIndex = 0

    # SET UP 
    lstDice = setPlayerHands(intNumPlayers, lstDice, intDicePerPlayer)

    # RUN FIRST BET
    print(lstDice)
    lstCurrentBet = takeBet(intNumPlayers, lstPlayerNumbers,intCurrentPlayerIndex, lstCurrentBet, lstDice)

    strGameActive = "yes"
    # START GAME LOOP
    while strGameActive == "yes":

        # Set up place holder variables for previous player
        lstPreviousDice = copy.deepcopy(lstDice)
        intPreviousPlayerIndex = copy.deepcopy(intCurrentPlayerIndex)

        #PASS TURN
        intCurrentPlayerIndex = passTurn(intNumPlayers, lstPlayerNumbers, intCurrentPlayerIndex, lstCurrentBet, lstDice)

        print(lstDice)
        # BS OR?
        lstDice = checkBS(intNumPlayers, lstPlayerNumbers, intCurrentPlayerIndex, lstCurrentBet, lstDice, intPreviousPlayerIndex, intDicePerPlayer)

        # Check if anything changed during check BS, and reset the CurrentBet if so, and
        # change the player index if so. Should be it's own two functions
        # one for changing the current player index
        # one for changing the current bet
        for i in range(intNumPlayers):
            if len(lstDice[i]) != len(lstPreviousDice[i]):
                print(len(lstDice[i]) != len(lstPreviousDice[i]))
                print("FLAG C")
                if lstDice[i] != []:
                    intCurrentPlayerIndex = i
                    lstCurrentBet = []
                    print("FLAG D")
                else:
                    print("FLAG E")
                    lstCurrentBet = []

                

        # SET NEW BET
        lstCurrentBet = takeBet(intNumPlayers, lstPlayerNumbers, intCurrentPlayerIndex, lstCurrentBet, lstDice)




main()
