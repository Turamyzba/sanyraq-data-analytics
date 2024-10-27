import re

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
