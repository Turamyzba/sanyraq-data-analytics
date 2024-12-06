import requests
import json
from datetime import datetime
import re

# Replace with your actual API key
api_key = 'AIzaSyAbW85uWNJtLpqNNxxM1Cu5ruO77DcSJlE'

# API endpoint URL
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'


def gemini(message_text):
    # Ensure message_text is not None
    if not message_text:
        message_text = ""
    prompt = f"""
    Extract structured data from this message:

    city: string (If the message contains a city name, extract it; otherwise, return null) (Example: Almaty)
    district: string (If the message contains a district name, extract it; otherwise, return null) (Example: Бостандыкский район  only save Бостандыкский name of district without Район  )
    address: string (If the message contains a full address with a street name and number, extract it; if it only contains the name of a residential complex, extract that; otherwise, return null) (Examples: "Улица Абая, дом 10", or "ЖК Жандос")
    cost: integer (Extract the cost value if present, excluding currency; otherwise, return null) (Example: "50000 тг", but save only 50000, also 35к it means 35000  save return full result)
    gender: string (If the message specifies a preferred gender, extract "male" or "female"; otherwise, return null, if there are two of them just return null) (Example: "ищем двух девушек" means "female")
    people_needed: integer (If the message specifies the number of people being sought, extract the number; otherwise, return null) (Example: "ищем двух девушек" means 2)
    long_term: boolean (If the message mentions long-term (e.g., "на долгий срок"), return true. If short-term, return false. If no term is mentioned, return null)
    phone_number: string (If the message contains a phone number, extract it; otherwise, return null)
    utilities: boolean (If the message mentions коммунальные услуги (utilities) cost, return true; otherwise, return false if there nothing about it then return null)
    deposit: integer (If the message mentions a deposit amount, extract the value; otherwise, return null   for ex: 10к is 10000 return fully result)

    Message:
    {message_text}


    к means 1000
    """

    # Data payload for the API
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Headers for the API request
    headers = {
        'Content-Type': 'application/json'
    }
    # Make the API request
    response = requests.post(url, headers=headers, json=data)

    # Check for successful response and parse JSON
    if response.status_code == 200:
        result = response.json()
        generated_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

        # Remove markdown formatting if it exists
        # cleaned_text = re.sub(r"```json|```", "", generated_text).strip()
        # cleaned_text = generated_text.split('{')[1].split('}')[0]
        json_content = re.search(r'{(.*?)}', generated_text, re.DOTALL)
        correct_text = json_content.group(0).strip()

        structured_data = json.loads(correct_text)

        # Format each key-value pair, converting None to "null" or empty strings as needed
        result = ""
        for key, value in structured_data.items():
            result += f"{key}: {str(value) if value is not None else 'null'}\n"
        # print(correct_text)
        return result

    else:
        return f"Error: {response.status_code}, {response.text}"
