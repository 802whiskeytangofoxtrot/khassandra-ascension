"""
Simple encryption helpers for the Khassandra Ascension package.

These helpers implement a naïve XOR‑based stream cipher on top of
base64 encoding.  They are intended for obfuscating small bits of
configuration or model metadata and are *not* secure for production use.

If you require strong cryptography you should replace these functions
with calls into a proper cryptographic library such as `cryptography` or
`PyNaCl`.  For any proprietary or secret data used in the ascension
process, you should implement your own secure logic locally.  You can
use the placeholder comment below as a marker for where such code
belongs.
"""

from __future__ import annotations

import base64
from typing import Union


def simple_encrypt(data: Union[str, bytes], key: Union[str, bytes]) -> bytes:
    """Encrypt bytes using a simple XOR cipher.

    Parameters
    ----------
    data:
        The plaintext to encrypt.  If a string is provided it will be
        encoded using UTF‑​8.
    key:
        A key used for the XOR cipher.  If a string is provided it will
        be encoded using UTF‑​8.  Keys shorter than the data will be
        repeated cyclically.

    Returns
    -------
    bytes
        The encrypted data, base64‑​url encoded.
    """
    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data
    if isinstance(key, str):
        key_bytes = key.encode("utf-8")
    else:
        key_bytes = key
    encrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data_bytes))
    return base64.urlsafe_b64encode(encrypted)


def simple_decrypt(data: Union[str, bytes], key: Union[str, bytes]) -> bytes:
    """Decrypt data encrypted by :func:`simple_encrypt`.

    Parameters
    ----------
    data:
        The base64‑​encoded ciphertext produced by :func:`simple_encrypt`.
        If a string is provided it will be encoded using ASCII prior to
        decoding.
    key:
        The key used during encryption.  If a string is provided it will
        be encoded using UTF‑​8.

    Returns
    -------
    bytes
        The decrypted plaintext.  You may decode it to a string if
        appropriate.
    """
    if isinstance(data, str):
        data_bytes = data.encode("ascii")
    else:
        data_bytes = data
    if isinstance(key, str):
        key_bytes = key.encode("utf-8")
    else:
        key_bytes = key
    encrypted = base64.urlsafe_b64decode(data_bytes)
    decrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(encrypted))
    return decrypted


def encrypt_proprietary_data(data: bytes, key: bytes) -> bytes:
    """
    Encrypt sensitive data using a locally implemented algorithm.

    This function is a placeholder for the proprietary encryption logic
    required by the ascension process.  The implementation of this
    function must remain internal and should not be exported.  When
    building locally, replace the body of this function with your own
    cryptographic scheme appropriate for your threat model.
    """
    # 🔒 BUILD LOCALLY: Proprietary, not to be exported, custom logic must be implemented here
    # The current implementation simply delegates to the naïve XOR cipher
    return simple_encrypt(data, key)


def decrypt_proprietary_data(data: bytes, key: bytes) -> bytes:
    """
    Decrypt sensitive data encrypted by :func:`encrypt_proprietary_data`.

    Similarly to :func:`encrypt_proprietary_data`, this function should
    contain the proprietary decryption logic.  Replace the body of this
    function locally with a secure algorithm of your choosing.
    """
    # 🔒 BUILD LOCALLY: Proprietary, not to be exported, custom logic must be implemented here
    return simple_decrypt(data, key)
