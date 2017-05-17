#!/usr/bin/env python
import asyncio
from google.cloud import speech, translate

class GoogleApi():

    def __init__(self, keyfile_path):
        self.speech_client = speech.Client.from_service_account_json(keyfile_path)
        self.translate_client = translate.Client.from_service_account_json(keyfile_path)

    def translate_text(self, target, text, model=translate.NMT):
        """Translates text into the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        result = self.translate_client.translate(text, target_language=target, model=model)

        print(u'Text: {}'.format(result['input']))
        print(u'Translation: {}'.format(result['translatedText']))
        print(u'Detected source language: {}'.format(
            result['detectedSourceLanguage']))
        return result['translatedText']

    def transcribe_streaming(self, audio_file, rate):
        audio_sample = self.speech_client.sample(
            stream=audio_file,
            encoding=speech.encoding.Encoding.FLAC,
            sample_rate=rate)

        alternatives = audio_sample.streaming_recognize('en-US')
        for alternative in alternatives:
            yield alternative.transcript, alternative.confidence

    def transcribe_sync(self, audio_file, rate):

        audio_sample = self.speech_client.sample(
            content=audio_file.read(),
            encoding=speech.encoding.Encoding.FLAC,
            sample_rate=rate)

        alternatives = audio_sample.sync_recognize('ru-RU')

        for alternative in alternatives:
            yield alternative.transcript, alternative.confidence

    async def transcribe_async(content, rate):
        speech_client = speech.Client()

        audio_sample = speech_client.sample(
            content=content,
            encoding=speech.Encoding.LINEAR16,
            sample_rate=rate)

        operation = audio_sample.async_recognize('en-US')

        while not operation.complete:
            operation.poll()
            await asyncio.sleep(2)

        alternatives = operation.results
        for alternative in alternatives:
            yield alternative.transcript, alternative.confidence