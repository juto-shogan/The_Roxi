import speech_recognition as sr
import subprocess


def run_bash_command(command):
    """Runs a bash command and returns the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


# Define trigger phrases (case-insensitive)
trigger_on = "click click"
trigger_off = "click day click"

# Initialize speech recognition and loop for continuous listening
recognizer = sr.Recognizer()
is_bash_mode = False

while True:
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()

        if text == trigger_on and not is_bash_mode:
            print("Entering bash mode. Speak commands or say", trigger_off, "to exit.")
            is_bash_mode = True

        elif text == trigger_off and is_bash_mode:
            print("Exiting bash mode.")
            is_bash_mode = False

        elif is_bash_mode:
            # Execute the recognized speech as a bash command
            output = run_bash_command(text)
            print(output)

        else:
            if not is_bash_mode:
                print("You said:", text)
            else:
                print("Invalid command in bash mode. Say", trigger_off, "to exit.")

    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))