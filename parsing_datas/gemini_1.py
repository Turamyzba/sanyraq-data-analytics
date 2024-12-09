import google.generativeai as genai
import json
import re

# Set up the API configuration
genai.configure(api_key="AIzaSyBAgvB8FJTVW7GzloGDO6rxv3-D5j19BK4")

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Define the gemini function to process each message
def gemini(message_text):
    # Define the prompt for extracting structured data
    prompt = f"""
    Extract the following from the message:

    address: string (Street, number, or residential complex name; otherwise, null)
    cost: integer (Value without currency; 'k' to thousands, handle spaces; otherwise, null)
    gender: string (male or female; otherwise, null)
    people_needed: integer (Number of people sought; otherwise, null)
    long_term: boolean (true for long-term, false for short-term, null if none)
    phone_number: string (If present; otherwise, null)
    utilities: boolean (true if utilities cost mentioned with rent; otherwise, false)
    deposit: integer (Deposit amount, 'k' to thousands; otherwise, null)

    Message:
    {message_text}
    """

    # Start a chat session
    chat_session = model.start_chat(
        history=[]
    )

    # Send the prompt to the model and get the response
    response = chat_session.send_message(prompt)

    # Extract the structured data from the response
    try:
        json_content = re.search(r'{(.*?)}', response.text, re.DOTALL)
        correct_text = json_content.group(0).strip() if json_content else '{}'

        structured_data = json.loads(correct_text)

        # Convert cost values with 'k' or '00' format
        if 'cost' in structured_data and isinstance(structured_data['cost'], str):
            cost_text = structured_data['cost'].replace('k', '000').replace(' ', '')
            structured_data['cost'] = int(cost_text) if cost_text.isdigit() else None

        return structured_data
    except json.JSONDecodeError:
        print("Error parsing response: Response is not in JSON format.")
        print("Raw response:", response.text)
        return {}
