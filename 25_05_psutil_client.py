import psutil
import subprocess
import re
import ipaddress
import datetime
import keyboard


def obtain_ip():
    global ip

    addresses = psutil.net_if_addrs()

    for interface_keys in addresses.keys():

        if re.findall(r'W[a-zA-Z][0-9]*', interface_keys) or re.findall(r'N[a-zA-Z][0-9]*', interface_keys):
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


def read_log_func(file_name):
    last_t = 0.0
    pat = re.compile(r'(\d+(\.\d+)?)-(\d+(\.\d+)?)\s+sec')
    with open(file_name, 'r') as file:
            for line in file:
                mat = pat.search(line)
                if mat:
                    end_t = float(mat.group(3))
                    if end_t > last_t:
                        last_t = end_t
    print(f'Run Time Before Failue: {last_t}')
    return float(last_t)

def read_log_test_complete(file_name):
    with open(file_name, 'r') as file:
        for line in reversed(file.readlines()):
            if re.search(r'-{10,}', line):
                return False
            elif re.search("Test Complete. Summary results:", line):
                return False

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
    f"client_5201_download_{log_file_name_time}.txt",
    creationflags=subprocess.CREATE_NEW_CONSOLE)

iperf_upload = subprocess.Popen(
    f".\\iperf3.exe -c {usr_input} -t {test_dur_for_iperf3_cli} -p 5202 -B {ipadd} -V -u -b {bitrate_up} --logfile "
    f"client_5202_upload_{log_file_name_time}.txt",
    creationflags=subprocess.CREATE_NEW_CONSOLE)

iperf_download_process = iperf_download.pid

iperf_upload_process = iperf_upload.pid

log_file_name_down = f"client_5201_download_{log_file_name_time}.txt"

log_file_name_up = f"client_5202_upload_{log_file_name_time}.txt"

test_dur_down = test_dur_for_iperf3_cli

test_dur_up = test_dur_for_iperf3_cli

rem_test_dur_down = test_dur_down

rem_test_dur_up = test_dur_up

while True:
    if keyboard.is_pressed('esc'):
        iperf_download.kill()
        iperf_upload.kill()
        break

    if not psutil.pid_exists(iperf_download_process):

        read_log_test_complete(log_file_name_down)
        fail_time_down = read_log_func(log_file_name_down)
        rem_test_dur_down = round(rem_test_dur_down - fail_time_down)
        if rem_test_dur_down <= 0 or rem_test_dur_down <= 0.0:
            break
        print(rem_test_dur_down)
        iperf_download = subprocess.Popen(
            f".\\iperf3.exe -c {usr_input} -t {rem_test_dur_down} -p 5201 -B {ipadd} -V -R -u -b {bitrate_down} --logfile "
            f"client_5201_download_{log_file_name_time}.txt",
            creationflags=subprocess.CREATE_NEW_CONSOLE)
        iperf_download_process = iperf_download.pid

        print(f'New Download PID: {iperf_download_process}')

    if not psutil.pid_exists(iperf_upload_process):

        read_log_test_complete(log_file_name_up)
        fail_time_up = read_log_func(log_file_name_up)
        rem_test_dur_up = round(rem_test_dur_up - fail_time_up)
        if rem_test_dur_up <= 0 or rem_test_dur_up <= 0.0:
            break
        print(test_dur_up)
        print(f"Time Up: {rem_test_dur_up}")
        iperf_upload = subprocess.Popen(
            f".\\iperf3.exe -c {usr_input} -t {rem_test_dur_up} -p 5202 -B {ipadd} -V -u -b {bitrate_up} --logfile "
            f"client_5202_upload_{log_file_name_time}.txt",
            creationflags=subprocess.CREATE_NEW_CONSOLE)

        iperf_upload_process = iperf_upload.pid

        print(f'New Upload PID: {iperf_upload_process}')
