import whois

def get_domain_age(domain):
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
        return f"Error fetching domain age: {e}"

def main():
    print("Domain Age Checker")
    print("-------------------")
    
    while True:
        # Prompt the user to enter a domain
        domain = input("Enter a domain (or type 'exit' to quit): ").strip()
        
        # Exit condition
        if domain.lower() == 'exit':
            print("Exiting...")
            break
        
        # Validate the input
        if not domain:
            print("Please enter a valid domain.")
            continue
        
        # Get the domain age
        result = get_domain_age(domain)
        
        # Display the result
        print(f"Domain: {domain}")
        print(f"Creation Date: {result}")
        print("-------------------")

if __name__ == "__main__":
    main()