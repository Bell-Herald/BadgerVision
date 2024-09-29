import requests
from typing import Optional, Dict, Any


class PinataError(Exception):
    pass


class NetworkError(PinataError):
    pass


class AuthenticationError(PinataError):
    pass


class ValidationError(PinataError):
    pass


def upload_file(
    config: Optional[Dict[str, Any]],
    file_path: str,
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not config or "pinataJwt" not in config:
        raise ValidationError("Pinata configuration is missing")

    jwt = (
        options.get("keys")
        if options and "keys" in options
        else config.get("pinataJwt")
    )

    with open(file_path, "rb") as file:
        files = {
            "file": (file_path, file),
        }

        data = {
            "name": (
                options.get("metadata", {}).get("name", file_path)
                if options
                else file_path
            )
        }

        if options and "groupId" in options:
            data["group_id"] = options["groupId"]

        headers = {
            "Authorization": f"Bearer {jwt}",
            "Source": "sdk/file",
        }

        if "customHeaders" in config:
            headers.update(config["customHeaders"])

        endpoint = config.get("uploadUrl", "https://uploads.pinata.cloud/v3/files")

        try:
            response = requests.post(endpoint, headers=headers, files=files, data=data)

            if response.status_code in [401, 403]:
                raise AuthenticationError(f"Authentication failed: {response.text}")

            if not response.ok:
                raise NetworkError(f"HTTP error: {response.text}")

            return response.json()

        except requests.RequestException as e:
            raise NetworkError(f"Network error occurred: {str(e)}") from e

        except Exception as e:
            raise PinataError(f"An error occurred: {str(e)}") from e