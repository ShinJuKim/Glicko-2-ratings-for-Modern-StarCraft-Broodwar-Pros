class Player:
    def __init__(self, ID, rating=1500, RD=350, vol=0.06):
        self.ID = ID
        self.rating = rating
        self.RD = RD
        self.vol = vol

        if (self.ID == "bot"): #adjust as needed
            self.rating=1350
            self.RD = 1
