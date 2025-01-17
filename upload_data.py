import requests
import argparse
import os
import json
from datetime import datetime

url = "https://us-central1-cleancurrentscoalition.cloudfunctions.net/upload-images"


def upload_data(trash_wheel_id, image_file_path, data, timestamp):
    files = {
        "trash_wheel_id": (None, str(trash_wheel_id)),
        "contents_data": (None, data),
        "image_file": open(image_file_path, "rb"),
        "timestamp": (None, datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').isoformat())
    }
    
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Images uploaded successfully.")
    else:
        print(f"Error uploading images. Status code: {response.status_code}")
        print(response.text)

parser = argparse.ArgumentParser(description='Upload trash wheel image, bounding box data, and trash collected data to the server')
parser.add_argument('--trash_wheel_id', type=int, help='unique id of trash wheel')
parser.add_argument('--image_file_path', type=str, help='directory path to image of trash on the trash wheel')
parser.add_argument('--data', type=str, default='{}', help='collected trash data')
parser.add_argument('--timestamp', type=str, help='timestamp of image capture')

if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.exists(args.image_file_path):
        print("Image needs to be present")
    else:
        json_data = json.dumps(json.loads(args.data))
        print(datetime.strptime(args.timestamp, '%Y-%m-%d %H:%M:%S').isoformat())
        upload_data(trash_wheel_id=args.trash_wheel_id, image_file_path=args.image_file_path, data=json_data, timestamp=args.timestamp)