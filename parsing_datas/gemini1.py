import requests
import json
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
    Extract structured data from this message, only returning the following fields:

    address: string (If the message contains a any address with a street name or number or nearby something, or ZHK Name should return any datas which relared to address, extract it; if it only contains the name of a residential complex, extract that; otherwise, return null. Do not return a district name separately.)
    cost: integer (Extract the cost value if present, excluding currency; otherwise, return null, convert values with 'k' to thousands, e.g., '50k' to 50000, Handle formats like '500 00' as 50000.)
    gender: string (If the message specifies a preferred gender, extract "male" or "female"; otherwise, return null)
    people_needed: integer (If the message specifies the number of people being sought, extract the number; otherwise, return null)
    long_term: boolean (If the message mentions long-term (e.g., "на долгий срок"), return true. If short-term, return false. If no term is mentioned, return null)
    phone_number: string (If the message contains a phone number, extract it; otherwise, return null)
    utilities: boolean (If the message mentions коммунальные услуги (utilities) cost or its cost together with cost of apartment, return true; otherwise, return false)
    deposit: integer (If the message mentions a deposit amount, extract the value; otherwise, return null, convert values with 'k' to thousands, e.g., '50k' to 50000)

    Message:
    {message_text}

    dont need to return district
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

    if response.status_code == 200:
        try:
            result = response.json()
            generated_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

            json_content = re.search(r'{(.*?)}', generated_text, re.DOTALL)
            correct_text = json_content.group(0).strip() if json_content else '{}'

            structured_data = json.loads(correct_text)

            # Convert cost values with 'k' or '00' format
            if 'cost' in structured_data and isinstance(structured_data['cost'], str):
                cost_text = structured_data['cost'].replace('k', '000').replace(' ', '')
                structured_data['cost'] = int(cost_text) if cost_text.isdigit() else None

            # Format each key-value pair, converting None to "null"
            formatted_result = "\n".join(
                f"{key}: {value if value is not None else 'null'}" for key, value in structured_data.items())

            return formatted_result

        except (json.JSONDecodeError, AttributeError) as e:
            return f"Error parsing response: {e}"

    else:
        return f"Error: {response.status_code}, {response.text}"
