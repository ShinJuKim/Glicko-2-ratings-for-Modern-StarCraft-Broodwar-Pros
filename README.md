This is a from-scratch implementation of the Glicko-2 rating system, which I have run on Starcraft pro tournaments (ASL seasons 0 through 19) to determine the relative strengths of the best Starcraft 1 players today. Feel free to download this project and exchange the data for your own purposes, just change the paths in main.py. Thank you!

To see all the lists, and how the rankings evolve after each season of ASL, look in the folder output_ratings. After season 19 of ASL, the Glicko-2 algorithm produces:

Top 10 after ASL S19
========================
1. Soulkey (Z): 2094.3397188260897 ~ 68.08761820462279 
2. Flash (T): 2063.645576613892 ~ 257.5372011610105 
3. Snow (P): 2027.351766000318 ~ 74.55181629061548
4. Best (P): 1998.7469554397169 ~ 67.06158518896434 
5. Flash (P) (offrace): 1979.3378925557477 ~ 317.57530159304207 
6. Larva (Z): 1966.5582684638116 ~ 233.77680737560607 
7. Light (T): 1962.0811266905573 ~ 76.19292148718294 
8. Sharp (T): 1923.3110490179351 ~ 99.10378013698377 
9. Queen (Z): 1914.9733128623882 ~ 96.01137603217332 
10. Effort (Z): 1909.1328959044363 ~ 170.9418204601055 
11. Rush (T): 1901.3885438081552 ~ 85.39532433247771


In general, Glicko-2 is mostly an indicator of how well a player did in their most recent performances. I added an extra row, since Flash's Protoss from ASL S10 occupies the rank 5 spot in this metric. Each player has a rating, as well as an uncertainty to their rating. Players who have not played in a while, like Flash, have a higher uncertainty in their rating than players who have played a lot more recently. This means that these players' ratings may change more drastically the next time they play. To see the full 94-player version of this list, look at output_ratings/defaultlist, and scroll to the bottom.

One aspect of this list that I was not satisfied with, was that players who got knocked out in the round of 24 would always experience a decrease in their rating, even though qualifying for ASL is very difficult in itself. The result is that firebathero, who got ro. 24 in S4 and S9, is ranked lower than players who only ever qualified and got ro. 24 once, which is unfair. I created a setting called "qualboost" that simulates a reward for players who qualify in each season, letting them win against a simulated 1350 rated player before that tournament. This also functions as a reward for top players who play in many ASLs, giving them an edge over players who have played fewer as shown:

Top 10 after ASL S19 (with reward for qualifying)
========================
[1] 2403.9789544289483 ~ 71.88580685221032 ~ 0.059836005753271644: soulkey (Z)
[2] 2344.6141869951252 ~ 79.0882194920724 ~ 0.060100603470991235: snow (P)
[3] 2312.1114898513815 ~ 69.0005809910144 ~ 0.059987464912877986: best (P)
[4] 2295.3309690164233 ~ 308.6541286599677 ~ 0.060040119853059494: flash (T)
[5] 2281.1655546648203 ~ 79.3198445108038 ~ 0.05999507661868169: light (T)
[6] 2223.236076644333 ~ 281.64694363226386 ~ 0.05997670659051647: larva (Z)
[7] 2214.84171605849 ~ 99.68453877739654 ~ 0.05998764390552429: queen (Z)
[8] 2203.8529563729116 ~ 90.65151008051384 ~ 0.05996943769054326: rush (T)
[9] 2201.801836430542 ~ 111.8694571271262 ~ 0.06000798710844264: sharp (T)
[10] 2195.586606291218 ~ 197.51367781628508 ~ 0.06010853537320318: effort (Z)

Now, Flash's Protoss is no longer in the top 10, and actually Sharp makes the top 10. I like this list the most, especially for how it ranks players below the very top in a slightly more reasonable manner by rewarding consistent appearance in the ASL, even if they end up going 0-2.

Finally, I added an extra toggleable setting to decay the ratings of each player by x amount for each season they do not play, but this setting is mostly an experiment. Usually, it results in recency bias being far too strong, even more than it is by default.

ASL S20 starts from mid-august, and I will be using this script to compute the next list myself. This list is pretty imperfect, but really there is no objectively correct way to rank the relative power of these players across all the different eras. Each of them bring different strengths, styles, preparation, and game knowledge to the table, and Starcraft fans should feel blessed to have such a vibrant, competitive scene among pros.

