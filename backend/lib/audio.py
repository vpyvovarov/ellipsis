#!/usr/bin/env python
import argparse
import io
from pydub import AudioSegment
import StringIO
from pydub.utils import which
from google.cloud import speech

def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    text = ""

    speech_client = speech.Client()
    # stream_file = mp3_to_flack(stream_file)
    for audio_file in mp3_to_flack(stream_file):
    # with io.open(stream_file, 'rb') as audio_file:
        audio_sample = speech_client.sample(
            stream=audio_file,
            encoding=speech.encoding.Encoding.FLAC,
            sample_rate=44100)

        alternatives = audio_sample.streaming_recognize('en-US')
        print "-----> SO FAR SO GOOD <-----"
        for alternative in alternatives:
            # print('Finished: {}'.format(alternative.is_final))
            # print('Stability: {}'.format(alternative.stability))
            # print('Confidence: {}'.format(alternative.confidence))
            text += alternative.transcript
    return text

def mp3_to_flack(stream_file):
    AudioSegment.converter = which("ffmpeg")
    wav_audio = AudioSegment.from_file(StringIO.StringIO(stream_file)) #frame_rate=44100, format="mp3")#, frame_rate=44100)
    chunk_size=10000
    limit = 0
    # import pdb; pdb.set_trace()
    # print len(wav_audio.frame_rate)
    while len(wav_audio) > limit:
        dest = StringIO.StringIO()
        print "FROM %s TO %s" % (limit, limit+chunk_size)
        wav_audio[limit:limit+chunk_size].export(dest, format="flac")
        limit += chunk_size
        yield dest

#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description=__doc__,
#         formatter_class=argparse.RawDescriptionHelpFormatter)
#     parser.add_argument('stream', help='File to stream to the API')
#     args = parser.parse_args()
#     transcribe_streaming(args.stream)