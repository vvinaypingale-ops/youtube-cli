from voice.voice_assistant import VoiceAssistant

def main():
    print(r"""
 __   __  _____  _     _ _______ _     _ ______  _______   _______        _____
   \_/   |     | |     |    |    |     | |_____] |______   |       |        |  
    |    |_____| |_____|    |    |_____| |_____] |______   |_____  |_____ __|__
[MUSIQ AI Multilingual Voice Assistant]
""")
    assistant = VoiceAssistant()
    assistant.run_loop()

if __name__ == "__main__":
    main()
