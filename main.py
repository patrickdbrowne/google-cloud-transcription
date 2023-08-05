# import argparse

# from google.cloud import speech

# audio_file = 'test.wav'

# def transcribe_file(speech_file: str) -> speech.RecognizeResponse:
#     """Transcribe the given audio file."""
#     client = speech.SpeechClient()

#     with open(speech_file, "rb") as audio_file:
#         content = audio_file.read()

#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         #sample_rate_hertz=16000,
#         language_code="en-US",
#     )

#     response = client.recognize(config=config, audio=audio)

#     # Each result is for a consecutive portion of the audio. Iterate through
#     # them to get the transcripts for the entire audio file.
#     for result in response.results:
#         # The first alternative is the most likely one for this portion.
#         print(f"Transcript: {result.alternatives[0].transcript}")

#     return response

# transcribe_file(audio_file)



# Imports the Google Cloud client library

AUDIO_LINK = "gs://large-audio-files-for-transcription/Jordie-gets-cranky.flac"

# def transcribe_gcs(gcs_uri: str) -> str:
#     """Asynchronously transcribes the audio file specified by the gcs_uri.

#     Args:
#         gcs_uri: The Google Cloud Storage path to an audio file.

#     Returns:
#         The generated transcript from the audio file provided.
#     """
#     from google.cloud import speech

#     client = speech.SpeechClient()

#     audio = speech.RecognitionAudio(uri=gcs_uri)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
#         # sample_rate_hertz=44100,
#         language_code="en-US",

#     )

#     operation = client.long_running_recognize(config=config, audio=audio)

#     print("Waiting for operation to complete...")
#     response = operation.result(timeout=90)

#     transcript_builder = []
#     # Each result is for a consecutive portion of the audio. Iterate through
#     # them to get the transcripts for the entire audio file.
#     for result in response.results:
#         # The first alternative is the most likely one for this portion.
#         transcript_builder.append(f"\nTranscript: {result.alternatives[0].transcript}")
#         transcript_builder.append(f"\nConfidence: {result.alternatives[0].confidence}")

#     transcript = "".join(transcript_builder)

#     return transcript
# print(transcribe_gcs(AUDIO_LINK))
################################## SPEAKER DIARISATION BELOW #####################
# from google.cloud import speech


# def transcribe_diarization_gcs_beta(gcs_uri: str) -> bool:
#     """Transcribe a remote audio file (stored in Google Cloud Storage) using speaker diarization.

#     Args:
#         gcs_uri: The Google Cloud Storage path to an audio file.

#     Returns:
#         True if the operation successfully completed, False otherwise.
#     """

#     client = speech.SpeechClient()

#     speaker_diarization_config = speech.SpeakerDiarizationConfig(
#         enable_speaker_diarization=True,
#         # min_speaker_count=2,
#         # max_speaker_count=2,
#     )

#     # Configure request to enable Speaker diarization
#     recognition_config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
#         language_code="en-US",
#         # sample_rate_hertz=8000,
#         diarization_config=speaker_diarization_config,
#         enable_automatic_punctuation=True,
#     )

#     # Set the remote path for the audio file
#     audio = speech.RecognitionAudio(
#         uri=gcs_uri,
#     )

#     # Use non-blocking call for getting file transcription
#     response = client.long_running_recognize(
#         config=recognition_config, audio=audio
#     ).result(timeout=300)

#     # The transcript within each result is separate and sequential per result.
#     # However, the words list within an alternative includes all the words
#     # from all the results thus far. Thus, to get all the words with speaker
#     # tags, you only have to take the words list from the last result
#     result = response.results[-1]
#     words_info = result.alternatives[0]

#     print(next(word_obj for word_obj in words_info if word_obj["start"]["seconds"] == 224))

#     # print(words_info)
#     # Print the output
#     # for word_info in words_info:
#     #     print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")
#     # return word_info

# transcribe_diarization_gcs_beta(AUDIO_LINK)


################# USE THIS AND GRAMMARLY TO MAKE SURE TRANSCRIPT MAKES SENSE.
from google.cloud import speech
import datetime

# up to 480 minutes
def transcribe_gcs_with_word_time_offsets(gcs_uri: str,) -> speech.RecognizeResponse:
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,

        # CHANGE SAMPLE_RATE_HERTZ BASED ON AUDIO ENCODING FORMAT
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    
    print("Waiting for operation to complete...")

    # Either will respond with transcript, or timeout of 10 000 seconds, whichever happens first.
    result = operation.result(timeout=10000)

    open('transcript.txt', 'w').close()
    transcript_file = open('transcript.txt', 'a')

    for result in result.results:
        alternative = result.alternatives[0]
        # Convert start_time [H:M:S.f] to [H:M:S] (no float values)
        formatted_time = str(alternative.words[0].start_time)
        if '.' in formatted_time:
            time_object = datetime.datetime.strptime(formatted_time, '%H:%M:%S.%f')
            formatted_time = time_object.strftime('%H:%M:%S')
        else:
            time_object = datetime.datetime.strptime(formatted_time, '%H:%M:%S')
            formatted_time = time_object.strftime('%H:%M:%S')

        transcript_file.write(f"[{formatted_time}]\t\t{alternative.transcript}\n\n")

    transcript_file.close()
    return result
transcribe_gcs_with_word_time_offsets(AUDIO_LINK)