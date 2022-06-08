import struct

def bytes_from_audio(data):
    return data.ravel().view('b').tobytes()

def generate_header(data, sample_rate):
    datasize = 2000*10**6
    channels = data.shape[1]
    fs = sample_rate
    header_data = b''
    header_data += b'RIFF'
    header_data += struct.pack('<I', datasize + 36)
    header_data += b'WAVE'
    header_data += b'fmt '
    bit_depth = data.dtype.itemsize * 8
    format_tag = 0x0001
    # format_tag = 0x0003 # IEEE Float – see https://github.com/scipy/scipy/blob/main/scipy/io/wavfile.py
    bytes_per_second = fs * (bit_depth // 8)*channels
    block_align = channels * (bit_depth // 8)
    fmt_chunk_data = struct.pack('<HHIIHH', format_tag, channels, fs,
                                     bytes_per_second, block_align, bit_depth)
    fmt_chunk_data += b'\x00\x00'
    header_data += struct.pack('<I', len(fmt_chunk_data))
    header_data += fmt_chunk_data
    header_data += b'fact'
    header_data += struct.pack('<II', 4, data.shape[0])
    header_data += b'data'
    header_data += struct.pack('<I', datasize)
    return header_data