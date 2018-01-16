import io
import csv
import argparse
#from tqdm import tqdm

def transcribe_gcs(gcs_uri, outputfile):
  """Asynchronously transcribes the audio file specified by the gcs_uri."""
  from google.cloud import speech
  from google.cloud.speech import enums
  from google.cloud.speech import types
  
  # build client and configuration
  client = speech.SpeechClient()
  audio = types.RecognitionAudio(uri=gcs_uri)
  config = types.RecognitionConfig(
      encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
      sample_rate_hertz=16000,
      language_code='en-US')
  operation = client.long_running_recognize(config, audio)
  
  # perform operation as defined in configuration
  print('Waiting for operation to complete...')
  response = operation.result(timeout=300)
  
  # Print the first guess of all the consecutive results.
  writer = csv.writer(open(outputfile,'wb'))
  for result in response.results:
    print('{}'.format(result.alternatives[0].transcript))
    writer.writerow([result.alternatives[0].transcript, result.alternatives[0].confidence])


if __name__ == '__main__':
  for i in range(1,31):#tqdm(range(1,31)):
    gcs_uri_root = 'gs://project.root.url/'
    inputfile = ('' + str(i).zfill(2) + 'Label.flac')
    outputfile = 'output/' + str(i).zfill(2) + 'Label.csv'
    print(inputfile, outputfile)
    transcribe_gcs(inputfile, outputfile)