#
# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from watson_developer_cloud import ConversationV1
import json
from pprint import pprint


class ChatBot:
    line_access_tocken = '0M2cbdPz9vSaMXJOKQV1ABdgDpwgMgjSxpJZL3/2PpyE2hX2oCD6RMZxCdqR0xb91pooVHpW7DSJFhJxK8LoZMSszBug3MowpABnWNQv/P19BIlp02mJWl37+un2835g5lvPM7pj7DXk1PTqEQMUFgdB04t89/1O/w1cDnyilFU='
    line_channel_secret = '5b56ff2ce2593c22c161a6501499f921'
    watson_username = 'a7ccea03-a340-4bff-8cb0-6cfe2851afae'
    watson_password = 'FKHURt5KJPaC'
    convesation_workspace_id = 'a08d1faf-8266-4117-92ba-f9c964eeed7c'
    msg_receive = ''
    msg_reply = ''

app = Flask(__name__)
line_bot_api = LineBotApi(ChatBot.line_access_tocken)
handler = WebhookHandler(ChatBot.line_channel_secret)

conversation_client = ConversationV1(
    username=ChatBot.watson_username,
    password=ChatBot.watson_password,
    version='2017-04-21')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ChatBot.msg_receive = event.message.text

    json_reply = conversation_client.message(
    workspace_id = ChatBot.convesation_workspace_id, 
    message_input = {'text':ChatBot.msg_receive})
    ChatBot.msg_reply = json_reply['output']['text'][0] 

    print(ChatBot.msg_receive)
    print(ChatBot.msg_reply)
    print(json.dumps(ChatBot.msg_reply, indent=2))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(ChatBot.msg_reply))


if __name__ == "__main__":
    app.run()
    


#Receive Json code from Line
    # {"events":[{
    #     "type":"message",
    #     "replyToken":"cc79dbed39df40019ed54511be8d77f6",
    #     "source":{
    #         "userId":"Ue22ff760aa6cde4390c6d5567d5aa5f5",
    #         "type":"user"
    #         },
    #     "timestamp":1496211335206,
    #     "message":{
    #         "type":"text",
    #         "id":"6167354628626",
    #         "text":"跑"
    #         }
    #     }]
    # }

#Receive Jason code from Line
    # {   
    #     'input': {'text': 'Hello'}, 
    #     'intents': [], 
    #     'context': 
    #     {
    #         'conversation_id': '4d173d82-a606-4b07-b6aa-3d5f92be54aa', 
    #         'system': 
    #         {
    #             'dialog_turn_counter': 1, 
    #                 'dialog_request_counter': 1, 
    #                 '_node_output_map': {'其他事情': [0]}, 
    #                 'dialog_stack': [{'dialog_node': 'root'}], 
    #                 'branch_exited_reason': 'completed', 
    #                 'branch_exited': True
    #                     }
    #             }, 
    #     'entities': [], 
    #     'output': {
    #         'log_messages': [], 
    #         'nodes_visited': ['其他事情'], 
    #         'text': ['我不瞭解您的問題。您可以換種方式說明']
    #         }
    # }
