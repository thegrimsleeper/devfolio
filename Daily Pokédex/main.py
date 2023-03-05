#!/usr/bin/env python3
import pokebase_pandas_funcs as ppf
import tweepy_funcs as tf
import alert as alert
import sys

def main():	
	# Create Dataframe based on if file exists
	try:
		df = ppf.is_first_run()
	except: 
		alert.alert_failure("Failed to Create/Import data. Failed at 'is_first_run'")
		sys.exit()
	
	# Get Pokemon Object Data
	try:
		# Take remaining IDs in df and select one at random
		id_pick = ppf.get_id(df)
		# Get Pokemon_Species Object using ID above
		poke_pick = ppf.get_pokemon(id_pick)
		# Get a list of name, version, flavor text, and date
		db_info = ppf.get_poke_info(df, id_pick, poke_pick)
		# Get Sprite URL of Pokemon based on ID
		sprite_url = ppf.get_sprite_url(id_pick)
		# Download sprite from URL
		ppf.get_sprite(sprite_url)
		# Write above list to dataframe
		df.loc[poke_pick.id] = db_info
	except: 
		alert.alert_failure("Failed to find pokemon info. Failed in 'Get Pokemon Object Data' comment")
		sys.exit()

	# Post Update
	try:
		tf.post_tweet(id_pick, db_info)
	except:
		alert.alert_failure("Failed to Tweet Information. Failed at 'post_tweet'")
		sys.exit()

	# Export updated frame to csv
	try:
		ppf.export_df(df)
	except:
		alert.alert_failure("Failed to export updated data. Failed at 'export_df'")
		sys.exit()


if __name__ == '__main__':
	main()
