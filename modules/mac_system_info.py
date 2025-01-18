import platform
import subprocess
import psutil
import socket
import uuid
import json
import re
from datetime import datetime

class MacSystemInfo:
    def __init__(self):
        self.system_info = {}
        
    def get_all_info(self):
        """Collect all system information"""
        self.get_os_info()
        self.get_hardware_info()
        self.get_network_info()
        self.get_storage_info()
        self.get_battery_info()
        self.get_bluetooth_info()
        self.get_security_info()
        return self.system_info
        
    def run_command(self, command):
        """Safely run a shell command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def get_os_info(self):
        """Get detailed OS information"""
        sw_vers = self.run_command("sw_vers")
        os_info = {}
        for line in sw_vers.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                os_info[key.strip()] = value.strip()

        self.system_info['os'] = {
            'name': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'build': os_info.get('BuildVersion', ''),
            'product_name': os_info.get('ProductName', ''),
            'product_version': os_info.get('ProductVersion', ''),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'),
            'uptime': self.run_command("uptime")
        }

    def get_hardware_info(self):
        """Get detailed hardware information"""
        system_profiler = self.run_command("system_profiler SPHardwareDataType")
        
        # Parse system_profiler output
        hw_info = {}
        for line in system_profiler.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                hw_info[key.strip()] = value.strip()

        self.system_info['hardware'] = {
            'model_name': hw_info.get('Model Name', ''),
            'model_identifier': hw_info.get('Model Identifier', ''),
            'processor_name': hw_info.get('Processor Name', ''),
            'processor_speed': hw_info.get('Processor Speed', ''),
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True),
            'memory': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'serial_number': hw_info.get('Serial Number (system)', ''),
            'hardware_uuid': hw_info.get('Hardware UUID', ''),
            'activation_lock_status': hw_info.get('Activation Lock Status', '')
        }

    def get_network_info(self):
        """Get detailed network information"""
        network_info = {}
        
        # Get network interfaces
        interfaces_data = self.run_command("ifconfig")
        interfaces = {}
        current_interface = None
        
        for line in interfaces_data.split('\n'):
            if line and not line.startswith('\t'):
                current_interface = line.split(':')[0]
                interfaces[current_interface] = {}
            elif line.strip() and current_interface:
                if 'inet ' in line:
                    interfaces[current_interface]['ipv4'] = line.split('inet ')[1].split(' ')[0]
                elif 'ether ' in line:
                    interfaces[current_interface]['mac'] = line.split('ether ')[1].split(' ')[0]

        # Get Wi-Fi information
        wifi_info = self.run_command("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I")
        wifi_data = {}
        for line in wifi_info.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                wifi_data[key.strip()] = value.strip()

        network_info['interfaces'] = interfaces
        network_info['wifi'] = {
            'ssid': wifi_data.get(' SSID', ''),
            'bssid': wifi_data.get(' BSSID', ''),
            'channel': wifi_data.get(' channel', ''),
            'signal_strength': wifi_data.get(' agrCtlRSSI', ''),
            'noise_level': wifi_data.get(' agrCtlNoise', '')
        }
        
        # Get DNS servers
        dns_servers = []
        scutil_output = self.run_command("scutil --dns")
        for line in scutil_output.split('\n'):
            if 'nameserver' in line:
                dns_server = line.split()[1]
                if dns_server not in dns_servers:
                    dns_servers.append(dns_server)
        network_info['dns_servers'] = dns_servers

        self.system_info['network'] = network_info

    def get_storage_info(self):
        """Get detailed storage information"""
        storage_info = {}
        
        # Get disk information
        disk_info = self.run_command("diskutil list")
        disks = []
        for line in disk_info.split('\n'):
            if '/dev/disk' in line:
                disks.append(line.strip())
                
        # Get volume information
        volumes = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                volumes.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total': f"{usage.total / (1024**3):.2f} GB",
                    'used': f"{usage.used / (1024**3):.2f} GB",
                    'free': f"{usage.free / (1024**3):.2f} GB",
                    'percentage': f"{usage.percent}%"
                })
            except Exception:
                continue

        storage_info['disks'] = disks
        storage_info['volumes'] = volumes
        self.system_info['storage'] = storage_info

    def get_battery_info(self):
        """Get detailed battery information"""
        battery_info = {}
        
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                battery_info = {
                    'percent': battery.percent,
                    'power_plugged': battery.power_plugged,
                    'time_left': battery.secsleft if battery.secsleft != -1 else 'Unknown'
                }
                
        # Get more detailed battery info from system_profiler
        battery_data = self.run_command("system_profiler SPPowerDataType")
        for line in battery_data.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                battery_info[key.strip()] = value.strip()

        self.system_info['battery'] = battery_info

    def get_bluetooth_info(self):
        """Get detailed Bluetooth information"""
        bluetooth_info = {}
        
        # Get Bluetooth information from system_profiler
        bluetooth_data = self.run_command("system_profiler SPBluetoothDataType")
        
        # Parse controller info
        controller_info = {}
        devices = []
        current_device = None
        
        for line in bluetooth_data.split('\n'):
            if 'Bluetooth Controller' in line:
                current_device = "controller"
            elif ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if current_device == "controller":
                    controller_info[key] = value
                elif current_device == "device":
                    if key == "Address":
                        devices.append({'address': value})
                    elif devices:
                        devices[-1][key.lower()] = value
            elif line.strip() and 'Services' not in line:
                current_device = "device"

        bluetooth_info['controller'] = controller_info
        bluetooth_info['paired_devices'] = devices
        
        self.system_info['bluetooth'] = bluetooth_info

    def get_security_info(self):
        """Get security-related information"""
        security_info = {}
        
        # Get SIP status
        sip_status = self.run_command("csrutil status")
        security_info['system_integrity_protection'] = sip_status
        
        # Get FileVault status
        filevault_status = self.run_command("fdesetup status")
        security_info['filevault'] = filevault_status
        
        # Get Gatekeeper status
        gatekeeper_status = self.run_command("spctl --status")
        security_info['gatekeeper'] = gatekeeper_status

        self.system_info['security'] = security_info