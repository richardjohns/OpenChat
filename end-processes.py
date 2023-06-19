import os
import psutil
import subprocess

# Function to kill processes based on names
def kill_processes(process_names):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['cmdline'] is not None:
            cmdline = ' '.join(proc.info['cmdline'])
        else:
            cmdline = ''
        for process_name in process_names:
            if process_name in proc.info['name'] or process_name in cmdline:
                print(f"Killing process {proc.info['pid']} ({proc.info['name']})")
                proc.kill()

def get_process_names_by_port(port):
    process_names = []
    try:
        output = subprocess.check_output(f"lsof -i:{port}", shell=True).decode()
        lines = output.split("\n")
        for line in lines[1:]:
            if line:
                process_name = line.split()[0]
                process_names.append(process_name)
    except subprocess.CalledProcessError:
        pass
    return process_names

# Check if MySQL server is already running
def is_mysql_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'mysqld':
            return True
    return False

# Check if Redis server is already running
def is_redis_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'redis-server':
            return True
    return False

print("Ending all OpenChat processes...")

# Kill backend-server and frontend-server processes
kill_processes(["php artisan serve", "npm run dev"])

# Kill processes running on ports 3000 and 8000
kill_processes(["node", "python", "php"])  # Modify the list of process names as needed

# Kill processes running on ports 3000 and 8000 excluding "Code Helper (Plugin)"
processes_to_kill = get_process_names_by_port(3000) + get_process_names_by_port(8000)
processes_to_kill = [process for process in processes_to_kill if process != "Code Helper (Plugin)"]
kill_processes(processes_to_kill)

# Kill Redis server if running
if is_redis_running():
    os.system("pkill -f redis-server")

# Kill MySQL server if running
if is_mysql_running():
    os.system("mysql.server stop")

print("All OpenChat processes have been ended.")
