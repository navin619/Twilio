from flask import Flask, request, redirect
import twilio.twiml
import os
from cleverbot import Cleverbot

app = Flask(__name__)

known_demos = {'black', 'young'}

demo_to_response = {'black': "Bernie has a 100% rating from the NCAAP",
                'young': "Bernie gonna give you free education bro!"}

@app.route("/", methods=['GET', 'POST'])
def respond():
    cb = Cleverbot()
    resp = twilio.twiml.Response()
    
    body = request.values.get('Body', None)
    
    demos_mentioned = []
    
    for demo in known_demos:
        if demo in body.lower():
            demos_mentioned.append(demo)
    
    if demos_mentioned:
        response = get_response_for_demos(demos_mentioned)
        #want to find out if what we gave was effective
        get_feedback = True
    else:
        response = cb.ask(body)
    
    resp.message(response)
    
    #TODO: get feedback
        
    return str(resp)

def get_response_for_demos(demos_mentioned):
    #logic to hit API and analyze response, doing dummy shit rn
    PREFACE_TEXT = "How Bernie Sanders helps the {} demographic: "
    
    response = ""
    for demo in demos_mentioned:
        response = response + PREFACE_TEXT.format(demo) + demo_to_response.get(demo) + "\n\n*****\n\n"
    
    return response
    
if __name__ == "__main__":
    app.run(debug=True, 
            host=os.getenv('IP', '0.0.0.0'),
            port = int(os.getenv('PORT', '8080')))