# -*- coding: utf-8 -*-
"""
@author: Vatsal patel
"""

from __future__ import print_function
import random
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time as tym
import decimal
from datetime import datetime,date,time


# --------------- Helpers that build all of the responses ----------------------

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EnrichedFrame')

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
        'statusCode': 200,
        'body': 'Item added',
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def hello_intent_handler():
    """ Message that is sent right when you launch your application
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello master."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def Snapshot_intent_handler(intent, session):
    """ Message that is sent right when you launch your application
    """
    session_attributes = {}
    card_title = "Welcome"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EnrichedFrame')
    speech_output = ""
    
    count_total =0
    #utc_dt = pytz.utc.localize(datetime.datetime.now())
    #now_ts_utc = (utc_dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    today = datetime.now()
    timestamp_curr = int(datetime.timestamp(today)) + 19785
    timestamp_beg = timestamp_curr - 300
    
    # For vehicle
    count_car = 0
    response1=table.scan(
    FilterExpression=Key('notification_type').eq('vehicle') & Key('approx_capture_timestamp').between(timestamp_beg, timestamp_curr)
    )
    
    speech_output_car = "A car was spotted at "
    
    for i in response1['Items']:
            count_car = count_car + 1
            x = json.dumps(i, cls=DecimalEncoder)
            y = json.loads(x)
            z = y['approx_capture_timestamp']
            readable = tym.ctime(z)
            hour = readable[11:16]
            speech_output_car += hour + " and "
    
    # For Unknown
    count_unknown = 0
    response2=table.scan(
    FilterExpression=Key('notification_type').eq('unknown') & Key('approx_capture_timestamp').between(timestamp_beg, timestamp_curr)
    )
    
    speech_output_unknown = "An Unknown was spotted at "
    
    for i in response2['Items']:
            count_unknown = count_unknown + 1
            x = json.dumps(i, cls=DecimalEncoder)
            y = json.loads(x)
            z = y['approx_capture_timestamp']
            readable = tym.ctime(z)
            hour = readable[11:16]
            speech_output_unknown += hour + " and "
    
    
    # For Known
    count_known = 0
    response3=table.scan(
    FilterExpression=Key('notification_type').eq('known') & Key('approx_capture_timestamp').between(timestamp_beg, timestamp_curr)
    )
    
    speech_output_known = ""
    
    for i in response3['Items']:
            count_known = count_known + 1
            x = json.dumps(i, cls=DecimalEncoder)
            y = json.loads(x)
            z = y['approx_capture_timestamp']
            name = y['external_image_id']
            readable = tym.ctime(z)
            hour = readable[11:16]
            speech_output_known += name + " was spotted at " + hour +  " , "
    
    count_total = count_known + count_unknown + count_car
    #speech_output += "Total " + str(count_total) + " things were spotted today. "
    
    if(count_known>0):
        speech_output += speech_output_known[:len(speech_output_known)-2] + "and "
    if(count_unknown>0):
        speech_output += speech_output_unknown[:len(speech_output_unknown)-5:] + "and "
    if(count_car>0):
        speech_output += " , " + speech_output_car[:len(speech_output_car)-5:]
    if(count_total == 0):
        speech_output = "No activity detected on the door in last five minutes"
        
    speech_output = speech_output[:len(speech_output)-4] + " ."
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def SpecificUpdate_intent_handler(intent, session):
    """ Message that is sent right when you launch your application
    """
    session_attributes = {}
    card_title = "Welcome"
    name = intent['slots']['name']['value']
    if(name.__contains__(" ")):
        namearr = name.split()
        name1 = namearr[0].capitalize()
        name2 = namearr[1].capitalize()
        name = name1 + name2
    speech_output = ""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EnrichedFrame')
    beg = datetime.combine(date.today(),time())
    today = datetime.now()
    timestamp_curr = int(datetime.timestamp(today)) + 19785
    timestamp_beg = int(datetime.timestamp(beg)) + 19785
    
    #Checking in Database
    count_known = 0
    response3=table.scan(
        FilterExpression=Key('notification_type').eq('known') & Key('approx_capture_timestamp').between(timestamp_beg, timestamp_curr)
        )
        
    speech_output_known = ""
        
    for i in response3['Items']:
            x = json.dumps(i, cls=DecimalEncoder)
            y = json.loads(x)
            namedb = y['external_image_id']
            if(name == namedb[:-1]):
                count_known += 1
                z = y['approx_capture_timestamp']
                readable = tym.ctime(z)
                hour = readable[11:16]
                speech_output_known += namedb + " was spotted at " + hour +  " , "
    
    if(count_known > 0):
        speech_output += speech_output_known[:len(speech_output_known)-3] + " . "
    else:
        speech_output += name + " was not at your home today."
    
    #speech_output += "Specific Intent " + name + speech_output_known
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)        

def update_intent_handler(intent, session):
    """ Message that is sent right when you launch your application
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = ""
    days = intent['slots']['days']['value']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EnrichedFrame')
    if (days == "today" or days == "today's"):
        count_total =0
        beg = datetime.combine(date.today(),time())
        today = datetime.now()
        timestamp_curr = int(datetime.timestamp(today)) + 19785
        timestamp_beg = int(datetime.timestamp(beg)) + 19785       
        
        # For vehicle
        count_car = 0
        response1=table.scan(
        FilterExpression=Key('notification_type').eq('vehicle') & Key('approx_capture_timestamp').between(timestamp_beg, timestamp_curr)
        )
        
        speech_output_car = "A car was spotted at "
        
        for i in response1['Items']:
                count_car = count_car + 1
                x = json.dumps(i, cls=DecimalEncoder)
                y = json.loads(x)
                z = y['approx_capture_timestamp']
                readable = tym.ctime(z)
                hour = readable[11:16]
                speech_output_car += hour + " and "
        
        speech_output_car = speech_output_car[:len(speech_output_car)-4]  
        # For Unknown
        count_unknown = 0
        response2=table.scan(
        FilterExpression=Key('notification_type').eq('unknown') & Key('approx_capture_timestamp').between(timestamp_beg, timestamp_curr)
        )
        
        speech_output_unknown = "An Unknown was spotted at "
        
        for i in response2['Items']:
                count_unknown = count_unknown + 1
                x = json.dumps(i, cls=DecimalEncoder)
                y = json.loads(x)
                z = y['approx_capture_timestamp']
                readable = tym.ctime(z)
                hour = readable[11:16]
                speech_output_unknown += hour + " and "
        
        speech_output_unknown = speech_output_unknown[:len(speech_output_unknown)-4]
        # For Known
        count_known = 0
        response3=table.scan(
        FilterExpression=Key('notification_type').eq('known') & Key('approx_capture_timestamp').between(timestamp_beg, timestamp_curr)
        )
        
        speech_output_known = ""
        
        for i in response3['Items']:
                count_known = count_known + 1
                x = json.dumps(i, cls=DecimalEncoder)
                y = json.loads(x)
                z = y['approx_capture_timestamp']
                name = y['external_image_id']
                readable = tym.ctime(z)
                hour = readable[11:16]
                speech_output_known += name + " was spotted at " + hour +  ", "
        
        speech_output_known = speech_output_known[:len(speech_output_known)-2]
        
        count_total = count_known + count_unknown + count_car
        speech_output += "Total " + str(count_total) + " things were spotted today. "
        
        if(count_known>0):
            speech_output += speech_output_known + " and "
        if(count_unknown>0):
            speech_output += speech_output_unknown + " and "
        if(count_car>0):
            speech_output += speech_output_car + " and "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    speech_output = speech_output[:-4] + " ."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_welcome_response():
    """ Message that is sent right when you launch your application
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Jupyter doorbell skill."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Jupyter. Have a nice day!."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "HelloIntent":
        return hello_intent_handler()
    elif intent_name == "UpdateIntent":
        return update_intent_handler(intent, session)
    elif intent_name == "SpecificUpdateIntent":
        return SpecificUpdate_intent_handler(intent, session)
    elif intent_name == "SnapshotIntent":
        return Snapshot_intent_handler(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])