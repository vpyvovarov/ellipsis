#!/usr/bin/env python
import argparse
import io
from pydub import AudioSegment
import StringIO
from pydub.utils import which
from google.cloud import speech

def transcribe_streaming(audio_file, rate):
    """Streams transcription of the given audio file."""
    speech_client = speech.Client()
    audio_sample = speech_client.sample(
        stream=audio_file,
        encoding=speech.encoding.Encoding.FLAC,
        sample_rate=rate)

    alternatives = audio_sample.streaming_recognize('en-US')
    for alternative in alternatives:
    return alternatives.transcript, alternative.confidence


