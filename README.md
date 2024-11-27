---
# Netspolt

**Netspolt** is my first project for learning about DDOS attacks. It may not be perfect, but it’s a start. I plan to add more features and make it better over time.

## Features

- **Crafting and Sending Packets**: This project uses Python's `scapy` library to create and send network packets.
- **Multi-threading**: It uses Python's `threading` library to send packets from multiple threads at once, making the attack stronger.
- **Proxy Support**: If you have a list of proxies, you can use them to make the DDOS attack more effective and hide your real IP.

## Requirements

Before running the script, make sure you have these Python libraries:

- `scapy`
- `threading` (this comes with Python, so you don't need to install it)

To install `scapy`, use the following command:

```bash
pip install scapy
```

## How It Works

The script uses **scapy** to create packets and sends them to the target server. By using **multi-threading**, it sends packets from multiple threads at once, making the attack stronger.

### Proxy List

If you have a list of proxies, you can use them to send the traffic through different IP addresses, which helps hide your real IP and makes it harder to stop the attack.

## Important

## This project is for learning and education only. **Do not use this for illegal or harmful purposes.** DDOS attacks without permission are illegal.

If you have any questions or want to talk more about the project, feel free to contact me on Discord: wiraa
