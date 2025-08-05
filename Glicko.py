from Series import Series
from Player import Player
import math
import csv

class Glicko:    

    def __init__(self, systemConstant=0.5):
        self.tau = systemConstant # Should be set between 0.3 and 1.2, adjust for greatest accuracy
        self.players = {}

    def update(self, series):
        #Step 1
        if not (series.playerA in self.players.keys()):
            self.players[series.playerA] = Player(series.playerA)
        if not (series.playerB in self.players.keys()):
            self.players[series.playerB] = Player(series.playerB)

        #Now it is given that player A and player B are both player objects in self.players
        pA = self.players[series.playerA]
        pB = self.players[series.playerB]

        #Step 2
        muA = (pA.rating - 1500) / 173.7178
        dA = pA.RD / 173.7178

        muB = (pB.rating - 1500) / 173.7178
        dB = pB.RD / 173.7178

        #Step 3
        def g(d):
            return 1 / math.sqrt(1 + 3 * (d**2 / math.pi**2))
        
        def E(mu, muj, dj):
            return 1 / (1 + math.exp(-g(dj) * (mu - muj)))
        
        
        vA = 1 / (g(dB)**2 * E(muA, muB, dB) * (1 - E(muA, muB, dB)) * (series.aScore + series.bScore))
        vB = 1 / (g(dA)**2 * E(muB, muA, dA) * (1 - E(muB, muA, dA)) * (series.aScore + series.bScore))

        #Step 4
        deltaA = vA * (series.aScore * (g(dB) * (1 - E(muA, muB, dB))) + series.bScore * (g(dB) * (0 - E(muA, muB, dB))))
        deltaB = vB * (series.bScore * (g(dA) * (1 - E(muB, muA, dA))) + series.aScore * (g(dA) * (0 - E(muB, muA, dA))))

        #Step 5
        a = math.log(pA.vol ** 2)
        def fA(x):
            num1 = math.exp(x) * (deltaA ** 2 - dA ** 2 - vA - math.exp(x))
            denom1 = 2 * (dA ** 2 + vA + math.exp(x)) ** 2

            return num1 / denom1 - (x - a) / (self.tau ** 2)
        
        eps = 0.000001

        A = a
        B = 0
        if deltaA**2 > (dA**2 + vA):
            B = math.log(deltaA**2 - dA**2 - vA)
        else:
            k = 1
            while (fA(a - k * self.tau) < 0):
                k += 1
            B = a - k * self.tau
        
        fa = fA(A)
        fb = fA(B)

        while (abs(B - A) > eps):
            C = A + (A - B) * fa / (fb - fa)
            fc = fA(C)

            if (fc * fb <= 0):
                A = B
                fa = fb
            else:
                fa = fa / 2

            B = C
            fb = fc
        
        pA.vol = math.exp(A / 2)

        #now step 5 for player b

        a = math.log(pB.vol ** 2)
        def fA(x):
            num1 = math.exp(x) * (deltaB ** 2 - dB ** 2 - vB - math.exp(x))
            denom1 = 2 * (dB ** 2 + vB + math.exp(x)) ** 2

            return num1 / denom1 - (x - a) / (self.tau ** 2)
        
        eps = 0.000001

        A = a
        B = 0
        if deltaB**2 > (dB**2 + vB):
            B = math.log(deltaB**2 - dB**2 - vB)
        else:
            k = 1
            while (fA(a - k * self.tau) < 0):
                k += 1
            B = a - k * self.tau
        
        fa = fA(A)
        fb = fA(B)

        while (abs(B - A) > eps):
            C = A + (A - B) * fa / (fb - fa)
            fc = fA(C)

            if (fc * fb <= 0):
                A = B
                fa = fb
            else:
                fa = fa / 2

            B = C
            fb = fc
        
        pB.vol = math.exp(A / 2)

        # def check step 5 for bugs, the longest step by far

        # step 6

        dA2 = math.sqrt(dA ** 2 + pA.vol ** 2)
        dB2 = math.sqrt(dB ** 2 + pB.vol ** 2)

        # step 7 + 8

        newdA = 1 / math.sqrt(1 / dA2**2 + 1/vA)
        newmuA = muA + newdA ** 2 * (series.aScore * g(dB) * (1 - E(muA, muB, dB)) + series.bScore * g(dB) * (0 - E(muA, muB, dB)))

        pA.rating = 173.7178 * newmuA + 1500
        pA.RD = 173.7178 * newdA

        newdB = 1 / math.sqrt(1 / dB2**2 + 1/vB)
        newmuB = muB + newdB ** 2 * (series.bScore * g(dA) * (1 - E(muB, muA, dA)) + series.aScore * g(dA) * (0 - E(muB, muA, dA)))

        pB.rating = 173.7178 * newmuB + 1500
        pB.RD = 173.7178 * newdB

        # step 9 would be to apply step 6 to all players who did not play in the series by increasing their volatility.

        for key in self.players:
            
            if (key in (series.playerA, series.playerB)):
                continue
            # if key is not one of the players involved in the match.
            
            pA = self.players[key]
            dA = pA.RD / 173.7178
            dA = math.sqrt(dA ** 2 + pA.vol ** 2)
            pA.RD = 173.7178 * dA
        
        if "botOt" in self.players:
            self.players.pop("botOt")
        
        

    def boostQualified(self, path):
        # This is an optional method that aims to reward players for qualifying to compete in an ASL, even if they perform poorly.
        # Since players pass through gruelling qualifiers before reaching ASL, achieving ro.28 twice should be better than achieving ro.28 just once.
        qualified = set()
        
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if (i == 0): continue
                qualified.add(Series(row).playerA)
                qualified.add(Series(row).playerB)
            
            # print(qualified)
        for player in qualified:
            qualSeries = Series([0,0,0,0,0,player,"bot",1,0])
            self.update(qualSeries)

    def decay(self, path, x):
        qualified = set()
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if (i == 0): continue
                qualified.add(Series(row).playerA)
                qualified.add(Series(row).playerB)
            
            # print(qualified)
        for player in self.players:
            if player not in qualified:
                self.players[player].rating -= x
            
        


    def display(self, path=None, title=None):
        if path:
            with open(path, 'a') as textfile:
                print('========================', file=textfile)
                print(title, file=textfile)
                print('========================', file=textfile)
                output = []
                for key in self.players:
                    output.append([self.players[key].rating, self.players[key].RD, self.players[key].vol, self.players[key].ID])
                    
                    
                output.sort(reverse=True)
                rank = 1
                for line in output:
                    print(f"[{rank}] {line[0]} ~ {line[1]} ~ {line[2]}: {line[3]}", file=textfile)
                    rank += 1
                print('========================', file=textfile)

        else:
            print('========================')
            print(title)
            print('========================')
            output = []
            for key in self.players:
                output.append([self.players[key].rating, self.players[key].RD, self.players[key].vol, self.players[key].ID])
                
                
            output.sort(reverse=True)
            rank = 1
            for line in output:
                print(f"[{rank}] {line[0]} ~ {line[1]} ~ {line[2]}: {line[3]}")
                rank += 1
            print('========================')

