import re


def clean_phone_number(phone_number):
    # Remove all non-digit characters
    phone_number = re.sub(r'[^\d]', '', phone_number)

    # Check if the phone number starts with '8' and is 11 digits long
    if phone_number.startswith('8') and len(phone_number) == 11:
        # Replace the leading '8' with '+7'
        phone_number = '+7' + phone_number[1:]
    # Check if the phone number starts with '7' and is 11 digits long
    elif phone_number.startswith('7') and len(phone_number) == 11:
        # Properly add '+7' to start of the number
        phone_number = '+7' + phone_number[1:]
    # Handle phone numbers without any country code but with correct length
    elif len(phone_number) == 10:
        # Add '+7' assuming the number is correct and only missing the country code
        phone_number = '+7' + phone_number

    return phone_number

#
# # Example usage
# test_numbers = [
#     '8 775 911 6790',  # Kazakh number starting with 8
#     '+7 775 911 6790',  # Properly formatted
#     '7 775 911 6790',  # Starts with 7 but missing '+'
#     '775 911 6790'  # Missing country code and '+'
# ]
#
# cleaned_numbers = [clean_phone_number(num) for num in test_numbers]
# print(cleaned_numbers)
