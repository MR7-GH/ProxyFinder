import requests
import json
import argparse
import concurrent.futures
from urllib.parse import urlparse

# Configuration
TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 10
MAX_WORKERS = 20

try:
    import socks
    from requests.packages.urllib3.contrib.socks import SOCKSProxyManager
    SOCKS_SUPPORTED = True
except ImportError:
    SOCKS_SUPPORTED = False

def fetch_proxies():
    base_url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page={}&sort_by=lastChecked&sort_type=desc"
    proxies = []

    for page in [1, 2]:
        url = base_url.format(page)
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            for proxy in data.get('data', []):
                processed = {
                    'ip': proxy.get('ip'),
                    'protocols': proxy.get('protocols', []),
                    'port': proxy.get('port'),
                    'responseTime': proxy.get('responseTime')
                }
                proxies.append(processed)
            
            print(f"Fetched {len(data.get('data', []))} proxies from page {page}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

    return proxies

def test_proxy(proxy):
    working_protocols = []
    ip = proxy['ip']
    port = proxy['port']
    
    for protocol in proxy['protocols']:
        if protocol in ['socks4', 'socks5'] and not SOCKS_SUPPORTED:
            print(f"Skipping SOCKS testing for {ip}:{port} (install requests[socks])")
            continue
            
        proxy_url = f"{protocol}://{ip}:{port}"
        try:
            response = requests.get(
                TEST_URL,
                proxies={protocol: proxy_url},
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                working_protocols.append(protocol)
        except Exception as e:
            continue
    
    if working_protocols:
        return {**proxy, 'protocols': working_protocols}
    return None

def save_proxies(proxies, proxy_chain_format):
    if proxy_chain_format:
        with open('proxychains.conf', 'w') as f:
            for proxy in proxies:
                for protocol in proxy['protocols']:
                    f.write(f"{protocol} {proxy['ip']} {proxy['port']}\n")
        print(f"Saved {len(proxies)} proxies to proxychains.conf")
    else:
        with open('proxies.json', 'w') as f:
            json.dump(proxies, f, indent=2)
        print(f"Saved {len(proxies)} proxies to proxies.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Proxy Fetcher and Tester')
    parser.add_argument('--working', action='store_true', help='Test and save only working proxies')
    parser.add_argument('--proxychain', action='store_true', help='Output in ProxyChain format')
    args = parser.parse_args()

    # Fetch initial proxies
    proxies = fetch_proxies()
    print(f"Initial proxy count: {len(proxies)}")

    # Test proxies if requested
    if args.working:
        print("Testing proxies...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(test_proxy, proxy) for proxy in proxies]
            proxies = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    proxies.append(result)
        print(f"Working proxies remaining: {len(proxies)}")

    # Save results
    save_proxies(proxies, args.proxychain)