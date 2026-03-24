"""Service-layer integration for uploading files to DigitalOcean Spaces."""

import uuid
from pathlib import PurePosixPath

import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def _get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.DO_SPACES_REGION,
        endpoint_url=settings.DO_SPACES_ENDPOINT,
        aws_access_key_id=settings.DO_SPACES_KEY,
        aws_secret_access_key=settings.DO_SPACES_SECRET,
    )


def upload_file_to_spaces(file_obj, folder="uploads"):
    """Upload an InMemoryUploadedFile to DigitalOcean Spaces.

    Returns the public URL of the uploaded object on success,
    or raises an exception on failure.
    """
    ext = PurePosixPath(file_obj.name).suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    key = f"{folder}/{unique_name}"

    client = _get_s3_client()
    client.upload_fileobj(
        file_obj,
        settings.DO_SPACES_BUCKET,
        key,
        ExtraArgs={
            "ContentType": file_obj.content_type or "application/octet-stream",
            "ACL": "public-read",
        },
    )

    url = f"{settings.DO_SPACES_ENDPOINT}/{settings.DO_SPACES_BUCKET}/{key}"
    return url
