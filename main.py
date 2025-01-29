import random
import subprocess
from getpass import getpass

"""
To do list
- trigger words
- core for knowing cyber security terms
- find a way to make AI verify whether tools or commands are there (installed)
- find 

Done List
- Basic trigger word
- subprocess integration
- Tool verfier 

Cyber Kill Chain
- Reconnaissance
- intrusion
- Exploration
- Privilege escalation
- lateral movement
- obfuscation/ Anti-forensics
- Denial of service
- Exfiltration

Types of attacks 
- firstly will be doing network attacks
    - ddos
    - malware attack
    - sql injection 

"""
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
            password = getpass("Enter your sudo password: ")
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


# Persona initialization 
class The_Roxi:

    def __init__(self, name="Roxi"):

        self.name = name
        self.greetings = [
            'Hiiiiiiiiiiiiiiiiiiiii',
            "Yoooooooooooooo",
            "Wagwan",
            "Whats up",
            'Howdy'
        ]
        self.catchphrases = [
            "I'm in!",
            "Access granted.",
            "The system is compromised.",
            "Nice try, script kiddie.",
            "I'll be watching you...",
            "Information is power.",
            "Booyah"
        ]
        self.credits = [
            "I was created by Juto and Rokari",
        ]


######################################
    def greet(self):
        return f"Me says, {random.choice(self.greetings)}"
    
    # def tool_verifier(self, user_input): 
    #     tool = subprocess.run(['bash', user_input +'--version'], capture_output=True, text=True)
    #     return tool.stdout
        


#######################################
    def respond(self, user_input):
        """
        Simulates a hacker's response to user input.
        """
        
        # 1. Analyze user input for keywords related to hacking, technology, etc.
        keywords = ["hack", "security", "exploit", "vulnerability", "cybersecurity", 
                    "encryption", "network", "system", "code", "algorithm", "AI"]

        # Simple credits
        credits = ['who made', ' who created', 'who developed', 'who designed', 'who built', 'who coded', 'who programmed', 'who authored']
        
        
        
        if any(keyword in user_input.lower() for keyword in keywords):
            # 2. Generate a response based on the keywords and context.
            responses = [
                "Interesting... I see a potential vulnerability.",
                "The code is poetry, but it can also be a weapon.",
                "Security is an illusion, but a necessary one.",
                "Always assume you're being watched.",
                "Knowledge is the key, but discretion is paramount."
            ]
            return random.choice(responses)
        
        elif any(word in user_input.lower() for word in credits):
            return random.choice(self.credits)
            
        ###################################################
        
        else:
            # 3. Provide a witty or sarcastic response to general input.
            return "I'm listening..."



# attacks begin
class network_chain:
    '''
    Cyber Kill Chain
    - Reconnaissance
    - intrusion
    - Exploration
    - Privilege escalation
    - lateral movement
    - obfuscation/ Anti-forensics
    - Denial of service
    - Exfiltration
'''
    class malware_attack:
        
        def __init__(self):
            pass
                
        # Recon
            """
            what tool do we use during "RECON"
            - nmap
            - wireshark
            - netdiscover
            - airgeddon
            - wifite
            - aircrack-ng 
            
            """
        def recon():# Reconnaissance
            pass
        
        #############################################
        
        # Intrusion
            """
            what do we use during a malware attack
            -viruses:
                - worm
                - trojan 
            """
        def intrusion(): # invasion
            pass
        
        def exploration():
            pass
        
        def priv_escalation():
            pass
        
        def Lmovement():
            pass
        
        def tracks_hider():
            pass
        
        def dos():
            pass
        
        def exfiltration():
            pass
        
        
 
# #########################################
# Run Implemented classes and functions 
# if __name__ == "__main__":
#     test = The_Roxi("Roxi") 
#     print(test.greet()) 

#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit" or "close":
#             break
#         print(test.name + ">", test.respond(user_input))
        
# # Usage
# tool_name = 'steghide'
# verifier = ToolVerifier(tool_name)
# verifier.verifier()
