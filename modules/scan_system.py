import psutil
import platform
import os

class SystemScanner:
    def __init__(self):
        self.progress = 0
        self.results = []
        
    def start_scan(self):
        """Start the system scan"""
        self.progress = 0
        self.results = []
        
        try:
            # Check CPU
            self._check_cpu()
            self.progress = 20
            
            # Check Memory
            self._check_memory()
            self.progress = 40
            
            # Check Disk
            self._check_disk()
            self.progress = 60
            
            # Check Network
            self._check_network()
            self.progress = 80
            
            # Check System
            self._check_system()
            self.progress = 100
            
        except Exception as e:
            self.results.append({
                'type': 'error',
                'severity': 'high',
                'description': f'Error during scan: {str(e)}'
            })
            self.progress = 100
            
    def _check_cpu(self):
        """Check CPU status"""
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 70:
            self.results.append({
                'type': 'cpu',
                'severity': 'high',
                'description': f'High CPU usage detected: {cpu_percent}%'
            })
            
    def _check_memory(self):
        """Check memory status"""
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            self.results.append({
                'type': 'memory',
                'severity': 'high',
                'description': f'High memory usage: {memory.percent}%'
            })
            
    def _check_disk(self):
        """Check disk space"""
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                if usage.percent > 85:
                    self.results.append({
                        'type': 'disk',
                        'severity': 'medium',
                        'description': f'Low disk space on {partition.mountpoint}: {usage.percent}%'
                    })
            except Exception:
                continue
                
    def _check_network(self):
        """Check network status"""
        try:
            if platform.system() == "Darwin":  # macOS
                result = os.system("ping -c 1 8.8.8.8")
                if result != 0:
                    self.results.append({
                        'type': 'network',
                        'severity': 'medium',
                        'description': 'Network connectivity issues detected'
                    })
        except Exception:
            pass
            
    def _check_system(self):
        """Check system status"""
        try:
            boot_time = psutil.boot_time()
            uptime = psutil.time.time() - boot_time
            if uptime > 30 * 24 * 3600:  # 30 days
                self.results.append({
                    'type': 'system',
                    'severity': 'low',
                    'description': 'System has not been restarted in over 30 days'
                })
        except Exception:
            pass
            
    def get_progress(self):
        """Get the current progress"""
        return self.progress
        
    def get_results(self):
        """Get the scan results"""
        return self.results