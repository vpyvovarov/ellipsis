import asyncio
import argparse

from lib.audio import mp3_to_flack
from lib.doctor_watson import WatsonApi
from lib.google_api import GoogleApi


# async def main():
#     parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
#     parser.add_argument('stream', help='File to stream to the API')
#     args = parser.parse_args()
#     async for audio_chunck in mp3_to_flack(args.stream):
#         async for data in transcribe_streaming(audio_chunck, 44100):
#             print(data)
#
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

def tr(audio_chunck, watson_user, watson_pass, google_key_path):
    google = GoogleApi(google_key_path)
    text, conf = google.transcribe_sync(audio_chunck, 44100)
    translation = google.translate_text("en", text)
    output_file = 'output2.wav'
    WatsonApi(username=watson_user, password=watson_pass).synthesize_speech(text=translation, output_file=output_file)

async def main(loop):
    from concurrent.futures import ThreadPoolExecutor
    e = ThreadPoolExecutor()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('stream', help='File to stream to the API')
    parser.add_argument('watson_user', help='User for Watson API')
    parser.add_argument('watson_pass', help='Password for Watson API')
    parser.add_argument('google_key_path', help='Path to google key file')

    args = parser.parse_args()
    async for audio_chunck in mp3_to_flack(args.stream):
        print('---> NEW CHUNCK  <-----')

        loop.run_in_executor(e, tr, audio_chunck, args.watson_user, args.watson_pass, args.google_key_path)

loop = asyncio.get_event_loop()
task = loop.create_task(main(loop))
ret = loop.run_until_complete(task)


# loop.run_until_complete(asyncio.gather(
#     factorial("A", 2),
#     factorial("B", 3),
#     factorial("C", 4),
# ))
