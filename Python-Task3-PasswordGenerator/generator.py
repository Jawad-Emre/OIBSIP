"""
Password Generator Engine — Oasis Infobyte SIP Task 3 (Advanced Tier)
Author: Jawad Ahmad

Features:
- Cryptographically secure generation using the `secrets` module (SystemRandom)
- Length validation (minimum 8 characters)
- Complexity options: Uppercase, Lowercase, Digits, Symbols
- Strict security rule: Guaranteed inclusion of at least 1 character from each selected set
- Optional exclusion of ambiguous characters (0, O, l, 1, I)
- Dynamic password strength evaluation using Information Entropy (NIST Standard)
- In-memory session history tracking (last 5 passwords, not persisted to disk)
"""

import string
import secrets
import math
from collections import deque
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Standard character sets
UPPERCASE_CHARS = string.ascii_uppercase
LOWERCASE_CHARS = string.ascii_lowercase
DIGIT_CHARS = string.digits
SYMBOL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

# Ambiguous characters often confused in display/print
AMBIGUOUS_CHARS = set("0Ol1I")

class SessionHistory:
    """Stores the last 5 generated passwords in-memory only."""
    def __init__(self, maxlen: int = 5):
        self._history = deque(maxlen=maxlen)

    def add(self, password: str, length: int, strength: str) -> None:
        entry = {
            "password": password,
            "length": length,
            "strength": strength,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self._history.appendleft(entry)

    def get_all(self) -> List[Dict]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()

# Global session history instance for the current application run
session_history = SessionHistory(maxlen=5)

def evaluate_strength(password: str) -> Tuple[str, int, str]:
    """
    Evaluates password strength dynamically using Information Entropy (bits):
    Entropy = Length * log2(Pool Size)
    
    Scales smoothly from 25% (Weak) up to 100% (Very Strong) as length and
    character diversity increase, so the strength meter changes dynamically!
    
    Returns: (category, score_percentage, hex_color)
    """
    length = len(password)
    if length == 0:
        return "Weak", 0, "#EF4444"

    # Calculate active character pool size
    pool_size = 0
    if any(c in UPPERCASE_CHARS for c in password):
        pool_size += 26
    if any(c in LOWERCASE_CHARS for c in password):
        pool_size += 26
    if any(c in DIGIT_CHARS for c in password):
        pool_size += 10
    if any(c in SYMBOL_CHARS for c in password):
        pool_size += len(SYMBOL_CHARS)

    if pool_size == 0:
        pool_size = 1

    # Information entropy in bits
    entropy_bits = length * math.log2(pool_size)

    # Scale entropy to a 0 - 100% score (128 bits is industry standard maximum):
    # < 45%  -> Weak (e.g. length 8 with 2 types ~ 30-40%)
    # 45-69% -> Medium (e.g. length 10-12 with 3 types ~ 45-65%)
    # 70-85% -> Strong (e.g. length 14-16 with 4 types ~ 70-85%)
    # > 85%  -> Very Strong (e.g. length 18+ with 4 types ~ 90-100%)
    score = int((entropy_bits / 128.0) * 100)
    score = max(20, min(score, 100))  # Clamp between 20% and 100%

    # Classification & Color Cues
    if score >= 85:
        return "Very Strong", score, "#10B981"  # Emerald
    elif score >= 70:
        return "Strong", score, "#22C55E"       # Green
    elif score >= 45:
        return "Medium", score, "#F59E0B"       # Amber / Orange
    else:
        return "Weak", score, "#EF4444"         # Red

def generate_password(
    length: int = 12,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False
) -> Tuple[str, str, int, str]:
    """
    Generates a cryptographically secure random password.
    
    Returns:
        (password, strength_label, strength_score, color_hex)
    
    Raises:
        ValueError: If length < 8 or fewer than 2 character sets are selected.
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    pools = []
    
    if include_upper:
        chars = UPPERCASE_CHARS
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(("uppercase", chars))

    if include_lower:
        chars = LOWERCASE_CHARS
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(("lowercase", chars))

    if include_digits:
        chars = DIGIT_CHARS
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(("digits", chars))

    if include_symbols:
        chars = SYMBOL_CHARS
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pools.append(("symbols", chars))

    if len(pools) < 2:
        raise ValueError("Please select at least 2 character types (Uppercase, Lowercase, Numbers, or Symbols).")

    # Combine all allowed characters
    combined_pool = "".join(pool_chars for _, pool_chars in pools)
    if not combined_pool:
        raise ValueError("Selected character pool is empty after exclusions.")

    rng = secrets.SystemRandom()

    # Rule: Guarantee at least 1 character from each selected character type
    password_chars = []
    for _, pool_chars in pools:
        password_chars.append(rng.choice(pool_chars))

    # Fill the remaining length from the combined pool
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(rng.choice(combined_pool))

    # Cryptographically secure shuffle to prevent predictable positions
    rng.shuffle(password_chars)
    password = "".join(password_chars)

    # Evaluate dynamic strength
    strength_label, strength_score, color_hex = evaluate_strength(password)

    # Record in session history
    session_history.add(password, length, strength_label)

    return password, strength_label, strength_score, color_hex
