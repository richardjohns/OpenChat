import os
import psutil

def print_menu():
    print("\n")
    print("1. Find processes")
    print("2. Kill process")
    print("3. List all processes")
    print("4. Shortcut to directory or file")
    print("5. Search tools")
    print("6. MySQL tools")
    print("7. Exit")
    print("\n")

def find_processes(search_term):
    print("\nSearching for processes containing:", search_term)
    for proc in psutil.process_iter(['pid', 'name']):
        if search_term in proc.info['name']:
            print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")

def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        print(f"Process with PID: {pid} terminated.")
    except psutil.NoSuchProcess:
        print(f"No process with PID: {pid} exists.")

def list_all_processes():
    print("\nListing all processes (excluding system processes):")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.info['username'] != 'SYSTEM':
            print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Username: {proc.info['username']}")

def shortcut_to_directory_or_file(path):
    if os.path.exists(path):
        os.chdir(path)
        print(f"\nChanged current directory to: {os.getcwd()}")
    else:
        print("\nPath does not exist.")

def find_process_by_port(port):
    print(f"\nSearching for processes running on port {port}:")
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        for conn in proc.info['connections']:
            if conn.laddr.port == port:
                print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Port: {port}")

def kill_process_prompt(pid):
    response = input(f"\nKill process with PID {pid}? (Y/n): ")
    if response.lower() == 'y':
        kill_process(pid)
    else:
        print("Process not killed.")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            search_term = input("\nEnter search term: ")
            find_processes(search_term)
        elif choice == '2':
            pid = int(input("\nEnter PID of the process to kill: "))
            kill_process_prompt(pid)
        elif choice == '3':
            list_all_processes()
        elif choice == '4':
            shortcut = input("\nEnter the shortcut for the directory or file: ")
            if shortcut in shortcuts:
                shortcut_to_directory_or_file(shortcuts[shortcut])
            else:
                print("\nInvalid shortcut.")
        elif choice == '5':
            search_tools_menu()
        elif choice == '6':
            mysql_tools_menu()
        elif choice == '7':
            print("\nExiting...")
            exit()
        else:
            print("\nInvalid choice. Please enter a valid option.")

def search_tools_menu():
    while True:
        print("\n--- Search Tools ---")
        print("1. Find process by name")
        print("2. Find file")
        print("3. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            process_name = input("\nEnter the process name: ")
            find_processes(process_name)
        elif choice == '2':
            file_name = input("\nEnter the file name: ")
            find_file(file_name)
        elif choice == '3':
            print("\nBack to previous menu...")
            break
        else:
            print("\nInvalid choice. Please enter a valid option.")

def find_file(file_name):
    print(f"\nSearching for file: {file_name}")
    cmd = f"sudo find / -name {file_name} 2>/dev/null"
    os.system(cmd)

def mysql_tools_menu():
    while True:
        print("\n--- MySQL Tools ---")
        print("1. Open MySQL config file")
        print("2. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            open_mysql_config_file()
        elif choice == '2':
            print("\nBack to previous menu...")
            break
        else:
            print("\nInvalid choice. Please enter a valid option.")

def open_mysql_config_file():
    mysql_config_file = "/usr/local/Cellar/mysql/8.0.33_1/.bottle/etc/my.cnf"
    os.system(f"nano {mysql_config_file}")

if __name__ == "__main__":
    main()
