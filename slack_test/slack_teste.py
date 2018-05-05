import os
from slackclient import SlackClient

slack_token = 'xoxp-178369105184-359126781829-359002639970-a74e124f72b5a7949c5ae62386f28c67'
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="GAJS5RH6X",
  text="Hello from Python! :tada:"
)