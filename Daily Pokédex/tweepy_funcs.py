import tweepy
import re

def twit_api():
    """ supply authorization details and return tweepy.API object"""
    auth = tweepy.OAuthHandler("", "") # removed for security
    auth.set_access_token("", "")      # removed for security
    api = tweepy.API(auth)
    return api

def test_creds():
    """ Test if credentials from twit_api work"""
    api = twit_api()
    try:
        api.verify_credentials
        return "Authentication OK"
    except:
        return "Error during authentication"

def post_tweet(id_pick, db_info):
    """ Posts Media Tweet including, ID. Name. Flavor Text. Sprite"""
    api = twit_api()
    filepath = f'/home/username/scripts/daily_pokedex/sprites/{id_pick}.png' #FIXME: Change dir to a variable
    # Create a formatted string of the text that will be posted into the tweet. ID, name, flavor text
    flavor_text = re.sub(r'[\n\x00-\x08\x0b\x0c\x0e-\x1f-\xff]', ' ', db_info[2])

    message = db_info[0].capitalize() + " <#" + str(id_pick) + "> : "  + flavor_text.replace('\n', ' ') + " (" + db_info[1].replace('-', ' ').capitalize() + ")"

    # Post the tweet
    api.update_with_media(filepath, status=message)
