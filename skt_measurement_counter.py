import tkinter as tk
from tkinter import filedialog
from skt_analyzer import extract_measurements_and_streets

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