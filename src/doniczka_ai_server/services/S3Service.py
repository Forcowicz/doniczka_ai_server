import os
from typing import Optional
import boto3


class S3Service:
    _instance = None

    def __init__(self, bucket: str) -> None:
        self._client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        self.bucket = bucket

    @classmethod
    def initialize(cls, bucket: str) -> None:
        if cls._instance is not None:
            return

        cls._instance = cls(bucket)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("S3Service is not initialized")
        return cls._instance

    def upload_file(self, file_name: str, object_name: Optional[str] = None):
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        try:
            self._client.upload_file(file_name, self.bucket, object_name)
        except Exception as e:
            return False
        return True

    def upload_fileobj(self, file_obj, object_name: str) -> bool:
        try:
            self._client.upload_fileobj(file_obj, self.bucket, object_name)
        except Exception as e:
            return False
        return True

    def get_url(self, object_name: str, expiration: int = 3600) -> Optional[str]:
        try:
            return self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": object_name},
                ExpiresIn=expiration,
            )
        except Exception as e:
            return None
