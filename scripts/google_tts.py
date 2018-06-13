#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Text-To-Speech API sample application .

Example usage:
    python quickstart.py
"""

import datetime
import time
import subprocess
DEFAULT_TIME_WAIT = 0.0 # Default time wait
def say(text, time_wait=DEFAULT_TIME_WAIT):
    ''' wait x second after playback '''
    print ("[TTS] " + text)
    # Get file name from datetime
    micro_int = datetime.datetime.now().microsecond
    filename = str(micro_int) + '.wav'

    # Call fanctions.
    quickstart(text=text,filename=filename) # create wav file
    sound(filename=filename)
    removeSoundFile(filename=filename)
    time.sleep(time_wait)


def removeSoundFile(filename):
    sound_cmd = 'rm ' + filename
    subprocess.call(sound_cmd.strip().split(' '))


def sound(filename):
    sound_cmd = 'aplay ' + filename
    subprocess.call(sound_cmd.strip().split(' '))
    #except OSError:
    #    print "[SOUND] Playback Failed."


def quickstart(text,filename): # text is <string>
    # [START tts_quickstart]
    """Synthesizes speech from the input string of text or ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        # -----------------------------------------
        # JA
        #language_code='ja-JP',

        # US
        language_code='en-US',
        name='en-US-Wavenet-F',
        #name='en-US-Standard-D',

        # CA
        #language_code='fr-CA',
        #name='fr-CA-Standard-D',
        #name='fr-CA-Standard-C',

        # -----------------------------------------

        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
        #ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(filename, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        #print('Audio content written to file "output.wav"')
    # [END tts_quickstart]


if __name__ == '__main__':
    # Using Example--->
    text = 'hello'
    say(text)

