import asyncio
import argparse

from concurrent.futures import ThreadPoolExecutor

from lib.audio import mp3_to_flack
from lib.doctor_watson import WatsonApi
from lib.google_api import GoogleApi
from lib.conf import Config
from lib.log import get_logger


pool = ThreadPoolExecutor()
log = get_logger(context='main')


def to_text(audio_chunck, google_client, chunk_number):
    return google_client.transcribe_sync(audio_chunck, 44100), chunk_number


async def main(loop):

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('stream', help='File to stream to the API')
    parser.add_argument('watson_user', help='User for Watson API')
    parser.add_argument('watson_pass', help='Password for Watson API')
    parser.add_argument('google_key_path', help='Path to google key file')

    args = parser.parse_args()
    futures_to_text = list()

    async for audio_chunck, chunk_number in mp3_to_flack(args.stream):
        log.info('Get new audio chunck')
        google_client = GoogleApi(args.google_key_path)
        futures_to_text.append(loop.run_in_executor(pool, to_text, audio_chunck, google_client, chunk_number))

    completed, pending = await asyncio.wait(futures_to_text)
    results = [t.result() for t in completed]
    results.sort(key=lambda a: a[-1])

    text = "".join([i[0] for i in results])
    translation = google_client.translate_text("en", text)
    log.info('translation complete')
    output_file = 'output2.wav'
    WatsonApi(username=args.watson_user, password=args.watson_pass).\
        synthesize_speech(text=translation, output_file=output_file)
    log.info('synthesize speech complete')


loop = asyncio.get_event_loop()
task = loop.create_task(main(loop))
ret = loop.run_until_complete(task)
