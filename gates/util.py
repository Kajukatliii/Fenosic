import requests
import re

def get_random_identity():

	req = requests.get("https://randomuser.me/api/1.2/?nat=US")

	if req.status_code < 300:

		return req.json()

	else: return False


def __extract_str(string, bet_one, bet_two):

	index_one = string.find(bet_one)
	index_two = string.find(bet_two)

	if index_one != -1 and index_two != -1:

		return string[index_one+len(bet_one):index_two]

	else: return False