import psutil
import subprocess
import re
import ipaddress
import datetime


def obtain_ip():
    global ip

    addresses = psutil.net_if_addrs()

    for interface_keys in addresses.keys():

        if re.findall(r'W[a-zA-Z][0-9]*', interface_keys) or re.findall(r'N[a-zA-Z][0-9]*', interface_keys):
            nic = addresses[interface_keys]

            ip = nic[1]

            print(ip.address)

            return ip.address


valid_throughput_sizes = ["K", "M", "G"]

ipadd = obtain_ip()

print(f"\n\n---------------------{ipadd}---------------------\n\n")

while True:
    try:
        usr_input = input("Enter the Iperf Server IP: ")

        ipaddress.ip_address(usr_input)

        try:

            test_duration = int(input("How long would you like to test for?\nIn Minutes, Enter Here: "))


        except Exception:

            print("Unknown Integer or variable type.\nPlease try again.")

        try:
            while True:

                bitrate_down = input("How much traffic would you like to push for the Downstream Channel?\nMUST USE "
                                     "UPPERCASE LETTERING\nEnter Here:")

                bitrate_up = input("How much traffic would you like to push for the Upstream Channel?\nMUST USE "
                                   "UPPERCASE LETTERING\nEnter Here:")

                if bitrate_down[:-1:].isdigit() and bitrate_up[:-1:].isdigit() and bitrate_down[
                    -1] in valid_throughput_sizes and bitrate_up[-1] in valid_throughput_sizes:
                    print(bitrate_down[-1])
                    break

                else:
                    print(bitrate_down)
                    print("Invalid Formatting")

        except Exception:
            print("1")

        break


    except Exception:

        print("Error, Please Check IP Before Entering")

log_file_name_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

iperf_download = subprocess.Popen(
    f".\\iperf3.exe -c {usr_input} -t {test_duration * 60} -p 5201 -B {ipadd} -V -R -u -b {bitrate_down} --logfile client_5201_download_{log_file_name_time}",
    creationflags=subprocess.CREATE_NEW_CONSOLE)

iperf_upload = subprocess.Popen(
    f".\\iperf3.exe -c {usr_input} -t {test_duration * 60} -p 5202 -B {ipadd} -V -u -b {bitrate_up} --logfile client_5202_upload_{log_file_name_time}",
    creationflags=subprocess.CREATE_NEW_CONSOLE)

print("-----------5201 is your download-----------\n\n")

print("-----------5202 is your upload-----------\n\n")

print('Done, Please View Terminals For Results\n')

input("Press any Key to Exit and Kill Iperf3 Server")

iperf_download.kill()

iperf_upload.kill()
