"""API views for resource upload, listing, and delete operations."""

from botocore.exceptions import ClientError
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .services import upload_file_to_spaces


@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_file(request):
    """Accept a file via multipart POST and upload it to DigitalOcean Spaces."""
    file_obj = request.FILES.get("file")
    if not file_obj:
        return Response(
            {"error": "No file provided. Include a 'file' field in the request."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        url = upload_file_to_spaces(file_obj)
    except ClientError as exc:
        return Response(
            {"error": f"Upload failed: {exc}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response({"url": url}, status=status.HTTP_201_CREATED)
