import requests
import json

# Replace with your actual API key
api_key = 'AIzaSyCNHDpBCPAaU_trjXfKe_pxsX_iJu9wuQc'


# API endpoint URL
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

def gemini(message_text):
    prompt = f"""
    Extract structured data from this message. Returned data can be in any language format:

    - city: string (If the message contains a city name, extract it; otherwise, return null) (Example: Almaty)
    - district: string (If the message contains a district name, extract it; otherwise, return null) (Example: Medey)
    - cost: integer (Extract the cost value if present, excluding currency; otherwise, return null) (Example: "50000 тг", but save only 50000)
    - gender: string (If the message specifies a preferred gender, extract "male" or "female"; otherwise, return null) (Example: "ищем двух девушек" means "female")
    - people_needed: integer (If the message specifies the number of people being sought, extract the number; otherwise, return null) (Example: "ищем двух девушек" means 2)
    - long_term: boolean (If the message mentions long-term (e.g., "на долгий срок"), return true. If short-term, return false. If no term is mentioned, return null)
    - phone_number: string (If the message contains a phone number, extract it; otherwise, return null)
    - utilities: integer (If the message mentions коммунальные услуги (utilities) cost, extract the value; otherwise, return null)
    - deposit: integer (If the message mentions a deposit amount, extract the value; otherwise, return null)

    Message:
    {message_text}
    """
    data = {
        "prompt": prompt
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"
