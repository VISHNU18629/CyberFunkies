import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Enhanced TCCC Protocols Dataset with Additional Injuries
tccc_protocols_synonyms = {
    ("gunshot wound", "shot", "gun shot", "bulletshot", "bulletshot wound"): 
        "Apply pressure to the wound. Use a tourniquet if bleeding is severe. Call for medical evacuation.",
    ("fracture", "broken bone", "bone fracture", "fractured limb", "broken leg", "broken arm"): 
        "Immobilize the limb using a splint. Check circulation below the injury. Provide pain relief if available.",
    ("burns", "burn", "scald", "thermal injury"): 
        "Cool the burn with clean water. Cover with a sterile, non-stick dressing. Prevent hypothermia and seek medical help.",
    ("chest trauma", "chest wound", "penetrating chest injury"): 
        "Seal any open wounds with a chest seal or occlusive dressing. Monitor breathing closely. Prepare for rapid evacuation.",
    ("chest pain", "heart pain", "tight chest", "cardiac pain"): 
        "Sit the patient down and keep them calm. Administer aspirin if available and not allergic. Seek urgent medical attention.",
    ("stroke", "brain stroke", "cerebrovascular accident"): 
        "Recognize signs such as facial drooping, arm weakness, and speech difficulties. Monitor vital signs and expedite evacuation.",
    ("unconscious soldier", "unconscious", "passed out", "non-responsive", "unresponsive"): 
        "Check for breathing and pulse. If not breathing, begin CPR. Call for immediate medical evacuation."
}

# Helper function to retrieve the appropriate protocol based on user input
def get_protocol(injury_input):
    injury_input = injury_input.lower()
    for synonyms, protocol in tccc_protocols_synonyms.items():
        if any(term in injury_input for term in synonyms):
            return protocol
    return "Injury type not found in database!"

# Function to speak the protocol and display it in the GUI
def speak_protocol(injury):
    protocol_text = get_protocol(injury)
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, protocol_text)
    engine.say(protocol_text)
    engine.runAndWait()

# Function for hands-free voice recognition
def listen_for_injury():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        engine.say("Listening for injury type...")
        engine.runAndWait()
        try:
            audio = recognizer.listen(source, timeout=5)
            injury = recognizer.recognize_google(audio).lower()
            speak_protocol(injury)
        except sr.UnknownValueError:
            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, "Sorry, could not understand. Please try again.")
            engine.say("Sorry, could not understand. Please try again.")
            engine.runAndWait()
        except sr.RequestError:
            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, "Speech recognition service unavailable.")
            engine.say("Speech recognition service unavailable.")
            engine.runAndWait()

# Create the GUI using Tkinter
root = tk.Tk()
root.title("TCCC Voice Assistant")
root.geometry("450x500")

tk.Label(root, text="Enter or Speak Injury Type:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 12), width=40)
entry.pack(pady=5)

tk.Button(root, text="Get TCCC Protocol", command=lambda: speak_protocol(entry.get()),
          font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

tk.Button(root, text="🎙 Use Voice Command", command=listen_for_injury,
          font=("Arial", 12), bg="green", fg="white").pack(pady=10)

output_text = scrolledtext.ScrolledText(root, font=("Arial", 12), width=50, height=10, wrap=tk.WORD)
output_text.pack(pady=10)

root.mainloop()