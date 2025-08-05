#In starcraft, a series is between 1 to 7 games in succession against 2 players/teams.
class Series:
    def __init__(self, year, month, day, number, playerA, playerB, aScore, bScore, aFaction, bFaction):
        self.year = year
        self.month = month
        self.day = day
        self.number = number
        
        self.playerA = playerA + f' ({aFaction.upper()})' if aFaction else playerA
        self.playerB = playerB + f' ({bFaction.upper()})' if bFaction else playerB
        self.aScore = aScore
        self.bScore = bScore

    def __init__(self, list): #assuming csv format
        self.year = int(list[1])
        self.month = int(list[2])
        self.day = int(list[3])
        self.number = int(list[4])
        if (len(list) == 11):
            self.playerA = list[5].lower() + f' ({list[9].upper()})' 
            self.playerB = list[6].lower() + f' ({list[10].upper()})'
        else:
            self.playerA = list[5].lower()[:-2] + list[5][-2].upper() + list[5].lower()[-1:]
            self.playerB = list[6].lower() + list[6][-2].upper() + list[6].lower()[-1:]
        self.aScore = int(list[7])
        self.bScore = int(list[8])
