"""User journey logging middleware"""

import base64
import json
import logging
import time
from collections import defaultdict

from fastapi import Request

logger = logging.getLogger(__name__)

# Cache for storing client tokens by IP to consistently identify users
client_token_cache = defaultdict(lambda: {"token": None, "timestamp": 0})


async def user_journey_logger(request: Request, call_next):
    """Log user journey with properly identified user"""
    # Only log API requests
    if not request.url.path.startswith("/api/"):
        return await call_next(request)

    # Skip logging for certain endpoints (like health checks)
    if request.url.path == "/api/health":
        return await call_next(request)

    # Get client IP for token caching
    client_ip = request.client.host if request.client else "unknown"

    # Process the request
    response = await call_next(request)

    # Extract user ID from Authorization header
    user_id = "anonymous"
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix

        # Store token in cache by client IP for future requests
        client_token_cache[client_ip] = {"token": token, "timestamp": time.time()}

        try:
            # Extract payload from JWT without verification
            # Format is typically header.payload.signature
            parts = token.split(".")
            if len(parts) == 3:
                # Fix padding for base64 decoding
                payload = parts[1]
                payload += "=" * ((4 - len(payload) % 4) % 4)

                # Decode payload
                decoded_payload = base64.urlsafe_b64decode(payload)
                payload_data = json.loads(decoded_payload)

                # Extract user email as ID
                if "sub" in payload_data:
                    user_id = payload_data["sub"]
        except Exception as e:
            # Log the error for debugging but fall back to anonymous
            logger.debug(f"Failed to parse JWT token: {e}")
            pass
    else:
        # Try to get user ID from cached token (for consistent tracking across requests)
        cached_data = client_token_cache[client_ip]
        if (
            cached_data["token"] and time.time() - cached_data["timestamp"] < 3600
        ):  # 1 hour TTL
            token = cached_data["token"]
            try:
                # Extract payload from JWT without verification
                parts = token.split(".")
                if len(parts) == 3:
                    payload = parts[1]
                    payload += "=" * ((4 - len(payload) % 4) % 4)

                    decoded_payload = base64.urlsafe_b64decode(payload)
                    payload_data = json.loads(decoded_payload)

                    if "sub" in payload_data:
                        user_id = payload_data["sub"]
            except Exception as e:
                logger.debug(f"Failed to parse cached JWT token: {e}")
                pass

    # Log only the user ID
    print(f"USER: user_id={user_id}")

    return response
