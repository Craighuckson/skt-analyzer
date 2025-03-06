import re

def read_file_content(filename):
    with open(filename, 'rb') as file:
        return file.read()

def find_measurements(content):
    measurements = []
    measurement_pattern = re.compile(rb'\d+\x00\.\x00\d+\x00\s?\x00?[mM]\x00', re.IGNORECASE)
    measurement_matches = measurement_pattern.findall(content)
    for match in measurement_matches:
        decoded_match = match.decode('utf-16-le')
        measurements.append(decoded_match.strip())
    return measurements

def find_streets(content):
    streets = []
    street_suffixes = [
        'Street', 'St', 'Avenue', 'Ave', 'Road', 'Rd', 'Boulevard', 'Blvd',
        'Drive', 'Dr', 'Lane', 'Ln', 'Court', 'Ct', 'Plaza', 'Plz', 'Square', 'Sq',
        'Terrace', 'Ter', 'Crescent', 'Cres'
    ]
    street_pattern = re.compile(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*(?:\s(?:{})\b)'.format('|'.join(street_suffixes)), re.IGNORECASE)
    decoded_content = content.decode('utf-16-le', errors='ignore')
    street_matches = street_pattern.findall(decoded_content)
    streets.extend(street_matches)
    return streets

def determine_complexity(measurements):
    count_measurements = len(measurements)
    if count_measurements == 0:
        return "Clear"
    elif 1 <= count_measurements <= 3:
        return "Simple"
    elif 4 <= count_measurements <= 8:
        return "Moderate"
    else:
        return "Complex"

def extract_measurements_and_streets(filename):
    content = read_file_content(filename)
    measurements = find_measurements(content)
    streets = find_streets(content)
    complexity = determine_complexity(measurements)
    return len(measurements), measurements, complexity, len(streets), streets