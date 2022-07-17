import format_pretty as fp
import os
from googleapiclient.discovery import build

api_key = os.environ.get('api_key')
youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
    part='contentDetails',
    forUsername='ASMRMagic'
)

response = request.execute()
s = repr(response)
fp.format_pretty(s)
