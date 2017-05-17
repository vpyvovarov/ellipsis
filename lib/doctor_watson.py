# coding=utf-8
from watson_developer_cloud import TextToSpeechV1


class WatsonApi():

    def __init__(self, username, password):
        self.tts_api = TextToSpeechV1(username=username, password=password, x_watson_learning_opt_out=True)

    def synthesize_speach(self, text, output_file, voice="en-US_AllisonVoice"):
        '''
        Make audio file from text
        :param text: str. Text from which speach whould be synthesize
        :param output_file: str. Path for output file
        :param voice: str. For getting this parameter look to `get_voices` method
        :return: None
        '''
        with open(output_file, 'wb') as audio_file:
            audio_file.write(self.tts_api.synthesize(text, accept='audio/wav', voice=voice))

    def get_voices(self, language=None, gender=None):
        '''
        Return list of voice names. This is need for synthesize_speach method
        
        :param language: str. language in format 'en-US'
        :param gender: str. One of ['male', 'female'] 
        :return: list of voice names
        '''
        response = self.tts_api.voices()
        # filter out
        filter_by_lang = lambda voice_dict: language is None or language.lower() == voice_dict["language"].lower()
        filter_by_gender = lambda voice_dict: gender is None or gender.lower() == voice_dict["gender"].lower()
        voices = \
            [voice['name'] for voice in response.get('voices', []) if filter_by_lang(voice) and filter_by_gender(voice)]

        return voices
