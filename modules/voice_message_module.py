from vk_api.api import vapi
import speech_recognize
import bash

module_name = "Voice message recognizer"
module_version = "1.0"
module_author = "HydroGen"

def main(m, l):
    for attach in m.attachments:
        if attach.attachment_type == "amessage":
            # Get audio message
            audio_message = attach.attachment_value
            # Get amessage info
            result = vapi("docs.getById", "docs=\"%s\"" % audio_message)
            # Get file url
            url = result[0]['preview']['audio_msg']['link_mp3']
            print(url)
            bash.bash("wget -O in.mp3 %s" % url)
            response_from_google = speech_recognize.recognize("in.mp3")
            #if "ры" in str(response_from_google):
            bash.bash("mpg123 riig*")
            return response_from_google
