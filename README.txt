# HOW TO USE

1. Obtain your audio file.

2. Convert it to .FLAC using Python or this website: https://www.zamzar.com/uploadComplete.php?session=8f7a9b435a37a925babaa1c894c5f1a&tcs=Z92&from=wav&to=flac

A) Note you can use WAV if you change encoding=speech.RecognitionConfig.AudioEncoding.FLAC to encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16

3. Upload the .flac audio file to your Google Bucket: https://console.cloud.google.com/storage/browser/large-audio-files-for-transcription;tab=objects?project=praxis-study-394809&prefix=&forceOnObjectsSortingFiltering=false

4. Click on the name link in the table once uploaded, and copy the "gsutil URI"

5. Copy and paste that to AUDIO_LINK in main.py