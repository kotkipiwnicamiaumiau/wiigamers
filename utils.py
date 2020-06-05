from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import storage
import random, string

#transkrybowanie pliku audio. Przyjmuje gcloud-storage uri, zwraca (plaintext, zdania z timestampami)
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

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "enable_word_time_offsets": enable_word_time_offsets
    }
    audio = {"uri": storage_uri}

    plaintext = ""
    sentences = []

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]

        plaintext += alternative.transcript + ' ';
        sentences.append((alternative.transcript, (alternative.words[0].start_time.seconds, alternative.words[0].start_time.nanos)))

    return (plaintext, sentences)


#wrzucanie plików do cloud storage. ('alamakota1', plik(path))
def upload_blob(bucket_name, source_file_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    destination_blob_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

 
    link = blob.path_helper(bucket_name, destination_blob_name)
    link = 'gs://' + link

    return link



#stranscribe("gs://alamakota1/coronavirus.mp3");
print(upload_blob('alamakota1', "/Users/adamszokalski/Projekty/Hackathony/Hackyeah-2020/test.mp3"))