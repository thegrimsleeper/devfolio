import ezgmail

# ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email')
def alert_failure(failure):
	ezgmail.send('recipient@example.com', 'Daily PokeDex failure', f'Daily PokeDex Twitter bot has encountered a failure. Please Investigate. FAILURE: {failure}') # my email removed for privacy
