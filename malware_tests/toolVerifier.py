import subprocess 

# Verify if tool or software is installed or can be installed 
class ToolVerifier:
    def __init__(self, tool_name):
        self.tool_name = tool_name

    def is_tool_installed(self):
        
        try:
            subprocess.run([self.tool_name, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def install_tool(self):
        try:
            password =  "pijicong" #getpass("Enter your sudo password: ") | put in pass word here 
            command = f'echo {password} | sudo -S apt-get install -y {self.tool_name}'
            subprocess.run(command, shell=True, check=True)
            print(f"{self.tool_name} has been installed.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {self.tool_name}. Error: {e}")

    def verifier(self):
        if self.is_tool_installed():
            print(f"{self.tool_name} is installed.")
        else:
            print(f"{self.tool_name} is not installed.")
            install = input(f"Do you want to install {self.tool_name}? (yes/no): ").strip().lower()
            if install == 'yes':
                self.install_tool()
            else:
                print(f"{self.tool_name} will not be installed.")

