
import requests
from datetime import datetime

# Task 1A — Writing notes to a file

notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes."
]

with open("python_notes.txt", "w", encoding="utf-8") as file:
    for line in notes:
        file.write(line + "\n")

print("File written successfully.")

#Append two new lines
extra_lines = [
    "Topic 6: Functions help organize reusable code.",
    "Topic 7: APIs allow programs to communicate with servers."
]
with open("python_notes.txt", "a", encoding="utf-8") as file:
    for line in extra_lines:
        file.write(line + "\n")

print("Lines appended.")

# Task 1B — Reading the file

with open("python_notes.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

print("\nPython Notes:\n")

for i, line in enumerate(lines, start=1):
    print(f"{i}. {line.strip()}")

print("\nTotal number of lines:", len(lines))

#Ask user for keyword
keyword = input("\nEnter a keyword to search: ").lower()

# Search for matching lines
matches = []

for line in lines:
    if keyword in line.lower():
        matches.append(line.strip())

# Print Results
if matches:
    print("\nMatching lines:")
    for m in matches:
        print(m)
else:
    print("No lines found containing that keyword.")



# Task 2 — API Integration
# API URL 

# Step 1 — Fetch and Display Products:
print("\nFetching products from API...")

url = "https://dummyjson.com/products?limit=20"

# 1.Sending get requests
response = requests.get(url) 

# 2. Parse the JSON response. Each product has fields including id, title, category, price, and rating.
data = response.json() # Converting requests to json
products = data["products"] # Extract the product lists

# 3. Print Formatted table
print("\nID  | Title                         | Category      | Price   | Rating")
print("-" * 80)

for product in products:
    print(f"{product['id']:<3} | "
          f"{product['title']:<30} | "
          f"{product['category']:<13} | "
          f"${product['price']:<7} | "
          f"{product['rating']}")

# Step 2 — Filter and Sort Products

# 1.filter those with a rating ≥ 4.5.

filtered_products = []

for product in products:
    if product["rating"] >= 4.5:
        filtered_products.append(product)

# 2.Sort the filtered list by price in descending order.
filtered_products.sort(key=lambda x: x["price"], reverse=True)

# 3. Print the filtered and sorted list.
print("\nProducts with rating >= 4.5 sorted by price:\n")
for product in filtered_products:
    print(f"{product['title']} - ${product['price']} - Rating {product['rating']}")

# Step 3 — Search Products by Category (Laptops)

#1. Create the laptop API URL 
print("\nFetching laptop products...")

laptop_url = "https://dummyjson.com/products/category/laptops"
response = requests.get(laptop_url)

data = response.json()


#2. Print the name and price of each laptop found.
print("\nLaptop Products:\n")

for product in data["products"]:
    print(f"{product['title']} - ${product['price']}")


# Step 4 — POST Request (Simulated Product Creation)

# 1.Send a POST request
print("\nSending POST request to create a product...")
post_url = "https://dummyjson.com/products/add"

product_data = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}
# 2.Print the full response returned by the server.
response = requests.post(post_url, json=product_data)
print("\nServer Response:")
print(response.json())


# Task 3 — Exception Handling

# Part A — Guarded Calculator

def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


print("\nTesting safe_divide function:")

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))

# Part B: Guarded File Reader

def read_file_safe(filename):
    try:
        file = open(filename, "r", encoding="utf-8")
        content = file.read()
        file.close()
        return content

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    finally:
        print("File operation attempt complete.")


print("\nTesting read_file_safe function:")

print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))


# Part C — Robust API Calls

print("\n=== Testing Robust API Calls ===")

url = "https://dummyjson.com/products?limit=20"

try:
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        data = response.json()
        print("Successfully fetched products from API.")
    else:
        print("HTTP Error:", response.status_code)

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")

except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")

except Exception as e:
    print("Unexpected error:", e)



# Part D — Input Validation Loop:

print("\n=== Product Lookup ===")

while True:
    user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ")

    if user_input.lower() == "quit":
        print("Exiting product lookup.")
        break

    if not user_input.isdigit():
        print("Invalid input. Please enter a number between 1 and 100.")
        continue

    product_id = int(user_input)

    if product_id < 1 or product_id > 100:
        print("Product ID must be between 1 and 100.")
        continue

    url = f"https://dummyjson.com/products/{product_id}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            print("Product not found.")

        elif response.status_code == 200:
            product = response.json()
            print("Title:", product["title"])
            print("Price:", product["price"])

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")

    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")

    except Exception as e:
        print("Unexpected error:", e)   

 # TASK 4 — ERROR LOGGER

print("\n===== TASK 4: ERROR LOGGER =====")


# Function to log errors into error_log.txt
def log_error(location, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("error_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] ERROR in {location}: {message}\n")


# Triggering ConnectionError intentionally
print("\nTriggering Connection Error...")

bad_url = "https://this-host-does-not-exist-xyz.com/api"

try:
    requests.get(bad_url, timeout=5)

except requests.exceptions.ConnectionError:
    print("Connection failed.")
    log_error("fetch_products", "ConnectionError — No connection could be made")


# Triggering HTTP error
print("\nTriggering HTTP Error...")

bad_product_url = "https://dummyjson.com/products/999"

response = requests.get(bad_product_url)

if response.status_code != 200:
    print("HTTP Error:", response.status_code)
    log_error("lookup_product", "HTTPError — 404 Not Found for product ID 999")


# Display the contents of the log file
print("\nContents of error_log.txt:\n")

try:
    with open("error_log.txt", "r", encoding="utf-8") as log_file:
        print(log_file.read())

except FileNotFoundError:
    print("No log file found.")