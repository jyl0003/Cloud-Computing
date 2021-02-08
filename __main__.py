import logging
import json
import base64
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(args):
    #authenticate with watson using AssistantV2
    authenticator = IAMAuthenticator("HUbLrY65P2rO3yp5aYuDFgKngqmT1idbm_AlULK-0m94")
    assistant = AssistantV2(
        version='2020-04-01',
        authenticator=authenticator
    )
    assistant.set_service_url('https://gateway.watsonplatform.net/assistant/api')

    #start a "session" (tell IBM to create and manage a token for you that you can use for authentication until you terminate the session)
    #tip, you can get your assistant ID by looking at the URL in the browser for your assistant
    #its right after the /assistant part of the url
    session = assistant.create_session(assistant_id="dd517c2b-f081-4228-b018-26d199fe516e").get_result()
    textValue = "nothing"
    #GET and Translate message from Alexa
    try:
        logging.warning("Testing args")
        logging.warning(args.get('__ow_body'))
        if (args  == None):
            logging.warning("args is empty")
        arguments = args.get('__ow_body')
        encoded_bytes = arguments.encode('ascii')
        decoded_bytes = base64.b64decode(encoded_bytes)
        decoded = decoded_bytes.decode('ascii')

        test = json.loads(decoded)
        textValue = test['request']['intent']['slots']['EverythingSlot']['slotValue']['value']
        #decoded = encoded.decode('base64')
        #decoded = args.get('__ow_body').decode('base64').strip()
        logging.warning("Decoded type: ")
        print("\ndecoded:", decoded)
        logging.warning(type(test))
        #return{"test:" : textValue}
    except:
        return {"body": "Could not decode body from Base64."}
        
    #send message to watson and display response received from watson
    message = assistant.message(assistant_id="dd517c2b-f081-4228-b018-26d199fe516e",session_id=session["session_id"],input= {'message_type': 'text','text': textValue}).get_result()
    print("test:", message)
    logging.warning("message type")
    textResponseList = message["output"]["generic"]
    textResponse = textResponseList[0]["text"]
    #return json.dumps(message, indent=4, sort_keys=True)
    #return {"test", message}
    #terminate the session (tell IBM that you are done with your token)
    response = assistant.delete_session(assistant_id="dd517c2b-f081-4228-b018-26d199fe516e", session_id=session["session_id"]).get_result()
    print(json.dumps(response, indent=4, sort_keys=True))
    jsonDictionary = {"version": "1.0", "response": {"outputSpeech": {"type":"PlainText","text":textResponse},"shouldEndSession":False }}
   # jsonReturn = json.dumps(jsonDictionary, indent=4,sort_keys=True)
    return jsonDictionary
