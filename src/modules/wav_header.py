"""
Wav header parsing module
"""

import struct

from modules.printer import Levels as log_levels
from modules.printer import log


class WavHeader:
    """WAV header structure"""
    def __init__(self):
        self.riff = None
        self.wave = None
        self.fmt = None
        self.pcm = None
        self.channels = None
        self.sample_rate = None
        self.bits = None
        
        self.is_valid = False
        
def get_header_from_filename(filename: str) -> WavHeader:
    """
    Get WAV header from file
    
    Args:
        filename (str): Path to WAV file
        
    Returns:
        WavHeader: Parsed WAV header
    """
    
    header = WavHeader()
    try:
        with open(filename, "rb") as f:
            # Read RIFF header
            header.riff = f.read(4).decode()
            # Read WAVE header
            f.seek(4)
            header.wave = f.read(4).decode()
            # Read fmt chunk
            header.fmt = f.read(4).decode()
            
            # Read PCM format, channels, sample rate
            f.seek(4)
            header.pcm = struct.unpack("<H", f.read(2))[0]
            header.channels = struct.unpack("<H", f.read(2))[0]
            header.sample_rate = struct.unpack("<I", f.read(4))[0]
            
            # Read bits per sample
            f.seek(6)
            header.bits = struct.unpack("<H", f.read(2))[0]
            
        # Validate header
        if header.riff == "RIFF" \
        and header.wave == "WAVE" \
        and header.fmt == "fmt ":
            header.is_valid = True
    except Exception as e:
        log(f"Error reading WAV header: {e}", log_levels.WARNING)
        return header
    return header