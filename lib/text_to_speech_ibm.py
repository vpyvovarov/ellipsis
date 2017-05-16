# coding=utf-8
from watson_developer_cloud import TextToSpeechV1

# print(json.dumps(text_to_speech.voices(), indent=2))
class WatsonApi():

    def __init__(self, username, password):
        self.tts_api = TextToSpeechV1(username=username, password=password, x_watson_learning_opt_out=True)

    def synthesize_speach(self, text, output_file, voice="en-US_AllisonVoice"):
        try:
            with open(output_file, 'wb') as audio_file:
                audio_file.write(self.tts_api.synthesize(text, accept='audio/wav', voice=voice))
        except Exception as e:
            print(e)
            import sys
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            print(sys.exc_info())
