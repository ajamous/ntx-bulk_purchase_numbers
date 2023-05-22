import requests
from requests.auth import HTTPDigestAuth
import json
import logging

# define the API endpoints
search_url = 'https://apiv2.neutrafix.telin.net/number/market'
purchase_url = 'https://apiv2.neutrafix.telin.net/number/purchase'

# define the headers for the POST request
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

# Provide the username and password for Digest Authentication
username = '{API-Login}'  # replace with your Buyer account username aka (API Login) - obtained from members.neutrafix.telin.net
password = '{API-Key}'  # replace with your buyer account API key - obtained from members.neutrafix.telin.net

# define the data for the search request
search_data = {
    'prefix': '96279825', # replace with the prefix you're looking for available numbers in.
    'country': '',
    'description': '',
    'seller': '',
    'voice': '1',
    'sms': '1',
    'fax': '0',
    'video': '0',
    'did_type': 'any',
    'pager': '10',
    'off': '1'
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('bulk_numbers_purchase.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# add console output (stdout)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Starting search request...")
search_response = requests.post(search_url, headers=headers, data=search_data, auth=HTTPDigestAuth(username, password))

logger.info(f"Search Response Status Code: {search_response.status_code}")
logger.info(f"Search Response Text: {search_response.text}")

# check if the request was successful
if search_response.status_code == 200:
    # try to get the list of available did_numbers from search_response
    try:
        available_numbers = search_response.json()['dids']  # adjust depending on the response structure
        logger.info(f"Found {len(available_numbers)} available numbers.")
    except ValueError:
        logger.error("Error decoding the response as JSON")
        available_numbers = []
else:
    logger.error("Search request failed")
    available_numbers = []

# loop over the available_numbers list
for number in available_numbers:
    i_did = number['i_did']  # extract the i_did field
    phone_number = number['number']  # extract the number field

    # define the data for the purchase request
    purchase_data = {
        'i_did': i_did,
        'billing_i_account': '35',
        'contact': f'sip:{phone_number}@sip.telecomsxchange.com:5060',  # replace with the actual sip contact
        'smpp_contact': f'smpp:did:did:{phone_number}@smpp.telecomsxchange.com:2776'  # replace with the actual smpp contact
    }

    logger.info(f"Purchase data for number {phone_number}: {json.dumps(purchase_data)}")  # log the purchase data

    logger.info(f"Starting purchase request for number: {phone_number}")
    purchase_response = requests.post(purchase_url, headers=headers, data=purchase_data, auth=HTTPDigestAuth(username, password))

    logger.info(f"Purchase Response Status Code: {purchase_response.status_code}")
    logger.info(f"Purchase Response Text: {purchase_response.text}")
