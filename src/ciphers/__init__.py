"""Reusable cipher helpers shared by chapters and the future game loop."""

from .frequency import (
    frequency_percentages,
    frequency_profile,
    letter_frequency,
    most_frequent_symbol,
    ranked_letters,
)
from .grid import (
    combine_grid_blocks,
    extract_grid_symbols,
    extract_grid_text,
    normalize_grid_rows,
    trace_grid_extraction,
)
from .hill import (
    DEFAULT_HILL_ALPHABET,
    DEFAULT_PAD_CHAR,
    block_mapping_trace,
    decode_hill,
    derive_key_from_digraph_pairs,
    encode_hill,
    hill_blocks,
    matrix_inverse_2x2,
    modular_inverse,
)
from .indexing import extract_symbols, extract_text, trace_extraction
from .morse import decode_morse, encode_morse
from .substitution import (
    apply_substitution,
    decode_substitution,
    invert_substitution,
    is_complete_substitution,
    rotation_mapping,
)

__all__ = [
    "apply_substitution",
    "combine_grid_blocks",
    "block_mapping_trace",
    "decode_morse",
    "decode_substitution",
    "decode_hill",
    "DEFAULT_HILL_ALPHABET",
    "DEFAULT_PAD_CHAR",
    "derive_key_from_digraph_pairs",
    "encode_morse",
    "encode_hill",
    "extract_grid_symbols",
    "extract_grid_text",
    "extract_symbols",
    "extract_text",
    "frequency_percentages",
    "frequency_profile",
    "hill_blocks",
    "invert_substitution",
    "is_complete_substitution",
    "letter_frequency",
    "most_frequent_symbol",
    "matrix_inverse_2x2",
    "modular_inverse",
    "normalize_grid_rows",
    "ranked_letters",
    "rotation_mapping",
    "trace_grid_extraction",
    "trace_extraction",
]
