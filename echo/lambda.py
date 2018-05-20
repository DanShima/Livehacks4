from __future__ import print_function
import urllib2


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session

    }



def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():


    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the mood player. " \
                    "Please tell me your current mood by saying, for example " \
                    "I feel sad"

    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your mood"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the mood player. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_mood_attributes(mood):
    return {"currentMood": mood}

def set_mood_in_session(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Mood' in intent['slots']:
        mood = intent['slots']['Mood']['value']
        session_attributes = create_mood_attributes(mood)
        speech_output = "I now know your mood is " + mood


        reprompt_text = "You can ask me your mood by saying, " \
                        "what's my mood?"
    else:
        speech_output = "I'm not sure what your mood is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your mood is. " \
                        "You can tell me your mood by saying, " \
                        "my mood is red."

    if mood == "sad":
        contents = urllib2.urlopen("http://56f66c9a.ngrok.io/?col=blue").read()
    elif mood == "angry":
        contents = urllib2.urlopen("http://56f66c9a.ngrok.io/?col=green").read()
    elif mood == "nostalgic":
        contents = urllib2.urlopen("http://56f66c9a.ngrok.io/?col=white").read()
    else:
        contents = urllib2.urlopen("http://56f66c9a.ngrok.io/?col=red").read()

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_mood_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "mood" in session.get('attributes', {}):
        mood = session['attributes']['mood']
        speech_output = "Your mood is " + mood + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your mood is. " \
                        "You can say, my mood is sad."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyMoodIntent":
        return set_mood_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):

    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
