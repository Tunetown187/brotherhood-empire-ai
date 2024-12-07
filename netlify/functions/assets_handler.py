import json
import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError
import hashlib
from datetime import datetime, timedelta

class SecureAssetsHandler:
    def __init__(self):
        self.s3_client = boto3.client('s3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        self.bucket_name = os.environ.get('S3_BUCKET_NAME')
        self.make_api_key = os.environ.get('MAKE_API_KEY', '726acbb9-1b9f-4c78-a72f-e3ca0e0129c4')

    def generate_secure_filename(self, original_name: str) -> str:
        """Generate a secure filename with timestamp and hash"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name_hash = hashlib.sha256(original_name.encode()).hexdigest()[:12]
        extension = os.path.splitext(original_name)[1]
        return f"{timestamp}_{name_hash}{extension}"

    def upload_file(self, file_path: str, content_type: str = None) -> Dict[str, Any]:
        """Upload file to S3 with security headers"""
        try:
            secure_filename = self.generate_secure_filename(os.path.basename(file_path))
            
            # Set security headers
            extra_args = {
                'ContentType': content_type or 'application/octet-stream',
                'Metadata': {
                    'x-amz-meta-encryption': 'AES256',
                    'x-amz-meta-uploaded-by': 'brotherhood-empire',
                    'x-amz-meta-timestamp': datetime.now().isoformat()
                },
                'ServerSideEncryption': 'AES256'
            }

            # Upload to S3
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                f"secure-assets/{secure_filename}",
                ExtraArgs=extra_args
            )

            # Generate secure temporary URL
            url = self.generate_presigned_url(f"secure-assets/{secure_filename}")

            return {
                'status': 'success',
                'secure_url': url,
                'filename': secure_filename,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """Generate a secure presigned URL for accessing the file"""
        try:
            url = self.s3_client.generate_presigned_url('get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration,
                HttpMethod='GET'
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None

    def list_secure_assets(self) -> Dict[str, Any]:
        """List all secure assets with their metadata"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='secure-assets/'
            )

            assets = []
            for obj in response.get('Contents', []):
                metadata = self.s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=obj['Key']
                )
                
                assets.append({
                    'filename': os.path.basename(obj['Key']),
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'metadata': metadata.get('Metadata', {})
                })

            return {
                'status': 'success',
                'assets': assets,
                'total_count': len(assets),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Initialize handler
assets_handler = SecureAssetsHandler()
