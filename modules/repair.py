import os
import subprocess
import platform
import psutil

class SystemRepair:
    def __init__(self):
        self.progress = 0
        self.results = []
        
    def fix_issues(self, issues):
        """Fix the identified issues"""
        self.progress = 0
        self.results = []
        
        if not issues:
            self.progress = 100
            return
            
        progress_per_issue = 100 / len(issues)
        
        for issue in issues:
            try:
                issue_type = issue.get('type')
                if issue_type == 'cpu':
                    self._fix_cpu()
                elif issue_type == 'memory':
                    self._fix_memory()
                elif issue_type == 'disk':
                    self._fix_disk()
                elif issue_type == 'network':
                    self._fix_network()
                elif issue_type == 'system':
                    self._fix_system()
                    
                self.progress += progress_per_issue
                
            except Exception as e:
                self.results.append({
                    'success': False,
                    'result': f'Error fixing {issue_type} issue: {str(e)}'
                })
                
        self.progress = 100
        
    def _fix_cpu(self):
        """Fix CPU-related issues"""
        if platform.system() == "Darwin":  # macOS
            try:
                # Clear CPU-intensive processes
                subprocess.run(['sudo', 'purge'], check=True)
                self.results.append({
                    'success': True,
                    'result': 'Successfully optimized CPU usage'
                })
            except Exception as e:
                raise Exception(f'Failed to optimize CPU: {str(e)}')
                
    def _fix_memory(self):
        """Fix memory-related issues"""
        if platform.system() == "Darwin":  # macOS
            try:
                # Clear memory cache
                subprocess.run(['sudo', 'purge'], check=True)
                self.results.append({
                    'success': True,
                    'result': 'Successfully cleared memory cache'
                })
            except Exception as e:
                raise Exception(f'Failed to clear memory: {str(e)}')
                
    def _fix_disk(self):
        """Fix disk-related issues"""
        if platform.system() == "Darwin":  # macOS
            try:
                # Clean temp files
                temp_dirs = [
                    '~/Library/Caches',
                    '~/Library/Logs',
                    '/Library/Caches',
                    '/Library/Logs'
                ]
                
                bytes_cleaned = 0
                for temp_dir in temp_dirs:
                    dir_path = os.path.expanduser(temp_dir)
                    if os.path.exists(dir_path):
                        for root, dirs, files in os.walk(dir_path):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    bytes_cleaned += os.path.getsize(file_path)
                                    os.remove(file_path)
                                except Exception:
                                    continue
                                    
                self.results.append({
                    'success': True,
                    'result': f'Cleaned {bytes_cleaned / (1024*1024):.2f} MB of temporary files'
                })
            except Exception as e:
                raise Exception(f'Failed to clean disk: {str(e)}')
                
    def _fix_network(self):
        """Fix network-related issues"""
        if platform.system() == "Darwin":  # macOS
            try:
                # Flush DNS cache
                subprocess.run(['sudo', 'killall', '-HUP', 'mDNSResponder'], check=True)
                subprocess.run(['sudo', 'killall', 'mDNSResponderHelper'], check=True)
                
                self.results.append({
                    'success': True,
                    'result': 'Successfully reset network settings'
                })
            except Exception as e:
                raise Exception(f'Failed to fix network: {str(e)}')
                
    def _fix_system(self):
        """Fix system-related issues"""
        if platform.system() == "Darwin":  # macOS
            try:
                # Repair disk permissions
                subprocess.run(['sudo', 'diskutil', 'repairPermissions', '/'], check=True)
                
                self.results.append({
                    'success': True,
                    'result': 'Successfully repaired system permissions'
                })
            except Exception as e:
                raise Exception(f'Failed to repair system: {str(e)}')
                
    def get_progress(self):
        """Get the current progress"""
        return int(self.progress)
        
    def get_results(self):
        """Get the repair results"""
        return self.results