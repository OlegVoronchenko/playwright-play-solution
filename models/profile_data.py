# models/profile_data.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileData:
    name: str