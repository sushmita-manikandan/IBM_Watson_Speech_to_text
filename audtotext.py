#import the watson developer cloud
from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback

speech_to_text = SpeechToTextV1(
    username='213....',
    password='fYTp....', #write the username and password provided in the credentials section of IBM Watson within ' '
    url='https://stream.watsonplatform.net/speech-to-text/api')

print(json.dumps(speech_to_text.list_models(), indent=2))

print(json.dumps(speech_to_text.get_model('en-US_BroadbandModel'), indent=2))

#specify path name like so
with open(join(dirname(__file__), '/Users/sushmitamanikandan/Downloads/sale-convo.mp3'),'rb') as audio_file:
    result = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/mp3',
                timestamps=True,
                word_confidence=True,speaker_labels=True)
    print(json.dumps(result,indent=2))

#result holds the entire transcription - unparsed. It needs to be abstracted as per the use case
    with open('file.txt', 'w') as file:
        file.write(json.dumps(result))
    # print("Done writing the whole file")

# Example using websockets
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_transcription_complete(self):
        print('Transcription completed')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)

mycallback = MyRecognizeCallback()
with open(join(dirname(__file__), '/Users/sushmitamanikandan/Downloads/sale-convo.mp3'),
          'rb') as audio_file:
    speech_to_text.recognize_using_websocket(audio=audio_file, content_type="audio/l16; rate=44100",
                                             recognize_callback=mycallback)