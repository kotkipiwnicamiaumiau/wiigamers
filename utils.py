from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import storage
import random
import string
import json
from moviepy.editor import *
from summarize_abstract import summarize_title
from summarize_wybiorcze import summarize

# transkrybowanie pliku audio. Przyjmuje gcloud-storage uri, zwraca
# (plaintext, zdania z timestampami)


def transcribe(storage_uri):
    """
    Performs synchronous speech recognition on an audio file

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1p1beta1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.mp3'

    # The language of the supplied audio
    language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    enable_word_time_offsets = True

    enable_automatic_punctuation = True

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "enable_word_time_offsets": enable_word_time_offsets,
        "enable_automatic_punctuation": enable_automatic_punctuation
    }
    audio = {"uri": storage_uri}

    plaintext = ""
    sentences = []

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]

        plaintext += alternative.transcript + ' '
        sentences.append(
            (alternative.transcript,
             (alternative.words[0].start_time.seconds,
              alternative.words[0].start_time.nanos)))
    return (plaintext, sentences)


# wrzucanie plików do cloud storage.
def upload_blob(source_file_name):
    """Uploads a file to the bucket."""
    bucket_name = "alamakota1"
    # source_file_name = "local/path/to/file"
    destination_blob_name = ''.join(
        random.choices(
            string.ascii_uppercase +
            string.digits,
            k=5))

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print("uploading")
    blob.upload_from_filename(source_file_name)
    link = f"gs://alamakota1/{destination_blob_name}"
    print("uploaded")

    return link


# extracts .mp3 file from video and returns it's relative path
def extract_audio(source_file_name):
    print("extracting")
    video = VideoFileClip(source_file_name)
    audio = video.audio
    path = 'static/audio/' + \
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.mp3'
    audio.write_audiofile(path)
    print("extracted")
    return path


def test(res):
    print(res[0])
    print("------------------------------------------")
    print(res[1])

def handle_video(video_id):
    filepath = 'static/vid/'+video_id+'.mp4'
    #to trwa długo, więc jeśli chcecie testować to sobie zapiszcie wartosci
    (plaintext, sentences_timestamps) = transcribe(upload_blob(extract_audio(filepath)))

    #magia maksa i kajtka
    title=summarize_title(plaintext)
    summary_sentences = summarize(plaintext) #zwraca tablice zdań
    summary=[("zdanie1", 5), ("zdanie2", 70)] #tutaj maks użyj mojej tablicy sentences_timestamps i tablicy summary_sentences
    transcript=["zdania dla pierwszej minuty", "zdania dla drugiej minuty", "zdania dla trzeciej minuty"] #tutaj posortuj zdania z transcript co minute

    summary_json = json.dumps(summary)
    transcript_json = json.dumps(transcript)

    db = sqlite3.connect("kotki.db")
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO videos(title,id, summary,transcript) VALUES(?,?,?,?)''', (time, video_id, summary_json, transcript_json))
    db.commit()
    db.close()
    

# example
#test(transcribe(upload_blob(extract_audio("vid/A2G1Z.mp4"))))
