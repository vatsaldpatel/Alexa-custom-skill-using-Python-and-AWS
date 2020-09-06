# Alexa-custom-skill-using-Python-and-AWS

In this example, I have created a custom **Alexa** skill using python and components of Amazon Web Services (AWS) like Lambda fuction and Dynamo DB.

## This is a demonstration video about what this code does. Please Watch.

[![Alexa Custom Skill using Python and AWS](http://img.youtube.com/vi/WbIyr3hq5Ps/0.jpg)](http://www.youtube.com/watch?v=WbIyr3hq5Ps "Alexa Custom Skill using Python and AWS")

#### The JSON output is of the following type

~~~~json
{
  "version": "1.0",
  "sessionAttributes": {},
  "statusCode": 200,
  "body": "Item added",
  "response": {
    "outputSpeech": {
      "type": "PlainText",
      "text": "Welcome to Jupyter doorbell skill."
    },
    "card": {
      "type": "Simple",
      "title": "SessionSpeechlet - Welcome",
      "content": "SessionSpeechlet - Welcome to Jupyter doorbell skill."
    },
    "reprompt": {
      "outputSpeech": {
        "type": "PlainText",
        "text": "I don't know if you heard me, welcome to your custom alexa application!"
      }
    },
    "shouldEndSession": false
  }
}
~~~~~

**Alexa :** Welcome to Jupyter doorbell skill.






*This code is about the Alexa Skill which I used to support my smart doorbell.*
