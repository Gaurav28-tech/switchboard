import hashlib

class HashBucket:
    @staticmethod
    def calculate_bucket(flag_key: str, user_id: str) -> int:
        salt_key = f"{flag_key}:{user_id}".encode("utf-8")
        digest = hashlib.sha256(salt_key).hexdigest()
        # Take first 8 hex characters as int and mod 100
        val = int(digest[:8], 16)
        return val % 100
