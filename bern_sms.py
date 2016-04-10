from flask import Flask, request, redirect, session
import twilio.twiml
import os
from cleverbot import Cleverbot

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

known_demos = {'black', 'young'}

demo_to_response = {'black': "Bernie has a 100% rating from the NCAAP",
                'young': "Bernie gonna give you free education bro!"}

@app.route("/", methods=['GET', 'POST'])
def respond():
    cb = Cleverbot()
    resp = twilio.twiml.Response()
    
    body = request.values.get('Body', None)
    print request.values
    print body
    
    demos_mentioned = []
    
    for demo in known_demos:
        if demo in body.lower():
            demos_mentioned.append(demo)
    
    get_feedback = False
    if demos_mentioned:
        response = get_response_for_demos(demos_mentioned)
        #want to find out if what we gave was effective
        get_feedback = True
    else:
        #no demos were detected so no feedback should be gathered
        get_feedback = False
        
        #they might be giving us feedback from the previous convo
        feedback = handle_feedback(body, resp)
        
        if feedback:
            response = feedback
        else:
            #nope they're not, let's just use cleverbot to reply
            response = cb.ask(body)
    
    if get_feedback:
        store_cookies(demos_mentioned)
        response += "*****\nWas this information helpful? (Y/N)"
        
    resp.sms(response)

    #TODO: store user info (maybe?)
        
    return str(resp)

def get_response_for_demos(demos_mentioned):
    #logic to hit API and analyze response, doing dummy shit rn
    PREFACE_TEXT = "How Bernie Sanders helps the {} demographic: "
    
    response = ""
    for demo in demos_mentioned:
        response = response + PREFACE_TEXT.format(demo) + demo_to_response.get(demo) + "\n\n*****\n\n"
    
    return response

def store_cookies(demos):
    print 'storing ' + str(demos)
    session['demos'] = demos
    
def handle_feedback(body, sms_sender):
    '''
    handles the possible case where a user is giving us feedback from a previous
    conversation. only goes to this method if we didn't find an identifier
    
    returns a thank you string if there was feedback else None
    '''
    body_words = body.lower().split()
    YES = ['yes', 'y']
    NO = ['no', 'n']
    
    if any(x in YES + NO for x in body_words):
        #check if we even have talked to this guy before
        if session.get('demos'):
            #TODO:tell api to strengthen previous connections
            print 'strengthening connections :' + str(session['demos'])
            return "Thank you for your feedback! Your answers help make WhyIBern even stronger!"
    
    return None
    
    
if __name__ == "__main__":
    app.run(debug=True, 
            host=os.getenv('IP', '0.0.0.0'),
            port = int(os.getenv('PORT', '8080')))