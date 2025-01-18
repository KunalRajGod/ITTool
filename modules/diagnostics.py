import psutil
import os
import platform
import subprocess
import shutil
import json
from datetime import datetime

class SystemDiagnostics:
    def __init__(self):
        self.system_info = {}
        self.issues = []
        self.recommendations = []

    def run_full_diagnostics(self):
        """Run all diagnostic checks"""
        self._check_system_info()
        self._check_cpu_health()
        self._check_memory_health()
        self._check_disk_health()
        self._check_network_health()
        self._check_battery_health()
        self._check_temperature()
        self._check_startup_items()
        self._check_system_logs()
        return self.generate_report()

    def _check_system_info(self):
        """Gather basic system information"""
        self.system_info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node(),
            'python_version': platform.python_version(),
            'total_ram': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'total_disk': f"{psutil.disk_usage('/').total / (1024**3):.2f} GB",
            'cpu_cores': psutil.cpu_count(),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }

    def _check_cpu_health(self):
        """Check CPU usage and performance"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        avg_cpu = sum(cpu_percent) / len(cpu_percent)
        
        if avg_cpu > 80:
            self.issues.append({
                'component': 'CPU',
                'severity': 'high',
                'description': f'High CPU usage detected: {avg_cpu:.1f}%'
            })
            self.recommendations.append(
                'Consider closing resource-intensive applications or scanning for malware'
            )

    def _check_memory_health(self):
        """Check memory usage and performance"""
        mem = psutil.virtual_memory()
        if mem.percent > 80:
            self.issues.append({
                'component': 'Memory',
                'severity': 'high',
                'description': f'High memory usage: {mem.percent}%'
            })
            self.recommendations.append(
                'Consider closing unused applications or increasing RAM'
            )

        # Check for memory leaks
        if mem.available < 1024 * 1024 * 1024:  # Less than 1GB available
            self.issues.append({
                'component': 'Memory',
                'severity': 'critical',
                'description': 'Very low memory available'
            })

    def _check_disk_health(self):
        """Check disk space and performance"""
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                if usage.percent > 85:
                    self.issues.append({
                        'component': 'Disk',
                        'severity': 'medium',
                        'description': f'Low disk space on {partition.mountpoint}: {usage.percent}%'
                    })
                    self.recommendations.append(
                        f'Clean up disk space on {partition.mountpoint}'
                    )
            except Exception:
                continue

    def _check_network_health(self):
        """Check network connectivity and performance"""
        net_io = psutil.net_io_counters()
        if net_io.packets_sent == 0 or net_io.packets_recv == 0:
            self.issues.append({
                'component': 'Network',
                'severity': 'high',
                'description': 'Network connectivity issues detected'
            })

    def _check_battery_health(self):
        """Check battery status if available"""
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                if battery.percent < 20 and not battery.power_plugged:
                    self.issues.append({
                        'component': 'Battery',
                        'severity': 'medium',
                        'description': f'Low battery: {battery.percent}%'
                    })
                if battery.power_plugged and battery.percent < 100:
                    self.recommendations.append(
                        'Battery is charging'
                    )

    def _check_temperature(self):
        """Check system temperature if available"""
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current > entry.high:
                            self.issues.append({
                                'component': 'Temperature',
                                'severity': 'high',
                                'description': f'High temperature detected: {entry.current}°C'
                            })
                            self.recommendations.append(
                                'Check system cooling and clean any dust'
                            )

    def _check_startup_items(self):
        """Check startup applications"""
        if platform.system() == "Darwin":  # macOS
            startup_path = os.path.expanduser('~/Library/LaunchAgents')
            if os.path.exists(startup_path):
                items = len(os.listdir(startup_path))
                if items > 10:
                    self.issues.append({
                        'component': 'Startup',
                        'severity': 'low',
                        'description': f'Many startup items detected: {items}'
                    })
                    self.recommendations.append(
                        'Consider reducing startup items for faster boot'
                    )

    def _check_system_logs(self):
        """Check system logs for errors"""
        if platform.system() == "Darwin":  # macOS
            try:
                log_output = subprocess.check_output(['log', 'show', '--last', '1h', '--predicate', 'eventMessage contains "error"']).decode()
                if len(log_output.split('\n')) > 10:
                    self.issues.append({
                        'component': 'System Logs',
                        'severity': 'medium',
                        'description': 'Multiple system errors detected in logs'
                    })
            except Exception:
                pass

    def generate_report(self):
        """Generate a complete diagnostic report"""
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'system_info': self.system_info,
            'issues': self.issues,
            'recommendations': self.recommendations
        }

    def export_report(self, filename='diagnostic_report.json'):
        """Export the diagnostic report to a file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        return filename