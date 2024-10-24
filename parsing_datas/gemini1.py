# Import the Python SDK
import google.generativeai as genai
import re

# Configure the SDK with your API key
GOOGLE_API_KEY = 'AIzaSyCNHDpBCPAaU_trjXfKe_pxsX_iJu9wuQc'  # Replace with your valid API key
genai.configure(api_key=GOOGLE_API_KEY)


# Define your gemini function using the new SDK
def gemini(message_text):
    prompt = f"""
    Extract structured data from this message. Returned data can be in any language format:

    city: string (If the message contains a city name, extract it; otherwise, return null) (Example: Almaty)
    district: string (If the message contains a district name, extract it; otherwise, return null) (Example: Бостандыкский район  only save Бостандыкский name of district without Район  )
    address: string (If the message contains a full address with a street name and number, extract it; if it only contains the name of a residential complex, extract that; otherwise, return null) (Examples: "Улица Абая, дом 10", or "ЖК Жандос")
    cost: integer (Extract the cost value if present, excluding currency; otherwise, return null) (Example: "50000 тг", but save only 50000)
    gender: string (If the message specifies a preferred gender, extract "male" or "female"; otherwise, return null) (Example: "ищем двух девушек" means "female")
    people_needed: integer (If the message specifies the number of people being sought, extract the number; otherwise, return null) (Example: "ищем двух девушек" means 2)
    long_term: boolean (If the message mentions long-term (e.g., "на долгий срок"), return true. If short-term, return false. If no term is mentioned, return null)
    phone_number: string (If the message contains a phone number, extract it; otherwise, return null)
    utilities: boolean (If the message mentions коммунальные услуги (utilities) cost, return true; otherwise, return false if there nothing about it then null)
    deposit: integer (If the message mentions a deposit amount, extract the value; otherwise, return null)

    Message:
    {message_text}
    """

    # Use the gemini model to generate a response based on the prompt
    model = genai.GenerativeModel('gemini-pro')  # Make sure to use the correct model name

    # Generate content using the model
    response = model.generate_content(prompt)

    # Return the structured data in the response (assuming the API responds with structured data)
    return response.text if response else None


def parse_string(result):
    # Use regular expressions to find values for each key
    city = re.search(r'city:\s*(.*)', result).group(1).strip() if re.search(r'city:\s*(.*)', result) else None
    district = re.search(r'district:\s*(.*)', result).group(1).strip() if re.search(r'district:\s*(.*)', result) else None
    cost = re.search(r'cost:\s*(\d+)', result).group(1).strip() if re.search(r'cost:\s*(\d+)', result) else None
    gender = re.search(r'gender:\s*(.*)', result).group(1).strip() if re.search(r'gender:\s*(.*)', result) else None
    people_needed = re.search(r'people_needed:\s*(\d+)', result).group(1).strip() if re.search(r'people_needed:\s*(\d+)', result) else None
    long_term = re.search(r'long_term:\s*(.*)', result).group(1).strip() if re.search(r'long_term:\s*(.*)', result) else None
    phone_number = re.search(r'phone_number:\s*(\d+)', result).group(1).strip() if re.search(r'phone_number:\s*(\d+)', result) else None
    utilities = re.search(r'utilities:\s*(.*)', result).group(1).strip() if re.search(r'utilities:\s*(.*)', result) else None
    deposit = re.search(r'deposit:\s*(\d+)', result).group(1).strip() if re.search(r'deposit:\s*(\d+)', result) else None

    # Return the parsed values as a dictionary
    return {
        'city': city,
        'district': district,
        'cost': int(cost) if cost else None,
        'gender': gender,
        'people_needed': int(people_needed) if people_needed else None,
        'long_term': long_term if long_term != 'null' else None,
        'phone_number': phone_number,
        'utilities': utilities if utilities != 'null' else None,
        'deposit': int(deposit) if deposit else None
    }


# # Example usage:
# message = """
# Доброго дня 🪐 В двухкомнатной квартире сдается одна комната. Только для девушки или девушек. Можете жить с подругой или одна. \n \n✅ Количество комнат в квартире: 2 \n✅ Этаж: 7 \n✅ Стиральная машина автомат \n✅ Холодильник \n✅ Отдельный гардероб  \n✅ Полностью меблированный \n✅ Кондиционер \nЦена: 100.000 тенге и ком услуга. 30.000 тг возвратный депозит\nАдрес: Аксай - 1а, 29\n\nТел: 8 7087086241
# """
# result = gemini(message)
#
# # Print the result or handle further
# print(result)
