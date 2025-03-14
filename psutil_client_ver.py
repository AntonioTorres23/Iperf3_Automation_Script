import psutil
import subprocess
import re
import ipaddress


def obtain_ip():
    global ip

    addresses = psutil.net_if_addrs()

    for interface_keys in addresses.keys():

        if re.findall(r'[0-9][a-zA-Z][0-9]C[a-zA-Z][0-9]*', interface_keys) or re.findall(r'[0-9][a-zA-Z][0-9]A[a-zA-Z][0-9]*', interface_keys):
            nic = addresses[interface_keys]

            ip = nic[1]

            print(ip.address)

            return ip.address


ipadd = obtain_ip()

print(f"\n\n---------------------{ipadd}---------------------\n\n")

while True:
    try:
        usr_input = input("Enter the Iperf Server IP:")

        ipaddress.ip_address(usr_input)

        break


    except Exception:

        print("Error, Please Check IP Before Entering")

try:

    iperf_download = subprocess.Popen(f".\\iperf3.exe -c {usr_input} -t 60 -p 5201 -B {ipadd} -V -R -u -b 900M",
                                      creationflags=subprocess.CREATE_NEW_CONSOLE)

    iperf_upload = subprocess.Popen(f".\\iperf3.exe -c {usr_input} -t 60 -p 5202 -B {ipadd} -V -u -b 900M",
                                    creationflags=subprocess.CREATE_NEW_CONSOLE)

    print("-----------5201 is your upload-----------\n\n")

    print("-----------5202 is your upload-----------\n\n")

    print('Done, Please View Terminals For Results\n')

    while True:
        input("Press any Key to Exit and Kill Iperf3 Server")

        iperf_download.kill()

        iperf_upload.kill()

        break


except Exception:

    print("Error with starting server.\nPlease try again")
