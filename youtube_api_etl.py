import os
import json
import boto3
from googleapiclient.discovery import build
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

search_query = "stargate"  # Replace with your search query

def main():
    global search_query
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv('youtube_api_key')  # Fetch API key from .env

    if not DEVELOPER_KEY:
        raise ValueError("YOUTUBE_API_KEY is not set in the .env file.")

    # Create the YouTube API client using the API key
    youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Step 1: Search for a video by title

    search_response = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",  # Ensures only video results are returned
        maxResults=1  # Limit to one video for simplicity
    ).execute()

    # Extract the video ID from the search response
    if not search_response['items']:
        print(f"No results found for query: {search_query}")
        return

    video_id = search_response['items'][0]['id']['videoId']
    print(f"Found video ID: {video_id} for query: {search_query}")

    # Step 2: Fetch comments for the video
    request = youtube.commentThreads().list(
        part="snippet,replies",  # Removed contentDetails, only snippet and replies
        videoId=video_id,
        maxResults=100,  # Increase results limit if needed (max 100 per request)
        textFormat="plainText"  # You can use "plainText" or "html" format for text
    )
    response = request.execute()

    # Load existing raw data from S3
    s3_bucket = os.getenv('s3_bucket_name')
    raw_filename = 'youtube_raw_data.json'
    transformed_filename = 'youtube_transformed_data.json'
    s3 = boto3.client('s3')

    try:
        existing_raw_data = s3.get_object(Bucket=s3_bucket, Key=raw_filename)
        raw_json = json.loads(existing_raw_data['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        raw_json = []

    # Append new raw data
    raw_json.extend(response.get('items', []))

    # Upload the updated raw data back to S3
    s3.put_object(Bucket=s3_bucket, Key=raw_filename, Body=json.dumps(raw_json))

    # Transformation: Extract specific fields
    transformed_data = []
    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']
        transformed_data.append({
            'author': comment['authorDisplayName'],
            'text': comment['textDisplay'],
            'videoId': comment['videoId']
        })

    # Load existing transformed data from S3
    try:
        existing_transformed_data = s3.get_object(Bucket=s3_bucket, Key=transformed_filename)
        transformed_json = json.loads(existing_transformed_data['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        transformed_json = []

    # Append new transformed data
    transformed_json.extend(transformed_data)

    # Upload the updated transformed data back to S3
    s3.put_object(Bucket=s3_bucket, Key=transformed_filename, Body=json.dumps(transformed_json))

    print(f"Raw data appended and saved to S3 bucket {s3_bucket} with filename {raw_filename}")
    print(f"Transformed data appended and saved to S3 bucket {s3_bucket} with filename {transformed_filename}")


if __name__ == "__main__":
    main()
