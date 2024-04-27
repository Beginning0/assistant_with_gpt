import openai
import pyttsx3
import speech_recognition as sr
import time

openai.api_key = 'TU_CLAVE_DE_API'
model_id = 'gpt-3.5-turbo'

class SpeechModule:
    def __init__(self, voice=0, volume=1, rate=125):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[voice].id)

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
class VoiceRecognitionModule:
    def __init__(self, key=None):
        self.key = key
        self.r = sr.Recognizer()

    def recognize(self):
        with sr.Microphone() as source:
            print("Escuchando: ")
            audio = self.r.listen(source)
            try:
                text = self.r.recognize_google(audio, key=self.key, language="es")
                return text
            except:
                return None


def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

conversation = []
conversation.append({'role': 'system', 'content': '¿Como puedo ayudarte?'})
conversation = ChatGPT_conversation(conversation)
# print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

speech = SpeechModule()
recognition = VoiceRecognitionModule()

speech.talk('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

while True:
    text = recognition.recognize()
    print(text)
    # prompt = input('User:')
    if text:
        prompt = text
        conversation.append({'role': 'user', 'content': prompt})
        conversation = ChatGPT_conversation(conversation)
        speech.talk(conversation[-1]['content'].strip())
        # print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
        time.sleep(1)

    if text == "Eso es todo":
         break
    else:
        speech.talk("No te he entendido")
        time.sleep(1)
