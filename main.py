import os
import tkinter as tk
import pyperclip
import psutil
import platform
from tkinter import messagebox
import subprocess
import wmi
from tkinter import *
import pyperclip
import ctypes
import sys
from PIL import Image, ImageTk

### Colors:
btn_bg_color = "#427aa1"
btn_bgg_color = "#064789"
btn_txt_color = "#ebf2fa"
bg_color = "#263238"
fg_color = "#37474f"
btn1_col = "#3f729b"
btn2_col = "#1c2331"
col = "#212121"
col2 = "#2e2e2e"
col3 = "#3e4551"
col4 = "#4b515d"
info_color = "#0099cc"
info2_color = "#33b5e5"
success_color = "#00c851"
warning_color = "#ffbb33"
danger_color = "#ff4444"
btn_bg_color1 = "#4285f4"
secondary_color = "#aa66cc"
default_color = "#2bbbad"



def shutdown_timer():
    if any([restart_hr_entry.get(), restart_min_entry.get(), restart_sec_entry.get()]):
        messagebox.showerror("Error", "Please clear the restart timer before setting the shutdown timer.")
        return
    try:
        t_hr = int(shutdown_hr_entry.get()) if shutdown_hr_entry.get() else 0
        t_min = int(shutdown_min_entry.get()) if shutdown_min_entry.get() else 0
        t_sec = int(shutdown_sec_entry.get()) if shutdown_sec_entry.get() else 0
        t = t_hr * 3600 + t_min * 60 + t_sec
        os.system(f"shutdown /s /t {t}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid time for the shutdown timer.")

def restart_timer():
    if any([shutdown_hr_entry.get(), shutdown_min_entry.get(), shutdown_sec_entry.get()]):
        messagebox.showerror("Error", "Please clear the shutdown timer before setting the restart timer.")
        return
    if any(shutdown_hr_entry.get() == 0, shutdown_min_entry.get() == 0, shutdown_sec_entry.get() == 0):
        messagebox.showerror("Error", "Please clear the shutdown timer before setting the restart timer.")
        return
    try:
        t_hr = int(restart_hr_entry.get()) if restart_hr_entry.get() else 0
        t_min = int(restart_min_entry.get()) if restart_min_entry.get() else 0
        t_sec = int(restart_sec_entry.get()) if restart_sec_entry.get() else 0
        t = t_hr * 3600 + t_min * 60 + t_sec
        os.system(f"shutdown /r /t {t}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid time for the restart timer.")

def _shutdown():
    os.system("shutdown /s /t 0")

def _restart():
    os.system("shutdown /r /t 0")

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def signout():
    os.system("shutdown /l")

def task_manager():
    os.system("start taskmgr")

def control_panel():
    os.system("start control")

def registry_editor():
    os.system("start regedit")

def event_viewer():
    subprocess.Popen(["eventvwr"])

#have error the script is frezz when open event viewer
# def event_viewer():
#    os.system("eventvwr.msc")

def firewall():
    os.system("firewall.cpl")

def internet_connect():
    os.system("ipconfig /renew")
    connect_button.config(state="disabled")
    disconnect_button.config(state="normal")

def internet_disconnect():
    os.system("ipconfig /release")
    connect_button.config(state="normal")
    disconnect_button.config(state="disabled")

def open_cmd():
    response = messagebox.askquestion("CMD", "Do you want to open CMD as admin?")
    if response == 'yes':
        subprocess.Popen(["powershell", "Start-Process", "cmd.exe", "-Verb", "runas"])
    else:
        subprocess.Popen(["cmd.exe"])

def open_powershell():
    response = messagebox.askquestion("PowerShell", "Do you want to open PowerShell as admin?")
    if response == 'yes':
        subprocess.Popen(["powershell", "Start-Process", "powershell.exe", "-Verb", "runas"])
    else:
        subprocess.Popen(["powershell.exe"])

def get_activation_status():
    try:
        result = subprocess.run(
            ['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dlv'],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        return output
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_system_info():
    try:
        activation_status = get_activation_status()
        
        result = subprocess.run(
            ['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dli'],
            stdout=subprocess.PIPE,
            shell=True,
            text=True
        )
        
        output = result.stdout.strip()
        lines = output.split('\n')
        activation_info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                activation_info[key.strip()] = value.strip()
        
        activation_status = get_activation_status()
        
        # WMI object for querying system information
        c = wmi.WMI()
        # Get GPU info
        gpu_info = c.Win32_VideoController()[0]
        gpu_name = gpu_info.Caption
        gpu_memory = f"{round(int(gpu_info.AdapterRAM) / (1024.0 ** 2))} MB"

        # Get Windows edition
        os_info = c.Win32_OperatingSystem()[0]
        windows_edition = os_info.Caption

        # Combine activation, GPU, and Windows edition into system info dictionary
        info = {
            "System": platform.system(),
            "Windows Edition": windows_edition,
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "RAM": f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB",
            "Activation Status": activation_info.get('License Status', 'Unknown'),
            "GPU": gpu_name,
            "GPU Memory": gpu_memory,
        }
        return info
    except Exception as e:
        return {"Error": str(e)}

def display_info():
    def copy_info_to_clipboard():
        info_text = "\n".join([f"{key}: {value}" for key, value in info.items()])
        pyperclip.copy(info_text)

    def get_license_status():
        activation_status = info.get('Activation Status', 'Unknown')
        return "Licensed" if "licensed" in activation_status.lower() else "Not Licensed"

    info_root = tk.Toplevel(root)
    info_root.title("System Information")
    info = get_system_info()

    # Determine License Status
    license_status = get_license_status()

    # Display License Status
    lbl_license_status = tk.Label(info_root, text=f"License Status: {license_status}", anchor='w', justify='left')
    lbl_license_status.grid(row=0, column=0, sticky='w')

    # Display other system information
    for i, (key, value) in enumerate(info.items()):
        if key != "Activation Status":
            lbl = tk.Label(info_root, text=f"{key}: {value}", anchor='w', justify='left')
            lbl.grid(row=i + 1, column=0, sticky='w')

    # Button to copy information to clipboard
    btn_copy = tk.Button(info_root, text="Copy Information", command=copy_info_to_clipboard)
    btn_copy.grid(row=len(info) + 1, column=0, pady=10)


def open_firewall_settings():
    subprocess.Popen(["mmc.exe", "c:\\windows\\system32\\wf.msc"])

def open_backup_tool():
    subprocess.Popen(["control", "backup"])

def open_antimalware_settings():
    subprocess.Popen(["cmd.exe", "/c", "start", "ms-settings:windowsdefender"])

def open_device_encryption():
    subprocess.Popen(["control", "bitlocker"])

def open_vpn_settings():
    subprocess.Popen(["control", "ncpa.cpl"])

def open_security_updates():
    subprocess.Popen(["ms-settings:windowsupdate"])

def open_firewall_settings():
    subprocess.Popen(["C:\\Windows\\System32\\firewall.cpl"])

def open_backup_tool():
    subprocess.Popen(["C:\\Windows\\System32\\backup"])

def open_antimalware_settings():
    subprocess.Popen(["cmd.exe", "/c", "start", "ms-settings:windowsdefender"])

def open_device_encryption():
    subprocess.Popen(["C:\\Windows\\System32\\bitlocker"])

def open_privacy_tools():
    subprocess.Popen(["C:\\Windows\\System32\\privacy"])

def open_secure_browser():
    subprocess.Popen(["C:\\Windows\\System32\\browser"])

def open_vpn_settings():
    subprocess.Popen(["C:\\Windows\\System32\\vpncli"])

def open_two_factor_auth():
    subprocess.Popen(["C:\\Windows\\System32\\2fa"])

def open_security_updates():
    subprocess.Popen(["ms-settings:windowsupdate"])

def open_notepad():
    subprocess.Popen(["C:\\Windows\\System32\\notepad.exe"])

def open_calc():
    subprocess.Popen(["C:\\Windows\\System32\\calc.exe"])

def open_cmd():
    subprocess.Popen(["C:\\Windows\\System32\\cmd.exe"])

def open_event_viewer():
    subprocess.Popen(["C:\\Windows\\System32\\eventvwr.exe"])

def open_registry_editor():
    subprocess.Popen(["C:\\Windows\\System32\\regedit.exe"])

def open_task_manager():
    subprocess.Popen(["C:\\Windows\\System32\\taskmgr.exe"])

def open_control_panel():
    subprocess.Popen(["C:\\Windows\\System32\\control.exe"])

import subprocess

def open_firewall_settings():
    subprocess.Popen(["C:\\Windows\\System32\\firewall.cpl"])

def open_backup_tool():
    subprocess.Popen(["C:\\Windows\\System32\\backup"])

def open_antimalware_settings():
    subprocess.Popen(["cmd.exe", "/c", "start", "ms-settings:windowsdefender"])

def open_device_encryption():
    subprocess.Popen(["C:\\Windows\\System32\\bitlocker"])

def open_privacy_tools():
    subprocess.Popen(["C:\\Windows\\System32\\privacy"])

def open_secure_browser():
    subprocess.Popen(["C:\\Windows\\System32\\browser"])

def open_vpn_settings():
    subprocess.Popen(["C:\\Windows\\System32\\vpncli"])

def open_two_factor_auth():
    subprocess.Popen(["C:\\Windows\\System32\\2fa"])

def open_security_updates():
    subprocess.Popen(["ms-settings:windowsupdate"])

def open_notepad():
    subprocess.Popen(["C:\\Windows\\System32\\notepad.exe"])

def open_calc():
    subprocess.Popen(["C:\\Windows\\System32\\calc.exe"])

def open_cmd():
    subprocess.Popen(["C:\\Windows\\System32\\cmd.exe"])

def open_event_viewer():
    subprocess.Popen(["C:\\Windows\\System32\\eventvwr.exe"])

def open_registry_editor():
    subprocess.Popen(["C:\\Windows\\System32\\regedit.exe"])

def open_task_manager():
    subprocess.Popen(["C:\\Windows\\System32\\taskmgr.exe"])

def open_control_panel():
    subprocess.Popen(["C:\\Windows\\System32\\control.exe"])

def open_disk_cleanup():
    subprocess.Popen(["C:\\Windows\\System32\\cleanmgr.exe"])

def open_performance_monitor():
    subprocess.Popen(["C:\\Windows\\System32\\perfmon.exe"])

def open_device_manager():
    subprocess.Popen(["C:\\Windows\\System32\\devmgmt.msc"])

def open_services():
    subprocess.Popen(["C:\\Windows\\System32\\services.msc"])

def open_remote_desktop():
    subprocess.Popen(["C:\\Windows\\System32\\mstsc.exe"])

def open_system_config():
    subprocess.Popen(["C:\\Windows\\System32\\msconfig.exe"])

def open_snipping_tool():
    subprocess.Popen(["C:\\Windows\\System32\\SnippingTool.exe"])

def open_power_options():
    subprocess.Popen(["C:\\Windows\\System32\\powercfg.cpl"])

def open_system_info():
    subprocess.Popen(["C:\\Windows\\System32\\msinfo32.exe"])

def open_windows_features():
    subprocess.Popen(["C:\\Windows\\System32\\optionalfeatures.exe"])

def open_print_management():
    subprocess.Popen(["C:\\Windows\\System32\\printmanagement.msc"])

def open_task_scheduler():
    subprocess.Popen(["C:\\Windows\\System32\\taskschd.msc"])

def open_user_accounts():
    subprocess.Popen(["C:\\Windows\\System32\\control.exe", "userpasswords2"])

from tkinter import messagebox

def help_button_clicked():
    help_message = (
        "This tool offers various functionalities:\n"
        "- System tools: Access Task Manager, Control Panel, Registry Editor, and more.\n"
        "- Security configurations: Manage firewall settings, backup tools, and more.\n"
        "- Internet Controller: Connect or disconnect from the internet.\n"
        "- Root Operations: Perform shutdown, restart, sleep, sign out, and set timers.\n\n"
        "For more assistance, refer to:\n"
        "- https://github.com/Mf-malaak/Windows-Mini-Tool-WMT\n"
        "- https://github.com/Mf-malaak"
    )
    messagebox.showinfo("Help", help_message)

def about_button_clicked():
    about_message = (
        "Windows Mini-Tool\n\n"
        "Developed by: [m.Malaak]"
        "This is a program aimed at providing a user-friendly interface for various system "
        "functions and configurations. The tool offers quick access to essential system tools, "
        "security configurations, internet controls, and root operations. It's designed to simplify "
        "system-related tasks for users.\n\n"
        "For more information:\n"
        "- https://github.com/Mf-malaak/Windows-Mini-Tool-WMT\n"
        "- https://github.com/Mf-malaak"
    )
    messagebox.showinfo("About", about_message)


root = tk.Tk()
root.configure(bg=btn_bgg_color)
root.attributes('-topmost', 1)
root.title('Winddows Mini-Tool')
#root.iconbitmap('icon.ico')
root.resizable(False, False)

frame1 = tk.LabelFrame(root, text="System Tools", bg=btn_txt_color, fg=btn_bg_color, font=('Helvetica', '10', 'bold'), relief='flat')
frame1.pack(fill="both", expand="yes", padx=5, pady=5)

system_tools = [
    ("Task Manager", task_manager),
    ("Control Panel", control_panel),
    ("Registry Editor", registry_editor),
    ("Event Viewer", event_viewer),
    ("Firewall", firewall),
    ("Open CMD", open_cmd),
    ("Open PowerShell", open_powershell)
]

for i, (text, command) in enumerate(system_tools):
    button = tk.Button(frame1,
                       text=text,
                       command=command,
                       width=20,
                       bg=btn_bg_color,
                       fg=btn_txt_color,
                       font=('Helvetica', '10', 'bold'),
                       relief='flat')
    button.grid(row=i // 3, column=i % 3, sticky='ew')

frame2 = tk.LabelFrame(root, text="Security Configuration", bg=btn_txt_color, fg=btn_bg_color, font=('Helvetica', '10', 'bold'), relief='flat')
frame2.pack(fill="both", expand="yes", padx=5, pady=5)

security_tools = [
    ("Firewall Settings", open_firewall_settings),
    ("Backup Tool", open_backup_tool),
    ("Antimalware Settings", open_antimalware_settings),
    ("Device Encryption", open_device_encryption),
    ("Privacy Tools", open_privacy_tools),
    ("Secure Browser", open_secure_browser),
    ("VPN Settings", open_vpn_settings),
    ("Two Factor Authentication", open_two_factor_auth),
    ("Security Updates", open_security_updates),
    ("Notepad", open_notepad),
    ("Calculator", open_calc),
    ("Command Prompt", open_cmd),
    ("Event Viewer", open_event_viewer),
    ("Registry Editor", open_registry_editor),
    ("Task Manager", open_task_manager),
    ("Control Panel", open_control_panel),
    ("Disk Cleanup", open_disk_cleanup),
    ("Performance Monitor", open_performance_monitor),
    ("Device Manager", open_device_manager),
    ("Services", open_services),
    ("Remote Desktop", open_remote_desktop),
    ("System Configuration", open_system_config),
    ("Snipping Tool", open_snipping_tool),
    ("Power Options", open_power_options),
    ("System Information", open_system_info),
    ("Windows Features", open_windows_features),
    ("Print Management", open_print_management),
    ("Task Scheduler", open_task_scheduler),
    ("User Accounts", open_user_accounts)
]


for i, (text, command) in enumerate(security_tools):
    button = tk.Button(frame2,
                       text=text,
                       command=command,
                       width=20,
                       bg=btn_bg_color,
                       fg=btn_txt_color,
                       font=('Helvetica', '10', 'bold'),
                       relief='flat')
    button.grid(row=i // 3, column=i % 3, sticky='ew')

# Internet Controller Frame
frame2 = tk.LabelFrame(root, text="Internet Controller", bg=btn_txt_color,fg=btn_bg_color , font=('Helvetica', '10','bold'),relief='flat')
frame2.pack(fill="both", expand="yes", padx=5, pady=5)

connect_button = tk.Button(frame2,
                           text="Connect Internet",
                           state="disabled",
                           command=internet_connect,
                           width=20,
                           bg=success_color,
                           fg=btn_txt_color,
                           font=('Helvetica', '10','bold'),
                           relief='flat')
connect_button.grid(row=0, column=0, sticky='ew')

disconnect_button = tk.Button(frame2,
                              text="Disconnect Internet",
                              command=internet_disconnect,
                              width=20,
                              bg=danger_color,
                              fg=btn_txt_color,
                              font=('Helvetica', '10','bold'),
                              relief='flat')
disconnect_button.grid(row=0, column=1, sticky='ew')

# roots Operation Frame
frame3 = tk.LabelFrame(root, text="roots Operation", bg=btn_txt_color,fg=btn_bg_color , font=('Helvetica', '10','bold'),relief='flat')
frame3.pack(fill="both", expand="yes", padx=5, pady=5)

button = tk.Button(frame3, 
                   text="Shutdown", 
                   command=_shutdown,
                   width=20,
                   bg=danger_color,
                   fg=btn_txt_color,
                   font=('Helvetica', '10','bold'),
                   relief='flat')
button.grid(row=0, column=0, sticky='ew')

button = tk.Button(frame3, 
                   text="Restart", 
                   command=_restart,
                   width=20,
                   bg=warning_color,
                   fg=btn_txt_color,
                   font=('Helvetica', '10','bold'),
                   relief='flat')
button.grid(row=0, column=1, sticky='ew')

button = tk.Button(frame3,
                   text="Sleep",
                   command=sleep,
                   width=20,
                   bg=default_color,
                   fg=btn_txt_color,
                   font=('Helvetica', '10','bold'),
                   relief='flat')
button.grid(row=1, column=0, sticky='ew')

signout_button = tk.Button(frame3,
                           text="Sign Out",
                           command=signout,
                           width=20,
                           bg=secondary_color,
                           fg=btn_txt_color,
                           font=('Helvetica', '10','bold'),
                           relief='flat')
signout_button.grid(row=1, column=1, sticky='ew')

shutdown_label = tk.Label(frame3, text="Shutdown Timer")
shutdown_label.grid(row=2, column=0, sticky='ew')

shutdown_hr_entry = tk.Entry(frame3)
shutdown_hr_entry.grid(row=4, column=0, sticky='ew')
shutdown_hr_label = tk.Label(frame3, text="HH")
shutdown_hr_label.grid(row=3, column=0, sticky='ew')

shutdown_min_entry = tk.Entry(frame3)
shutdown_min_entry.grid(row=6, column=0, sticky='ew')
shutdown_min_label = tk.Label(frame3, text="MM")
shutdown_min_label.grid(row=5, column=0, sticky='ew')

shutdown_sec_entry = tk.Entry(frame3)
shutdown_sec_entry.grid(row=8, column=0, sticky='ew')
shutdown_sec_label = tk.Label(frame3, text="SS")
shutdown_sec_label.grid(row=7, column=0, sticky='ew')

shutdown_button = tk.Button(frame3,
                            text="Set Shutdown Timer",
                            command=shutdown_timer,
                            width=20,
                            bg=danger_color,
                            fg=btn_txt_color,
                            font=('Helvetica', '10','bold'),
                            relief='flat')
shutdown_button.grid(row=9, column=0, sticky='ew')

restart_label = tk.Label(frame3, text="Restart Timer")
restart_label.grid(row=2, column=1, sticky='ew')

restart_hr_entry = tk.Entry(frame3)
restart_hr_entry.grid(row=4, column=1, sticky='ew')
restart_hr_label = tk.Label(frame3, text="HH")
restart_hr_label.grid(row=3, column=1, sticky='ew')

restart_min_entry = tk.Entry(frame3)
restart_min_entry.grid(row=6, column=1, sticky='ew')
restart_min_label = tk.Label(frame3, text="MM")
restart_min_label.grid(row=5, column=1, sticky='ew')

restart_sec_entry = tk.Entry(frame3)
restart_sec_entry.grid(row=8, column=1, sticky='ew')
restart_sec_label = tk.Label(frame3, text="SS")
restart_sec_label.grid(row=7, column=1, sticky='ew')

restart_button = tk.Button(frame3,
                           text="Set Restart Timer",
                           command=restart_timer,
                           width=20,
                           bg=warning_color,
                           fg=btn_txt_color,
                           font=('Helvetica', '10','bold'),
                           relief='flat')
restart_button.grid(row=9, column=1, sticky='ew')

frame4 = tk.LabelFrame(root, text="INFO",  bg=btn_txt_color,fg=btn_bg_color , font=('Helvetica', '10','bold'),relief='flat')
frame4.pack(fill="none", expand="yes", padx=11, pady=11)

help_button = tk.Button(frame4,                        
                        text="Help",
                        command=help_button_clicked,
                        width=11,
                        bg=btn_bg_color,
                        fg=btn_txt_color,
                        font=('Helvetica', '10','bold'),
                        relief='flat')
help_button.grid(row=3, column=2, sticky='ew')
about_button = tk.Button(frame4,
                        text="About",
                        command=about_button_clicked,
                        width=11,
                        bg=btn_bg_color,
                        fg=btn_txt_color,
                        font=('Helvetica', '10','bold'),
                        relief='flat')
about_button.grid(row=4, column=2, sticky='ew')

root.mainloop()
