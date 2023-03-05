import pokebase as pb
import pandas as pd
import numpy as np
import os, sys
import requests # to get image from the web
import shutil # to save it locally
from datetime import datetime
import alert as alert

def is_first_run():
    """ Check if program running for first time. If not, import existing csv"""
    
    if not os.path.isfile('/home/username/scripts/daily_pokedex/PokeData.csv'):     # FIXME: Change dir to a variable
        # Create dataframe with specified columns
        df = pd.DataFrame(columns=['ID', 'Name', 'Version', 'Flavor_Text', 'Date1'])

        # Number of pokemon 898 as of 3/7/2021, 1-898 into ID column of datarame
        df['ID'] = ids = [x for x in range(1,899)]

        # Set the dataframe index to the IDs (1-898)
        df = df.set_index('ID')

    # If the PokeData.csv already exists just import it
    else:
        df = pd.read_csv('/home/username/scripts/daily_pokedex/PokeData.csv', index_col='ID')  # FIXME: Change dir to a variable
    return df

def get_id(df):
    """ Return an ID from list of IDs in dataframe that contain null date values"""

    remaining_ids = list(df[df['Date1'].isnull()].index)

    if len(remaining_ids) == 0:
        alert.alert_failure("All Pokemon have been tweeted about once")
        sys.exit()

    # randomly choose 1 of the remaining ids
    id_pick = remaining_ids[np.random.randint(len(remaining_ids))] # HACK: Could return inline instead of reassignment

    return id_pick

def get_pokemon(id_pick):
    """ Return pokemon species pokebase object from Pokebase API call for Pokemon_Species(ID)"""
    return pb.pokemon_species(id_pick)

def get_name(poke_pick):
    """ Return Pokemon's name calling .name on pokemon species pokebase object as parameter"""
    return poke_pick.name

def get_poke_info(df, id_pick, poke_pick):
    """Return a list of [name, version, flavor_text, date(YYYY-mm-dd)]"""
    
    # Get the Pokemon's name
    pk_name = get_name(poke_pick)

    # Create empty list for all english flavor texts (Should be 1 per version, ie. red,silver,emerald,etc.) 
    english_flavor_texts = []
    # Check every flavor text entry for pokemon using .flavor_text_entries, add to list if english
    for flavor_text in poke_pick.flavor_text_entries: 
        if str(flavor_text.language) == 'en':
            english_flavor_texts.append(flavor_text)
    
    # Length of english flavor texts should be number of verisons. Grab index of one at random
    version_id = np.random.randint(len(english_flavor_texts))
    # Use .version on the english_flavor_text selected above to get version name
    version = str(english_flavor_texts[version_id].version)
    # Grab flavor text with .flavor_text for that particular version selected using version_id from above
    fl_text = str(english_flavor_texts[version_id].flavor_text)
    
    # Returns a list desired information. Formatted to be added to dataframe
    return [pk_name, version, fl_text, datetime.today().strftime('%Y-%m-%d')]

def get_sprite_url(id_pick):
    """ Return URL from Pokebase API call for Pokemon(ID) front-default sprite"""
    return pb.pokemon(id_pick).sprites.front_default

def get_sprite(sprite_url): 
    """Take URL of image and download image"""

    # Set up the image URL and filename
    image_url = sprite_url      # HACK: Could just use sprite_url inline instead of creating new var
    filename = image_url.split("/")[-1]
    filepath = f'/home/username/scripts/daily_pokedex/sprites/{filename}' # FIXME: Change dir to a variable

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return 0 # success
    else:
        return 1 # fail

def export_df(df):
    """Exports the working dataframe to a CSV for import later"""

    try:
        df.to_csv('/home/username/scripts/daily_pokedex/PokeData.csv') # FIXME: Change dir to a variable
        return 0
    except:
        return 1
