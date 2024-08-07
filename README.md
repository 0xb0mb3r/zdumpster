# z_dumpster
# DNS and Subdomain Discovery Tool

This Python script performs DNS lookups and subdomain discovery for a given domain. It retrieves DNS records, IP addresses, and subdomains using the `lookup.segfault.net` API.

## Features

- DNS lookups for records of types: A, NS, MX, SOA, TXT, and PTR.
- IP address extraction from DNS A and PTR records.
- Subdomain discovery using the `lookup.segfault.net` API.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `dnspython`
  - `requests`
  - `ipaddress` (included in Python 3.3 and above)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/0xb0mb3r/z_dumpster.git
    cd z_dumpster
    ```

2. Install the required packages:
    ```sh
    pip install dnspython requests
    ```

## Usage

Run the script and enter a domain when prompted:
```sh
python z_dumpster.py
