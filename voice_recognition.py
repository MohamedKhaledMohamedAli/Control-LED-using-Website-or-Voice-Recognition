# Library to Make voice recognition
import speech_recognition as sr

# Library to write on the terminal
import os

# Function to listen to the voice from the speaker and return the voice in string
def voice_recognition():
    
    # object to recognie the voice
    recognizer = sr.Recognizer()
    
    # Object to set the microphone
    mic = sr.Microphone()
    
    # Open the Laptop mic
    with mic as source:
        
        # Print Listening
        print("Listening.....")
        
        # Clear the noice
        recognizer.adjust_for_ambient_noise(source)
        
        # Listen to the voice from the laptop mic and convert it to audio record
        audio = recognizer.listen(source)
        
        # Here we will try to convert audio record to string
        try:
            
            # Print that we are processing the audio record convertion to string
            print("Parsing......")
            
            # Convert the audio record to string using Google voice recognition
            command = recognizer.recognize_google(audio)
            
            # Print the string of the voice the user said
            print("You said --> {command}")
            
            # Return the string all lower case
            return command.lower()
        except:
            
            # Do Nothing
            pass
        
        # Return empty string
        return ""

# Function to send the value of the voice to the server
def execute_command(command):
    
    # Check if keyword "on" exists in the string or not (NOTE: command is in lower case therefore the "on" must be lower case too for the comparing)
    if "on" in command:
        
        # Make the Program produce sound that it will turn ON the Light
        os.system("espeak -ven+f3 -s 140 -p 50 -a 200 \"OK. I'm Turning ON the Light.\"")
        
        # Send the value to the server to make the Raspberry Pi turn on the LED
        os.system("curl -X POST -d data=1 https://linuxwebsite.pythonanywhere.com/files")
    
    # Check if keyword "off" exists in the string or not
    elif "off" in command:
        
        # Make the Program produce sound that it will turn OFF the Light
        os.system("espeak -ven+f3 -s 140 -p 50 -a 200 \"OK. I'm Turning OFF the Light.\"")
        
        # Send the value to the server to make the Raspberry Pi turn off the LED
        os.system("curl -X POST -d data=0 https://linuxwebsite.pythonanywhere.com/files")
    
    # Check if keyword "exit" exists in the string or not
    elif "exit" in command:
        
        # Make the Program produce sound GoodBye
        os.system("espeak -ven+f3 -s 140 -p 50 -a 200 \"Goodbye.\"")
        
        # exit the program
        exit(0)

# Infinite Loop
while True:
    
    # Get the string of the voice
    command = voice_recognition()
    
    # Check if the command is not empty --> Then execute the program and send to the server the value of the LED
    if command is not None:
        
        # Execute the program and send to the server the value of the LED
        execute_command(command)
