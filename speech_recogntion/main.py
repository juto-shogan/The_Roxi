# from narwhals import Duration
# import speech_recognition as sr
# import pyttsx3

# # Create a Recognizer instance
# r = sr.Recognizer()
  
  
# def speakText(command):
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()
    
# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source, duration=0.2)
    
#     audio2 = r.listen(source)
#     mytext = r.recognize_google(audio2)
#     mytext = mytext.lower()
    
#     print('did you say' +mytext)
#     speakText(mytext)
    



import subprocess

def run_bash_script(bash_script):
    """Runs a Bash script within the Python script.

    Args:
        bash_script (str): The Bash script to run.
    """

    try:
        result = subprocess.run(
            ["bash", "-c", bash_script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running Bash script: {e}")

bash_script = """
cd /home/juto/Desktop/projects/The_Roxi

git add .
git commit -m "subprocess added"
"""
run_bash_script(bash_script)