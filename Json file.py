import json


product_string = """
{
    "first_scrape": [
    {
        "Product_Id" : "B0BSRVL2VV",
        "title": "Whirlpool 184 L 2 Star Direct-Cool Single Door Refrigerator (205 WDE CLS 2S SAPPHIRE BLUE-Z, Blue,2023 Model)",
        "price": "12,190.",
        "rating": "4.0 out of 5 stars"
        }
    ]
}
"""

data = json.loads(product_string)
print(data)

for product_details in data['first']:
    print(product_details['Product_Id'])