# This is the main file to run, in order to calculate the GLICKO-2 Algorithm on input
from Glicko import Glicko
from Series import Series
import csv
import os

INPUT_PATH = "data"
OUTPUT_PATH = "output_ratings\s0ratings"

glicko = Glicko()

min = 0
max = 19
for i in range(min, max + 1):
    with open(os.path.join(INPUT_PATH, f"S{i}.csv"), newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if (i == 0): continue

            #print(row)
            glicko.update(Series(row))
        glicko.display()
        next = input()
            
