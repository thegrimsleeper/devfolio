# Daily_Pokédex: A Twitter bot that posts "Descriptions of your favorite Pocket Monsters!"
### https://twitter.com/pokedx_daily


### About: 
This program is currently running on a free trier GCP VM instance. It is scheduled via cron to run daily.
The program uses Poke_Base API to make calls and collect the daily Poke'Mon information. 
The images are stored locally in /sprites/{id}.png (No clean up was implented given the sprites small sizes)
Tracking of Poke'Mon information and dates posted is done in the PokeData.csv
This uses Tweepy to post a Media Tweet with the selected content: Name, ID, Flavor Text, Version, and Sprite


### Updates:
#### 5/2/22
- Initial commit to this repo
- This code was pulled down from the running instance
- Changes prior to uploading to this repo:
    - Readability changes
    - Removal of Auth tokens and keys. 
