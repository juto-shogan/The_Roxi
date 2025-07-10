import os 
import platform
import random
import subprocess
from getpass import getpass

# from toolVerifier import ToolVerifier

"""
To do list
- trigger words
- core for knowing cyber security terms
- find a way to make AI verify whether tools or commands are there (installed)
- find 

Done List
- Basic trigger word
- subprocess verfier 

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
    def start():
       pass
        
        
        
        

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
        
# # Usage for tool verifier 
# tool_name = 'steghide'
# verifier = ToolVerifier(tool_name)
# verifier.verifier()

# # Example usage: for OS detector
# current_os = detect_os()
# print(f"The current operating system is: {current_os}")
