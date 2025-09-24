from src.llm_poc.pipeline import ner_with_judge
from dotenv import load_dotenv
import json
import os
load_dotenv()

API_KEY = os.getenv("MODEL_API_KEY")

ner_text = """
Hi there, I just wanted to let you know I paid €1.234,50 on the 5th of Jan 2024 for the order, 
but I think there’s another charge showing as $4,567.8912 in USD which looks strange. 
Anyway, you can call me at (020) 7946 0958 or my US number +1 (415) 555-2671 if needed. 
Also, please email the receipt to John.Doe+test@Example.Co.UK and make sure the invoice 
(#INV-2024/01-05-XYZ) includes my VAT ID gb 999 9999 73 and my IBAN de44 1234 1234 1234 1234 00. 
The shipping address is 221B Baker Street, London NW1 6XE, UK and the due date 
seems to be written as March 15th ‘24 somewhere in the portal. 
I noticed the site HTTPS://Example.com looks different from 
WWW.SomeShop.COM/products?id=123&ref=abc so not sure which one is correct. 
Anyway, the customer name should read Mr. John H. Doe. 
Please call back after 6pm, that’s the best time to reach me.
"""
entity_whitelist = ["date","amount","phone","email","url","iban","vat","zipcode","currency","country","name","address"]
defaults_vals = {
        "default_country": "US",
        "default_currency": "USD",
        "default_phone_country": "US",
        "locale": "en-US"
      }

# Example usage
if __name__ == "__main__":
    result = ner_with_judge(API_KEY, ner_text, defaults_vals, entity_whitelist)
    print("\nFinal result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))




