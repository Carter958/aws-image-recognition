import boto3
from PIL import Image, ImageDraw, ImageFont

# Configure the AWS client with region
s3_client = boto3.client('s3', region_name='us-east-1')
rekognition_client = boto3.client('rekognition', region_name='us-east-1')

def upload_to_s3(file_name, bucket_name):
    try:
        s3_client.upload_file(file_name, bucket_name, file_name)
        print(f"Uploaded {file_name} to {bucket_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def detect_labels(bucket_name, file_name):
    try:
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_name,
                }
            },
            MaxLabels=10
        )
        return response['Labels']
    except Exception as e:
        print(f"Error detecting labels: {e}")
        return []

def show_labels(image_path, labels):
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 24)  # Use a larger font size
        for label in labels:
            if 'Instances' in label:
                for instance in label['Instances']:
                    box = instance['BoundingBox']
                    left = image.width * box['Left']
                    top = image.height * box['Top']
                    width = image.width * box['Width']
                    height = image.height * box['Height']
                    draw.rectangle(
                        [left, top, left + width, top + height],
                        outline='red',
                        width=3  # Thicker line for bounding box
                    )
                    draw.text((left, top), label['Name'], fill='red', font=font)
        image.show()
    except Exception as e:
        print(f"Error displaying image: {e}")

if __name__ == "__main__":
    bucket_name = 'my-image-recognition-bucket-123'
    file_name = 'image1.jpg'  # Ensure this matches your actual file name

    # Step 1: Upload the image to S3
    upload_to_s3(file_name, bucket_name)

    # Step 2: Detect labels in the image
    labels = detect_labels(bucket_name, file_name)
    for label in labels:
        print(f"Label: {label['Name']}, Confidence: {label['Confidence']}")

    # Step 3: Display the image with labels
    show_labels(file_name, labels)
