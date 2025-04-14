import psutil
import subprocess
import re
import ipaddress
import datetime


def obtain_ip():
    global ip

    addresses = psutil.net_if_addrs()

    for interface_keys in addresses.keys():

        if re.findall(r'A[a-zA-Z][0-9]*', interface_keys) or re.findall(r'N[a-zA-Z][0-9]*', interface_keys):
            nic = addresses[interface_keys]

            ip = nic[1]

            print(ip.address)

            return ip.address


def run_time(run_time_var):
    if run_time_var[-1] in valid_times:

        if valid_times[0] in run_time_var:

            new_runtime = int(run_time_var[:-1])

            return int(new_runtime)

        elif valid_times[1] in run_time_var:

            new_runtime = int(run_time_var[:-1])

            return int(new_runtime * 60)

        elif valid_times[2] in run_time_var:

            new_runtime = int(run_time_var[:-1])

            return int(new_runtime * 3600)
    else:

        print("NOT FOUND")


valid_times = ["S", "M", "H"]

valid_throughput_sizes = ["K", "M", "G"]

ipadd = obtain_ip()

print(f"\n\n---------------------{ipadd}---------------------\n\n")

while True:
    try:
        usr_input = input("Enter the Iperf Server IP: ")

        ipaddress.ip_address(usr_input)

        while True:

            try:
                test_duration = input("How long would you like to test for?\nIn this formatting (i.e 1S, 10M, or 2H), "
                                      "Enter Here: ")

                test_dur_for_iperf3_cli = run_time(test_duration)

                if test_dur_for_iperf3_cli.is_integer():
                    print(f"Your Time In Seconds: {test_dur_for_iperf3_cli}")
                    break

                else:

                    print("UNKNOWN DATA TYPE PLEASE TRY AGAIN")



            except Exception:
                print("UNKNOWN TYPE PLEASE TRY AGAIN")

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
    f".\\iperf3.exe -c {usr_input} -t {test_dur_for_iperf3_cli} -p 5201 -B {ipadd} -V -R -u -b {bitrate_down} --logfile "
    f"client_5201_download_{log_file_name_time}",
    creationflags=subprocess.CREATE_NEW_CONSOLE)

iperf_upload = subprocess.Popen(
    f".\\iperf3.exe -c {usr_input} -t {test_dur_for_iperf3_cli} -p 5202 -B {ipadd} -V -u -b {bitrate_up} --logfile "
    f"client_5202_upload_{log_file_name_time}",
    creationflags=subprocess.CREATE_NEW_CONSOLE)

print("-----------5201 is your download-----------\n\n")

print("-----------5202 is your upload-----------\n\n")

print('Done, Please View Terminals For Results\n')

input("Press any Key to Exit and Kill Iperf3 Server")

iperf_download.kill()

iperf_upload.kill()
