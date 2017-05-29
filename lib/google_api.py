#!/usr/bin/env python
import asyncio
from google.cloud import speech, translate
from lib.log import get_logger


class GoogleApi():

    def __init__(self, keyfile_path):
        self.log = get_logger('Google API')
        self.speech_client = speech.Client.from_service_account_json(keyfile_path)
        self.translate_client = translate.Client.from_service_account_json(keyfile_path)
        self.log.info('Init successful')

    def translate_text(self, target, text, model=translate.NMT):
        """Translates text into the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        result = self.translate_client.translate(text, target_language=target, model=model)

        self.log.info('Text: {}'.format(result['input']))
        self.log.info('Translation: {}'.format(result['translatedText']))
        self.log.info('Detected source language: {}'.format(result['detectedSourceLanguage']))

        return result['translatedText']

    def transcribe_streaming(self, audio_file, rate):
        audio_sample = self.speech_client.sample(
            stream=audio_file,
            encoding=speech.encoding.Encoding.FLAC,
            sample_rate=rate)

        alternatives = audio_sample.streaming_recognize('en-US')
        for alternative in alternatives:
            self.log.info('Text: {}'.format(alternative.transcript))
            self.log.info('Confidence: {}'.format(alternative.confidence))
            yield alternative.transcript, alternative.confidence

    def transcribe_sync(self, audio_file, rate):
        audio_sample = self.speech_client.sample(
            content=audio_file.read(),
            encoding=speech.encoding.Encoding.FLAC,
            sample_rate=rate)

        res = audio_sample.sync_recognize('ru-RU')[0]

        self.log.debug('Text: {}'.format(res.transcript))
        self.log.info('Confidence: {}'.format(res.confidence))
        return res.transcript


    async def transcribe_async(self, content, rate):
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
            self.log.debug('Text: {}'.format(alternative.transcript))
            self.log.info('Confidence: {}'.format(alternative.confidence))
            yield alternative.transcript, alternative.confidence