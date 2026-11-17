"""Losslessly pack UTF-8 text into a compact ternary radio-inspired signal.

Each UTF-8 byte is represented by six base-3 symbols. The symbols correspond
to the three agreed signal states (-1, 0, +1), mapped to base-3 digits
(0, 1, 2). Five trits are packed into each output byte. This is a digital
encoding for the ROS payload; it does not generate a physical radio waveform.
"""

from __future__ import annotations

from collections.abc import Iterable

TRITS_PER_BYTE = 6
TRITS_PER_PACKED_BYTE = 5
BASE = 3
MAX_PACKED_VALUE = BASE**TRITS_PER_PACKED_BYTE - 1
BYTE_TRIT_DIVISORS = tuple(BASE**i for i in reversed(range(TRITS_PER_BYTE)))
PACKED_TRIT_DIVISORS = tuple(BASE**i for i in reversed(range(TRITS_PER_PACKED_BYTE)))


def encode_text(text: str) -> tuple[bytes, int]:
    """Encode arbitrary Unicode text as packed ternary symbols.

    Returns the packed bytes and exact trit count. Six trits per UTF-8 byte
    make decoding unambiguous without delimiters; the count excludes padding.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    original = text.encode("utf-8")
    packed = bytearray()
    value = used = 0
    for byte in original:
        for divisor in BYTE_TRIT_DIVISORS:
            digit, byte = divmod(byte, divisor)
            value = value * BASE + digit
            used += 1
            if used == TRITS_PER_PACKED_BYTE:
                packed.append(value)
                value = used = 0
    if used:
        packed.append(value * BASE ** (TRITS_PER_PACKED_BYTE - used))
    return bytes(packed), len(original) * TRITS_PER_BYTE


def decode_text(packed_signal: Iterable[int], symbol_count: int) -> str:
    """Decode packed ternary symbols into their original Unicode text."""
    if not isinstance(symbol_count, int) or isinstance(symbol_count, bool):
        raise TypeError("symbol_count must be an integer")
    if symbol_count < 0 or symbol_count % TRITS_PER_BYTE:
        raise ValueError("symbol_count must be a non-negative multiple of six")

    packed = bytes(packed_signal)
    expected_length = (symbol_count + TRITS_PER_PACKED_BYTE - 1) // TRITS_PER_PACKED_BYTE
    if len(packed) != expected_length:
        raise ValueError("packed signal length does not match symbol_count")
    decoded = bytearray()
    remaining = symbol_count
    byte = used = 0
    for value in packed:
        if value > MAX_PACKED_VALUE:
            raise ValueError("packed signal contains an invalid base-3 group")
        for divisor in PACKED_TRIT_DIVISORS:
            digit, value = divmod(value, divisor)
            if not remaining:
                if digit:
                    raise ValueError("packed signal has non-zero trailing padding")
                continue
            remaining -= 1
            byte = byte * BASE + digit
            used += 1
            if used == TRITS_PER_BYTE:
                if byte > 0xFF:
                    raise ValueError("ternary group is outside the UTF-8 byte range")
                decoded.append(byte)
                byte = used = 0

    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("radio signal does not contain valid UTF-8") from error
