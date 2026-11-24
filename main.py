#!/usr/bin/env python3
"""news-23 b97 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    real_out = os.path.realpath(out_dir_abs)
    real_here = os.path.realpath(here)
    if real_out == real_here or real_out.startswith(real_here + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(real_out) and not os.path.isdir(real_out):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if not os.path.isfile(src):
        fail("source entry.png not found next to main.py")

    with open(src, "rb") as f:
        data = f.read()

    if len(data) < MIN_BYTES:
        fail("entry.png too small (%d bytes)" % len(data))
    if len(data) > MAX_BYTES:
        fail("entry.png exceeds 1 MiB (%d bytes)" % len(data))

    # Validate PNG header manually (stdlib struct, no PIL).
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("first chunk is not IHDR")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    if ihdr_len != 13:
        fail("IHDR length is not 13")
    width, height, bit_depth, colour_type, comp, filt, interlace = struct.unpack(
        ">IIBBBBB", data[16:29]
    )
    if (width, height) != (1024, 1024):
        fail("expected 1024x1024, got %dx%d" % (width, height))
    if bit_depth != 8 or colour_type not in (2, 6):
        fail("expected 8-bit RGB/RGBA, got depth %d type %d" % (bit_depth, colour_type))
    if comp != 0 or filt != 0 or interlace != 0:
        fail("unexpected compression/filter/interlace in IHDR")
    # Walk the chunks: verify CRCs, require non-empty IDAT payload, IEND last.
    pos = 8
    idat_total = 0
    last_type = None
    while pos + 8 <= len(data):
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            fail("truncated chunk %r" % ctype)
        stored_crc = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        calc_crc = zlib.crc32(ctype + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF
        if stored_crc != calc_crc:
            fail("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        last_type = ctype
        pos += 12 + clen
        if ctype == b"IEND":
            break
    if last_type != b"IEND":
        fail("last chunk is not IEND")
    if pos != len(data):
        fail("trailing data after IEND")
    if idat_total < 1000:
        fail("IDAT payload too small (%d bytes)" % idat_total)

    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.realpath(dst) == os.path.realpath(src):
        fail("output would overwrite the source entry.png")
    with open(dst, "wb") as f:
        f.write(data)

    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output does not match source byte-for-byte")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
