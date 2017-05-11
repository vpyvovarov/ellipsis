import asyncio
import argparse
from lib.audio import mp3_to_flack
from lib.translate import translate_text
from lib.speech_to_text import transcribe_streaming, transcribe_sync

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

def tr(audio_chunck):
    text, conf = transcribe_sync(audio_chunck, 44100)
    translate_text("ru", text)

async def main(loop):
    from concurrent.futures import ThreadPoolExecutor
    e = ThreadPoolExecutor()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('stream', help='File to stream to the API')
    args = parser.parse_args()
    async for audio_chunck in mp3_to_flack(args.stream):
        print('---> NEW CHUNCK  <-----')
        loop.run_in_executor(e, tr, audio_chunck)

loop = asyncio.get_event_loop()
task = loop.create_task(main(loop))
ret = loop.run_until_complete(task)
