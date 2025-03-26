import re
import whois

def validate_url(url):
    """Validates the URL using an improved regex."""
    pattern = r"^(https?://)?"  # Optional http or https
    pattern += r"(www\.)?"      # Optional www.
    pattern += r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Domain name (e.g., example.com)
    pattern += r"(:\d{1,5})?"   # Optional port number
    pattern += r"(/[-a-zA-Z0-9@:%._+~#=]*)*"  # Optional path
    pattern += r"(\?[;&a-zA-Z0-9%_+=-]*)?"  # Optional query string
    pattern += r"(\#[-a-zA-Z0-9_]*)?$"  # Optional fragment identifier
    return re.match(pattern, url) is not None

def extract_email(text):
    """Extracts an email address from the given text using regex."""
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, text)
    return match.group() if match else None

def get_domain_age(domain):
    """Fetches the creation date of a domain using WHOIS."""
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        
        # Handle cases where creation_date is a list or None
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        elif creation_date is None:
            return "Creation date not available"
        
        return creation_date
    except Exception as e:
        return f"Error: Unable to fetch WHOIS data. This may be due to privacy restrictions or network issues."

def analyze_link(link):
    """Runs all checks on the provided link and returns the results."""
    results = {
        "is_valid_url": False,
        "domain_age": None,
        "extracted_email": None,
        "message": ""
    }
    
    # Step 1: Validate the URL
    if not validate_url(link):
        results["message"] = "The link you entered is invalid or broken."
        return results
    
    results["is_valid_url"] = True
    
    # Step 2: Extract domain from the URL
    domain_match = re.search(r"(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", link)
    if not domain_match:
        results["message"] = "Could not extract domain from the link."
        return results
    
    domain = domain_match.group(1)
    
    # Step 3: Check domain age
    results["domain_age"] = get_domain_age(domain)
    
    # Step 4: Extract email (if any)
    results["extracted_email"] = extract_email(link)
    
    # Step 5: Generate user-friendly message
    if "Error" in str(results["domain_age"]):
        results["message"] = f"{results['domain_age']}. Proceed with caution."
    elif results["domain_age"] == "Creation date not available":
        results["message"] = "The domain's creation date is unavailable. Proceed with caution."
    else:
        results["message"] = f"The domain '{domain}' was created on {results['domain_age']}."
    
    if results["extracted_email"]:
        results["message"] += f"\nAn email address was found in the link: {results['extracted_email']}."
    
    return results

def main():
    print("Welcome to the Link Analyzer!")
    print("--------------------------------")
    print("Paste a link, and we'll analyze it for you.\n")
    
    while True:
        # Prompt the user to enter a link
        link = input("Paste a link (or type 'exit' to quit): ").strip()
        
        # Exit condition
        if link.lower() == 'exit':
            print("\nExiting the program. Goodbye!")
            break
        
        # Analyze the link in the background
        print("\nAnalyzing the link... Please wait.\n")
        results = analyze_link(link)
        
        # Display the results
        if not results["is_valid_url"]:
            print("Result: The link you entered is invalid or broken.")
        else:
            print(f"Result: {results['message']}")
        
        print("--------------------------------")

if __name__ == "__main__":
    main()