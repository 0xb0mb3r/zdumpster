import dns.resolver
import ipaddress
import re
import requests

def is_valid_domain(domain):
    regex = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$"
    return all(re.match(regex, part) for part in domain.split("."))

def get_relations(domain):
    dns_relations = {}
    for record_type in ['A', 'NS', 'MX', 'SOA', 'TXT', 'PTR']:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            for data in answers:
                if record_type == 'A':
                    dns_relations[data.address] = record_type
                else:
                    dns_relations[data.to_text()] = record_type
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            pass
    return dns_relations

def get_ip_addresses(dns_relations):
    ip_addresses = []
    for relation, record_type in dns_relations.items():
        if record_type == 'A':
            ip_addresses.append(relation)
        elif record_type == 'PTR':
            try:
                ip_address = ipaddress.ip_address(relation)
                ip_addresses.append(str(ip_address))
            except ValueError:
                pass
    return ip_addresses

def discover_subdomains(domain, limit=10):
    url = "https://lookup.segfault.net/api/v1/lookup/subdomains"
    payload = {"domain": domain, "limit": limit}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get('domains', [])
    else:
        print(f"Failed to discover subdomains for {domain}")
        return []

def process_domain(domain):
    if not is_valid_domain(domain):
        print(f"Invalid domain format: {domain}")
        return None, None, None
    dns_relations = get_relations(domain)
    ip_addresses = get_ip_addresses(dns_relations)
    subdomains = discover_subdomains(domain)
    return dns_relations, ip_addresses, subdomains

def main():
    domain = input("Enter a domain: ").strip()
    
    dns_relations, ip_addresses, subdomains = process_domain(domain)
    if dns_relations is not None:
        print(f"\nDNS Relations for {domain}:\n")
        for relation, record_type in dns_relations.items():
            print(f"| Related NS: {relation} | Type: {record_type} |")
        
        print(f"\nIP Addresses found for {domain}:\n")
        for ip_address in ip_addresses:
            print(f"| IP | {ip_address} |")
        
        print(f"\nSubdomains found for {domain}:\n")
        for subdomain in subdomains:
            print(f"| Subdomain | {subdomain} |")

if __name__ == "__main__":
    main()