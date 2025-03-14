import psutil
import subprocess
import re


def obtain_ip():
    global ip
    addresses = psutil.net_if_addrs()

    for interface_keys in addresses.keys():

        if re.findall(r'C[a-zA-Z][0-9]*', interface_keys) or re.findall(r'N[a-zA-Z][0-9]*', interface_keys):
            nic = addresses[interface_keys]

            ip = nic[1]
            print(ip.address)

            return ip.address


ipadd = obtain_ip()

print(f"\n\n---------------------{ipadd}---------------------\n\n")

try:

    iperf_download = subprocess.Popen(args=f".\\iperf3.exe -s -B {ipadd} -V -p 5201",
                                      creationflags=subprocess.CREATE_NEW_CONSOLE)

    iperf_upload = subprocess.Popen(args=f".\\iperf3.exe -s -B {ipadd} -V -p 5202",
                                    creationflags=subprocess.CREATE_NEW_CONSOLE)

    print("-----------5201 is your upload-----------\n\n")

    print("-----------5202 is your upload-----------\n\n")

    while True:

        input("Press any Key to Exit and Kill Iperf3 Server")

        iperf_download.kill()

        iperf_upload.kill()

        break

except Exception:

    print("Error with starting server.\nPlease try again")
