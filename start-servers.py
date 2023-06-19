import os
import subprocess
import time
import psutil
import keyboard
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to run a command in a separate process
def run_command(cmd, cwd=None):
    return subprocess.Popen(cmd, shell=True, cwd=cwd)

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

# Check if Redis server is already running
def is_redis_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'redis-server':
            return True
    return False

# Check if MySQL server is already running
def is_mysql_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'mysqld':
            return True
    return False

# Start Redis server in a separate process if not already running
if not is_redis_running():
    print("Starting Redis server...")
    redis_process = run_command("redis-server")
else:
    print("Redis server is already running.")

# Start MySQL server if not already running
if not is_mysql_running():
    print("Starting MySQL server...")
    mysql_data_dir = os.getenv("MYSQL_DATA_DIR")  # Provide the correct data directory path from your MySQL installation
    mysql_process = run_command(f"mysqld --user=root --datadir={mysql_data_dir} --defaults-file=/usr/local/Cellar/mysql/8.0.33_1/.bottle/etc/my.cnf", cwd="/usr/local/Cellar/mysql/8.0.33_1")
    time.sleep(5)  # Wait for MySQL server to start
else:
    print("MySQL server is already running.")

# Get MySQL credentials from environment variables
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_host = "localhost"
mysql_port = "3306"

# Log in to MySQL
mysql_login_command = f"mysql -h {mysql_host} -P {mysql_port} -u {mysql_user} -p{mysql_password} {mysql_database}"
os.system(mysql_login_command)

# Start backend-server
print("Starting backend-server...")
backend_process = run_command("php artisan serve --host=0.0.0.0 --port=8000", cwd="./backend-server")

time.sleep(1)  # Wait for 1 second

# Start llm-server (frontend)
print("Starting llm-server...")
frontend_process = run_command("npm run dev", cwd="./llm-server")

print("All servers are running...")
print("Press 'q' to shut down the servers...")

while True:
    if keyboard.is_pressed('q'):
        print("Shutting down the servers...")
        kill_processes(["php artisan serve", "npm run dev"])
        if is_redis_running():
            redis_process.terminate()
        if is_mysql_running():
            mysql_process.terminate()
        break
