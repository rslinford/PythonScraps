import os
from googleapiclient.discovery import build

api_key = os.environ.get('api_key')

video_id = 'oMfOpfUPX_8'
# video_id = '5cxtS8Rc28k'

resource = build('youtube', 'v3', developerKey=api_key)
pageToken = ''
while pageToken != None:
    # create a request to get 20 comments on the video
    response = resource.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=20,
        order="orderUnspecified",
        pageToken=pageToken).execute()

    items = response["items"]

    print(f"-------  Items returned {len(items)} --------------------------------")
    for item in items:
        item_info = item["snippet"]

        # the top level comment can have sub reply comments
        topLevelComment = item_info["topLevelComment"]
        comment_info = topLevelComment["snippet"]

        print("Comment By:", comment_info["authorDisplayName"])
        print("Comment Text:", comment_info["textDisplay"])
        print("Likes on Comment :", comment_info["likeCount"])
        print("Comment Date: ", comment_info['publishedAt'])
        print("================================\n")
    if "nextPageToken" in response:
        pageToken = response['nextPageToken']
    else:
        pageToken = None
