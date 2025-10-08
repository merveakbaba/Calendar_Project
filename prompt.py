import re
import json
from datetime import datetime


def extract_datetime(user_input):
    date_patterns = [
        (r'(\d{4}-\d{2}-\d{2})', '%Y-%m-%d'),   # YYYY-MM-DD
        (r'(\d{2}/\d{2}/\d{4})', '%d/%m/%Y'),   # DD/MM/YYYY
        (r'(\d{2}-\d{2}-\d{4})', '%d-%m-%Y'),   # DD-MM-YYYY
        (r'([a-zA-Z]+ \d{1,2}(st|nd|rd|th)?)', '%B %d')  # March 3rd
    ]

    for pattern, date_format in date_patterns:
        match = re.search(pattern, user_input)
        if match:
            try:
                # Tarihi parse etme
                dt = datetime.strptime(match.group(1), date_format)

                # Eğer yıl yoksa (örneğin "March 5th") default olarak bu yılı alacak
                if "%Y" not in date_format:
                    dt = dt.replace(year=datetime.now().year)

                # Google Calendar formatı (RFC3339) → YYYY-MM-DDTHH:MM:SS+00:00
                return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")

            except ValueError:
                continue
    return None



def generate_prompt(user_input):
    user_input = user_input.lower()
    extracted_date = extract_datetime(user_input)

    if "list" in user_input:
        return json.dumps({"function": "list_appointments", "start_date": "2025-03-01", "end_date": "2025-03-07"})

    if "add" in user_input:
        return json.dumps({"function": "add_appointment", "date_time": extracted_date, "location": "Office",
                           "description": "Meeting"})

    if "delete" in user_input:
        match = re.search(r'\d+', user_input)
        if match:
            return json.dumps({"function": "delete_appointment", "appointment_id": match.group(0)})

    if "update" in user_input:
        return json.dumps(
            {"function": "update_appointment", "appointment_id": "12345", "new_date_time": extracted_date})

    if "check" in user_input:
        return json.dumps({"function": "check_appointment", "date": extracted_date})

    return json.dumps({"error": "Invalid input. Please try again."})


# Örnek test
print(generate_prompt("Can I book an appointment on March 5th?"))