import re
import tkinter as tk
from tkinter import filedialog

def extract_measurements_and_streets(filename):
    measurements = []
    streets = []

    # Open the binary file in read mode
    with open(filename, 'rb') as file:
        # Read the entire binary content
        content = file.read()
    
    # Define the pattern to look for measurements, allowing for optional preceding bytes and optional bytes before 'm' or 'M'
    measurement_pattern = re.compile(rb'\d+\x00\.\x00\d+\x00\s?\x00?[mM]\x00', re.IGNORECASE)
    
    # Find all measurements in the content
    measurement_matches = measurement_pattern.findall(content)
    
    # Decode the matched binary strings to text for measurements
    for match in measurement_matches:
        decoded_match = match.decode('utf-16-le')
        measurements.append(decoded_match.strip())

    # Define a list of common street suffixes and their abbreviations
    street_suffixes = [
        'Street', 'St',
        'Avenue', 'Ave',
        'Road', 'Rd',
        'Boulevard', 'Blvd',
        'Drive', 'Dr',
        'Lane', 'Ln',
        'Court', 'Ct',
        'Plaza', 'Plz',
        'Square', 'Sq',
        'Terrace', 'Ter'
    ]

    # Define the pattern to look for street names with suffixes or abbreviations
    street_pattern = re.compile(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*(?:\s(?:{})\b)'.format('|'.join(street_suffixes)), re.IGNORECASE)
    
    # Convert content to string and decode for text search
    decoded_content = content.decode('utf-16-le', errors='ignore')

    # Find all street names in the content
    street_matches = street_pattern.findall(decoded_content)
    
    # Add the matched street names to the list
    streets.extend(street_matches)

    # Determine complexity level based on the number of measurements found
    count_measurements = len(measurements)
    if count_measurements == 0:
        complexity = "Clear"
    elif 1 <= count_measurements <= 3:
        complexity = "Simple"
    elif 4 <= count_measurements <= 8:
        complexity = "Moderate"
    else:
        complexity is "Complex"

    return count_measurements, measurements, complexity, len(streets), streets

def select_file():
    # Open file dialog to select a file
    file_path = filedialog.askopenfilename(filetypes=[("SKT Files", "*.skt")])
    if file_path:
        count_measurements, measurements, complexity, count_streets, streets = extract_measurements_and_streets(file_path)
        result_text.set(f"Count of Measurements: {count_measurements}\nMeasurements: {measurements}\nComplexity Level: {complexity}\n\nCount of Streets: {count_streets}\nStreets: {streets}")

# Create the main window
root = tk.Tk()
root.title("Measurement and Street Extractor")

# Create a label to display instructions
label = tk.Label(root, text="Select a .skt file to extract measurements and street names:")
label.pack(pady=10)

# Create a button to open the file dialog
button = tk.Button(root, text="Select File", command=select_file)
button.pack(pady=5)

# Create a label to display the result
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400)
result_label.pack(pady=10)

# Run the application
root.mainloop()
