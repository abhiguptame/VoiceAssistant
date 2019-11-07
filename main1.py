#!/usr/bin/pythonN
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import os
import dialogflow
from google.protobuf.json_format import MessageToDict
from google.api_core.exceptions import InvalidArgument
from flask_cors import CORS

##from backend
import pandas as pd
import pyodbc
import json


db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)
CORS(app)



class Responder(Resource):
    def get(self, text):
        if(text):
            received = text
        else:
            received = ""
        reply_text = "Hi there! " + text
        result = { "reply" : "test"}
        return jsonify(reply= reply_text)

    def post(self):
        # text_query

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

        DIALOGFLOW_PROJECT_ID = 'testbot-256009'
        DIALOGFLOW_LANGUAGE_CODE = 'en'
        SESSION_ID = 'me'
        t= True

        #text_to_be_analyzed = "plot a bar graph of companies and events"
        text_to_be_analyzed = request.json['text_query']
        #request.json['text_query']
        print(request.json)
        
        #text_to_be_analyzed = input()
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise

        try:
            moveforward = response.query_result.all_required_params_present
        except:
            moveforward = False

        if moveforward == False:
            json_packet = {'response': response.query_result.fulfillment_text,
                           'graph': False
                            }
            return json_packet


        ##### Small talk supports to be added here
        #try:
        #    moveforward2 = response.query_result.action
        #    json_packet = {'response': response.query_result.fulfillment_text
        #                    }
        #    return json_packet
        #except:
        #    pass




        ## if fulfillment not done


        ##

            #print("Query text:", response.query_result.query_text)
            #print("Detected intent:", response.query_result.intent.display_name)
            #print("Detected intent confidence:", response.query_result.intent_detection_confidence)
            #print("Keywords detected:", response.query_result. )
            #print("Fulfillment text:", response.query_result.fulfillment_text)
        test= response.query_result.parameters
        output= MessageToDict(test)
            #print(output['AY'])

            ##response example
        #    query_result {
        #  query_text: "show companies for year 2018"
        #  parameters {
        #    fields {
        #      key: "AY"
        #      value {
        #        list_value {
        #          values {
        #            string_value: "2018"
        #          }
        #        }
        #      }
        #    }
        #    fields {
        #      key: "ToFind"
        #      value {
        #        string_value: "CompanyName"
        #      }
        #    }
        #  }
        #  all_required_params_present: true
        #  fulfillment_text: "Here are your required plots."
        #  fulfillment_messages {
        #    text {
        #      text: "Here are your required plots."
        #    }
        #  }
        #  intent {
        #    name: "projects/testbot-256009/agent/intents/9f59df0f-cd02-4401-aa92-dd31e32239d6"
        #    display_name: "PlotGraph"
        #  }
        #  intent_detection_confidence: 0.7113070487976074
        #  language_code: "en"
        #}

            ##backend start
       # conn = pyodbc.connect(
        #    'DRIVER={SQL Server}; SERVER=INBENSAMAGUPTA\SQLEXPRESS; DATABASE=datastore; Trusted_Connection=yes')

        #sql = """
        #    select * from datamine
        #    """

        #datatable = pd.read_sql(sql, conn)
        #print(datatable.tail())

        datatable = pd.read_csv('DB.csv')
        #print(datatable.head(5))

            ##Modifications to table needed AY:Date conversion like df['Date'] =pd.to_datetime(df.Date)

            # API gets us a

        a=  {
                'question1': None, #kya karna hai
                'ToFind': None,
                'CompanyName': None,
                'CompanyLocation' : None,
                'AuthorityName' : None,
                'intent': "Count",
                'ReturnID':None,
                'last':None,
                'EventName':None,
                'AY':None, 
                'Ground':None,
                'GroundStatus':None,
                'duplicate_entries': None,
                'plot_type':None
                }


        text_to_speech_aider=  {
                'CompanyName': "Companies",
                'CompanyLocation': "locations",
                'AuthorityName' : "Authorities",
                'ReturnID':'Return ID',
                'EventName':"events",
                'AY':"assessment years",
                'Ground':"grounds",
                'records':"records"
                }

            ##Over writing function from dialogflow
            #a['intent']= str(response.intent.display_name)
            #output_intent= MessageToDict(response.query_result.intent)
            #print(output_intent['display_name'])

        a['intent']=response.query_result.intent.display_name
        try:
                a['ToFind']=output['ToFind']
                if  a['ToFind'] == []:
                     a['ToFind'] = ['CompanyName']
        except:
                pass
        try:
                a['CompanyName']=output['CompanyName']
                if  a['CompanyName'] == []:
                     a['CompanyName'] = None
        except:
                pass
        try:
                a['CompanyLocation']=output['CompanyLocation']
                if  a['CompanyLocation'] == []:
                     a['CompanyLocation'] = None
        except:
                pass
        try:
                a['AuthorityName']=output['AuthorityName']
                if  a['AuthorityName'] == []:
                     a['AuthorityName'] = None
        except:
                pass
        try:
                a['ReturnID']=output['ReturnID']
                if  a['ReturnID'] == []:
                     a['ReturnID'] = None
        except:
                pass
        try:
                a['EventName']=output['EventName']
                if  a['EventName'] == []:
                     a['EventName'] = None
        except:
                pass
        try:
                a['AY']= output['AY']
                if  a['AY'] == []:
                     a['AY'] = None
        except:
                pass
        try:
                a['Ground']=output['Ground']
                if  a['Ground'] == []:
                     a['Ground'] = None
        except:
                pass
        try:
                a['GroundStatus']=output['GroundStatus']
                if  a['GroundStatus'] == []:
                     a['GroundStatus'] = None
        except:
                pass
        try:
                a['duplicate_entries']=output['duplicate_entries']
                if  a['duplicate_entries'] == "":
                     a['duplicate_entries'] = None
        except:
                pass
        try:
                a['plot_type']=output['plot_type']
                if  a['plot_type'] == []:
                     a['plot_type'] = None
        except:
                pass

            #a['ToFind']=["EventName"]
            #a['AuthorityName']=["Assessing officer"]


            #keys_questions = [
            #    'how',
            #    'what',
            #    'where',
            #    'when',
            #    'maximum',
            #    'greatest',
            #    'minimum',
            #    'count',
            #    'least'
            #]


            #def question_type(list):
            #    for element in list:
            #        for x in keys_questions:
            #            if (element == x):
            #                a['question1'] = element
            #                # emphasiser sub parts
            #                if (element == 'last'):
            #                    a['last'] = "yes"


            ##question_type(input_attr)


            # functions of data konsa uthana hai sorter functions
        def sorter_location(x):
                x = x[x['CompanyLocation'].isin(a['CompanyLocation'])]
                return x

        def sorter_companyName(x):
                x = x[x['CompanyName'].isin(a['CompanyName'])]
                return x

        def sorter_eventName(x):
                x = x[x['EventName'].isin(a['EventName'])]
                return x

        def sorter_authorityName(x):
                x = x[x['AuthorityName'].isin(a['AuthorityName'])]
                return x

        def sorter_assessmentYear(x):
                x = x[x['AY'].isin(a['AY'])]
                return x

        def sorter_ground(x):
                x = x[x['Ground'].isin(a['Ground'])]
                return x

        def sorter_groundStatus(x):
                x = x[x['GroundStatus'].isin(a['GroundStatus'])]
                return x

            ## Fall through filter
        def sorter_main(x):
                if a['CompanyName'] is not None:
                    x = sorter_companyName(x)

                if a['CompanyLocation'] is not None:
                    x = sorter_location(x)

                if a['EventName'] is not None:
                    x = sorter_eventName(x)

                if a['AuthorityName'] is not None:
                    x = sorter_authorityName(x)

                if a['AY'] is not None:
                    x = sorter_assessmentYear(x)

                if a['Ground'] is not None:
                    x = sorter_ground(x)

                if a['GroundStatus'] is not None:
                    x = sorter_groundStatus(x)

                return x
        
        ### intents added here---
        if a['intent'] == "Count":
                datatable = sorter_main(datatable)
                #print(datatable)

                if a['ToFind'] == [""]:
                     a['ToFind']=["CompanyName"]
                     temp =  a['ToFind'][0]

                else:
                     temp = a['ToFind'][0]

                datatable = datatable[[temp]]
                #print(datatable.head(5))
                if a['duplicate_entries'] is None:
                    datatable= datatable.drop_duplicates()
              
                x = datatable[temp].count()

                if a['duplicate_entries'] is not None:
                    temp='records'

                #return Json area
                reply = "I scanned through the data and I found the total number of {} to be {}".format(text_to_speech_aider[temp],x)
                json_packet = {'response': reply,
                               'graph': False
                            }
                #json_response = json.dumps(json_packet)
                return jsonify(json_packet)

        if a['intent'] == "test_fulfilment":
                json_packet = {'response': response.query_result.fulfillment_text,
                               'graph': False
                            }
                json_packet = jsonify(json_packet)
                json_packet.headers.add('Access-Control-Allow-Origin', '*')
                #json_response = json.dumps(json_packet)
                return json_packet

        ##small talk ones:
        if  a['intent'] == "Default Welcome Intent":
                json_packet = {'response': response.query_result.fulfillment_text,
                               'graph': False
                            }
                json_packet = jsonify(json_packet)
                json_packet.headers.add('Access-Control-Allow-Origin', '*')
                #json_response = json.dumps(json_packet)
                return json_packet

        if a['intent'] == '' :
                json_packet = {'response': response.query_result.fulfillment_text,
                               'graph': False
                            }
                json_packet = jsonify(json_packet)
                json_packet.headers.add('Access-Control-Allow-Origin', '*')
                #json_response = json.dumps(json_packet)
                return json_packet

        if a['intent'] == "PlotGraph":
                datatable = sorter_main(datatable)
                ##plot begin
                y_var = a['ToFind'][0]
                if len(a['ToFind']) > 1:
                    x_var = a['ToFind'][1]
                else:
                    x_var = a['ToFind'][0]
                
                if len(a['ToFind']) > 1:
                    horizontal_stack = pd.concat([datatable[[x_var]], datatable[[y_var]]], axis=1)
                    horizontal_stack= horizontal_stack.groupby([x_var])[y_var].count()
                else:
                    horizontal_stack = datatable.groupby([x_var])[x_var].count()

                response = "I have plotted number of records of {} with respect to the {} as per your search parameters".format(text_to_speech_aider[y_var],text_to_speech_aider[x_var])
                graph_data = horizontal_stack.to_json(orient='split')#[1:-1].replace('},{', '} {')
                graph_data_f = json.loads(graph_data)
                json_packet = {'response': response,
                               'graph': True,
                               'graph_type': a['plot_type'][0],
                               'graph_x':text_to_speech_aider[x_var],
                               'graph_y':text_to_speech_aider[y_var],
                               'graph_data': graph_data_f,
                               'note':"index is x axis, data is value"
                               }
                return jsonify(json_packet)

        if a['intent'] == "FindValue":
                datatable = sorter_main(datatable)
               
                temp = a['ToFind'][0]

                datatable = datatable[temp]
                datatable= datatable.drop_duplicates()
                i = datatable.count()
                str_val=""
                p=0
                while p < i :
                    str_val = str_val + str(datatable.tolist()[p])
                    p= p+1
                    if p<i :
                        str_val = str_val + ", "

                #return Json area
                reply = "I found following {} to be matching your search requirements: {}".format(text_to_speech_aider[temp],str_val)
                if i == 0:
                    reply = "I couldn't find any {} to be matching your search requirements".format(text_to_speech_aider[temp])
                json_packet = {'response': reply,
                               'graph': False
                            }
                #json_response = json.dumps(json_packet)
                return jsonify(json_packet)



        json_packet = {'response': response.query_result.fulfillment_text,
                               'graph': False
                            }
        json_packet = jsonify(json_packet)
        json_packet.headers.add('Access-Control-Allow-Origin', '*')
        return json_packet
                #json_response = json.dumps(json_packet)



   
api.add_resource(Responder, '/responder') # Route_responder
#api.add_resource(Employees, '/employees') # Route_1
#api.add_resource(Tracks, '/tracks') # Route_2
#api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run()
