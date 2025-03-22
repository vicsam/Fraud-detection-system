import whois
from datetime import datetime

def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(creation_date, datetime):
            return creation_date
        else:
            return None
    except whois.exceptions.WhoisCommandFailed:
        return None

if __name__ == "__main__":
    # Example domains to test
    domains_to_test = [
        "google.com",
        "example.com",
        "thisisprobablynotarealdomain12345.xyz",
        "microsoft.com",
        "nic.ru"
    ]

    for domain in domains_to_test:
        age = get_domain_age(domain)
        if age:
            print(f"The creation date of {domain} is: {age.strftime('%Y-%m-%d')}")
        else:
            print(f"Could not retrieve the creation date for {domain} or the domain is not registered.")

