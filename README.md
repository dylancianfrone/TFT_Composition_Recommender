# TFT Team Composition Recommender System

This was created as my final project for my Spring 2021 Introduction to Data Mining class at GMU. It's a modification of a K-NN based recommender system for the online game Teamfight Tactics.

## Background Information

Teamfight Tactics is an 8-player autochess game created by Riot Games in which players assemble a team of units to fight against other players' teams. Units are purchased from a random shop, so players have to adapt to the randomness of each unique game in order to build a strong team. This project aimed to recommend a strong team composition for users to aim for based on the units they already had. For more information about Teamfight Tactics, see [Riot Games].

The dataset was sourced from the user mariuszmackowski on [Kaggle]. It consisted of about 90,000 Challenger ranked matches on the EU West server for the set Teamfight Tactics: Fates (the game cycles through 'sets' constantly, each one with a unique set of units and mechanics). 

## Usage

The program reads a csv file of training data consisting of team compositions from each game. Then, the training data is sorted into 'buckets' consisting of similar team compositions. For each test point, the most similar bucket was found and then within the bucket, the most similar real team composition was found and recommended. 

## Results

In my testing, the recommender ended up recommending team compositions with about 85% similarity to the final composition, with 20% of the recommended compositions exactly matching the composition that the player used in the real game. I considered these results satisfactory for several reasons:
- The randomness of the game means that often, a player doesn't get the chance to put together the team composition they were aiming for. Especially late in the game, it can be difficult to find the units you're looking for in the random shop.
- Players don't always play optimally. Since the goal of the system was to recommend the optimal setup, there's no real way to know if the recommendation was more effective than the real game without online play, which would come with a whole host of new challenges (that I would love the chance to work on one day).



   [Kaggle]: <https://www.kaggle.com/mariuszmackowski/teamfight-tactics-fates-challenger-euw-rank-games>
   [Riot Games]: <https://teamfighttactics.leagueoflegends.com/en-us/>
