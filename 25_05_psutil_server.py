import datetime
import psutil
import subprocess
import re
import keyboard

proc_name = "iperf3"

proc_list = []

pid = None


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

log_file_name_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

iperf_download = subprocess.Popen(args=f".\\iperf3.exe -s -B {ipadd} -V -p 5201",
                                  creationflags=subprocess.CREATE_NEW_CONSOLE)

iperf_upload = subprocess.Popen(args=f".\\iperf3.exe -s -B {ipadd} -V -p 5202",
                                creationflags=subprocess.CREATE_NEW_CONSOLE)

iperf_download_process = iperf_download.pid

iperf_upload_process = iperf_upload.pid

print(iperf_download_process)

print(iperf_upload_process)

print("-----------5201 is your download-----------\n\n")

print("-----------5202 is your upload-----------\n\n")


while True:
    if keyboard.is_pressed('esc'):
        iperf_download.kill()
        iperf_upload.kill()
        break

    if psutil.pid_exists(iperf_download_process):
        pass
    else:
        iperf_download = subprocess.Popen(args=f".\\iperf3.exe -s -B {ipadd} -V -p 5201",
                                          creationflags=subprocess.CREATE_NEW_CONSOLE)
        iperf_download_process = iperf_download.pid

    if psutil.pid_exists(iperf_upload_process):
        pass
    else:
        iperf_upload = subprocess.Popen(args=f".\\iperf3.exe -s -B {ipadd} -V -p 5202",
                                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        iperf_upload_process = iperf_upload.pid

