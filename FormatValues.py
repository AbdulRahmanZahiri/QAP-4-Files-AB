# FormatValues.py

def format_name(name):
    return name.strip().title()

def format_address(address):
    return address.strip().title()

def validate_province(province):
    valid_provinces = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
    return province.upper() in valid_provinces

def format_and_validate_postal_code(postal_code):
    postal_code = postal_code.upper().replace(" ", "")
    if len(postal_code) == 6 and postal_code[1].isdigit() and postal_code[3].isdigit() and postal_code[5].isdigit():
        return postal_code[:3] + " " + postal_code[3:]
    else:
        return None

def format_full_name(first_name, last_name):
    full_name = f"{format_name(first_name)} {format_name(last_name)}"
    return full_name, len(full_name)

def format_dollar(amount):
    return f"${amount:,.2f}"
