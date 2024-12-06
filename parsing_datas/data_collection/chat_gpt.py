import openai
# Set the API key from the environment variable
openai.api_key = "sk-None-biyzAFdK3naS9mnvlPAmT3BlbkFJKkdrNsx6BrlkWBXSc9tl"

message = """
Доброго дня 🪐 В двухкомнатной квартире сдается одна комната. Только для девушки или девушек. Можете жить с подругой или одна.
✅ Количество комнат в квартире: 2
✅ Этаж: 7
✅ Стиральная машина автомат
✅ Холодильник
✅ Отдельный гардероб
✅ Полностью меблированный
✅ Кондиционер
Цена: 100.000 тенге и ком услуга. 30.000 тг возвратный депозит
Адрес: Аксай - 1а, 29

Тел: 8 7087086241
"""

prompt = f"""
Extract structured data from this message. Returned data should include and return in json format:
city: string (If the message contains a city name, extract it; otherwise, return null)
district: string (If the message contains a district name, extract it; otherwise, return null)
address: string (If the message contains a full address with a street name and number, extract it; if it only contains the name of a residential complex, extract that; otherwise, return null)
cost: integer (Extract the cost value if present, excluding currency; otherwise, return null)
gender: string (If the message specifies a preferred gender, extract "male" or "female"; otherwise, return null)
people_needed: integer (If the message specifies the number of people being sought, extract the number; otherwise, return null)
long_term: boolean (If the message mentions long-term, return true. If short-term, return false. If no term is mentioned, return null)
phone_number: string (If the message contains a phone number, extract it; otherwise, return null)
utilities: boolean (If the message mentions коммунальные услуги (utilities) cost, return true; otherwise, return false if there nothing about it then null)
deposit: integer (If the message mentions a deposit amount, extract the value; otherwise, return null)

Message:
{message}
"""

# Create a chat completion using the appropriate chat endpoint
completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

# Print the generated text from the model
print(completion.choices[0].message['content'])
