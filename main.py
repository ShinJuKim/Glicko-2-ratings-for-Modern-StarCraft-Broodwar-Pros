# This is the main file to run, in order to calculate the GLICKO-2 Algorithm on input
from Glicko import Glicko
from Series import Series
import csv
import os

INPUT_PATH = "data"
OUTPUT_PATH = "output_ratings\defaultlist"

glicko = Glicko()

min = 0
max = 19

BOOSTQUAL = False
DECAY = False

for i in range(min, max + 1):
    with open(os.path.join(INPUT_PATH, f"S{i}.csv"), newline='') as csvfile:
        reader = csv.reader(csvfile)

        # v Optional, boosts players at the start of each season on the account they qualified
        if BOOSTQUAL: glicko.boostQualified(os.path.join(INPUT_PATH, f"S{i}.csv"))

        # v Optional, decays rating by x per season not participated.
        if DECAY: glicko.decay(os.path.join(INPUT_PATH, f"S{i}.csv"), x=15)
        for j, row in enumerate(reader):
            if (j == 0): continue

            #print(row)
            
            glicko.update(Series(row))
    glicko.display(title=f'S{i}')
    glicko.display(OUTPUT_PATH, title=f'S{i}')
    next = input()
            
