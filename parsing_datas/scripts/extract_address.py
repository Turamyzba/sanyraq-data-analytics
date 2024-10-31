import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model with the specified configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def get_district(city, area):
    # Define districts and areas for each city with expanded keywords
    districts = {
        'Алматы': {
            'Алмалинский район': ['Панфилов', 'Гоголь', 'Жібек Жолы', 'Жибек Жолы', 'Абылай хан', 'Кабанбай батыр'],
            'Алатауский район': ['Шаңырақ', 'Шанырак', 'Томирис', 'Рахат', 'Алгабас', 'Нуркент', 'Ожет'],
            'Ауэзовский район': ['Мамыр', 'Орбита', 'Тастақ', 'Тастак', 'Аксай', 'Сайран', 'Жетысу-1', 'Жетысу-2'],
            'Бостандыкский район': ['Самал', 'Орбита', 'Гагарин', 'Алмагуль', 'Баганашыл', 'Навои', 'Ходжанова'],
            'Жетысуский район': ['Құлагер', 'Кулагер', 'Айнабұлақ', 'Айнаблак', 'Көкжиек', 'Кокжик', 'Айнабулак', 'Палладин'],
            'Медеуский район': ['Думан', 'Көктөбе', 'Коктобе', 'Шымбұлақ', 'Шымбулак', 'Горный гигант', 'Самал-2', 'Бесагаш'],
            'Наурызбайский район': ['Таусамалы', 'Калкаман', 'Қалқаман', 'Акжар', 'Ремизовка', 'Коккайнар'],
            'Турксибский район': ['Саяхат', 'Әуежай', 'Ауежай', 'Жас Қанат', 'Жас Канат', 'Кайрат', 'Жулдыз', 'Султан казы']
        },
        'Астана': {
            'Байконурский район': ['Шапағат', 'Шапагат', 'Еңбекшілдер', 'Енбекшилдер', 'Интернациональный', 'Мирный'],
            'Есильский район': ['Сарыарқа', 'Сарыарка', 'Тұран', 'Туран', 'Expo', 'Хан Шатыр', 'ЖК Оркен', 'ЖК Барыс'],
            'Алматинский район': ['Жастар', 'Көктал', 'Коктал', 'Өндіріс', 'Ондіріс', 'Индустриальный', 'Промышленный'],
            'Сарыаркинский район': ['Көктем', 'Коктем', 'Железнодорожный', 'Қараөткел', 'Караоткель', 'Старый вокзал', 'Молодежный']
        }
    }

    # Find district based on city and area
    city_districts = districts.get(city)
    if city_districts:
        for district, areas in city_districts.items():
            if area in areas:
                return district
    return None

def gemini_address(message_text, channel_name):
    # Add the channel name to the beginning of the message text
    combined_text = f"{channel_name} - {message_text}"

    # Define the prompt to improve area extraction based on contextual hints
    prompt = f"""
    Please analyze the following message and extract structured data in JSON format with the fields below. If any field is not present in the message, please return null for that field.

    - city: string (Extract the city name if mentioned; otherwise, return null)
    - area: string (Extract the area name if mentioned; otherwise, return null)

    For the area, look for phrases or keywords that commonly indicate a neighborhood or location within the city, such as landmarks, universities, schools, or transit points. For example, if the message mentions "ЕНУ", "school", or "колесо обозрения", these might indicate the general area within the city.

    Message:
    {combined_text}

    Please return the extracted data in JSON format:
    {{
      "city": "City name or null",
      "area": "Area name or null"
    }}
    """

    # Start a chat session with the prompt history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            }
        ]
    )

    # Send the message and get the response
    response = chat_session.send_message(combined_text)

    # Retrieve the text content from the Part object
    response_data = response.parts[0].text if response.parts else None

    # If there's a valid response, parse the JSON data
    if response_data:
        try:
            extracted_data = json.loads(response_data)
            city = extracted_data.get("city")
            area = extracted_data.get("area")
            # Determine district using get_district function
            district = get_district(city, area)
            return {"city": city, "area": area, "district": district}
        except json.JSONDecodeError:
            print("Error parsing response as JSON.")
            return {"city": None, "area": None, "district": None}
    else:
        print("No response received from Gemini API.")
        return {"city": None, "area": None, "district": None}
