import json
import boto3
from datetime import datetime
from io import StringIO
import csv

def transform_tracks_data(data):
    track_list = []
    
    # Check for the 'tracks' key in the data
    if 'tracks' not in data:
        raise ValueError("The key 'tracks' is missing from the data.")
    
    for item in data['tracks']:
        # Initialize a track dictionary
        track_dict = {
            'track_id': item['id'],
            'track_name': item['name'],
            'track_url': item['external_urls']['spotify'],
            'track_popularity': item.get('popularity', None),  # Use .get() to avoid KeyError
            'album_id': item['album']['id'] if 'album' in item else None,
            'album_name': item['album']['name'] if 'album' in item else None,
            'release_date': item['album']['release_date'] if 'album' in item else None,
            'artist_ids': ', '.join(artist['id'] for artist in item['artists']),  # Join multiple artist IDs
            'artist_names': ', '.join(artist['name'] for artist in item['artists']),  # Join multiple artist names
        }
        
        # Transformation: Replace '2012' with '2012-01-01' in release_date
        if track_dict['release_date'] == '2012':
            track_dict['release_date'] = '2012-01-01'
        
        track_list.append(track_dict)
    
    return track_list

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Define the S3 bucket and key prefixes
    bucket = "spotify-data-scrapping"
    key_prefix = "raw-data/to_process/"
    transformed_key_prefix = "transformed-data/tracks_data/"
    processed_key_prefix = "raw-data/processed/"  # New processed folder
    
    # List objects in the S3 bucket
    response = s3.list_objects(Bucket=bucket, Prefix=key_prefix)
    
    if 'Contents' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps('No objects found in the specified bucket and prefix.')
        }
    
    for file in response['Contents']:
        file_key = file['Key']
        if file_key.endswith(".json"):
            response = s3.get_object(Bucket=bucket, Key=file_key)
            content = response['Body'].read().decode('utf-8')
            jsonObject = json.loads(content)
            
            # Log the JSON object for debugging
            print(jsonObject)  # Debugging line
            
            # Transform the data
            try:
                transformed_data = transform_tracks_data(jsonObject)
                if not transformed_data:
                    print("Warning: No data transformed from the input.")
                    continue  # Skip to the next file if no data is transformed
            except ValueError as e:
                print(f"Error transforming data: {e}")
                continue  # Skip this file and continue with the next
            
            # Create CSV content
            csv_buffer = StringIO()
            csv_writer = csv.DictWriter(csv_buffer, fieldnames=transformed_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(transformed_data)
            csv_content = csv_buffer.getvalue()
            
            # Define the output key for the transformed data
            output_key = f"{transformed_key_prefix}tracks_transformed_{datetime.now().isoformat()}.csv"
            print(f"Uploading to S3: {output_key}")  # Log the output key
            s3.put_object(Bucket=bucket, Key=output_key, Body=csv_content)
            
            # Copy the original JSON file to the processed folder
            processed_file_key = f"{processed_key_prefix}{file_key.split('/')[-1]}"  # Keep the original filename
            print(f"Copying original file to processed folder: {processed_file_key}")  # Log the copy action
            s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': key_prefix}, Key=processed_file_key)
            
            # Delete the original JSON file from the to_process folder
            print(f"Deleting original file: {file_key}")  # Log the deletion
            s3.delete_object(Bucket=bucket, Key=file_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data transformed, uploaded, original files copied and deleted successfully!')
    }