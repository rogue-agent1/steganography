#!/usr/bin/env python3
"""steganography - LSB steganography in PPM images."""
import argparse, sys

def read_ppm(path):
    with open(path,"rb") as f:
        assert f.readline().strip() == b"P6"
        line = f.readline()
        while line.startswith(b"#"): line = f.readline()
        w, h = map(int, line.split())
        maxval = int(f.readline().strip())
        data = bytearray(f.read())
    return w, h, data

def write_ppm(path, w, h, data):
    with open(path,"wb") as f:
        f.write(f"P6\n{w} {h}\n255\n".encode())
        f.write(bytes(data))

def encode(img_path, message, output):
    w, h, data = read_ppm(img_path)
    msg_bits = []
    msg_bytes = message.encode() + b"\x00"
    for byte in msg_bytes:
        for bit in range(8):
            msg_bits.append((byte >> (7-bit)) & 1)
    if len(msg_bits) > len(data):
        print(f"Message too large ({len(msg_bits)} bits > {len(data)} pixels)"); return
    for i, bit in enumerate(msg_bits):
        data[i] = (data[i] & 0xFE) | bit
    write_ppm(output, w, h, data)
    print(f"Encoded {len(message)} chars into {output}")

def decode(img_path):
    _, _, data = read_ppm(img_path)
    chars = []; byte = 0
    for i, pixel in enumerate(data):
        byte = (byte << 1) | (pixel & 1)
        if (i + 1) % 8 == 0:
            if byte == 0: break
            chars.append(chr(byte)); byte = 0
    return "".join(chars)

def make_test_ppm(path, w=100, h=100):
    data = bytearray()
    for y in range(h):
        for x in range(w):
            data.extend([int(x*255/w), int(y*255/h), 128])
    write_ppm(path, w, h, data)
    print(f"Created test image: {path}")

def main():
    p = argparse.ArgumentParser(description="LSB steganography")
    sub = p.add_subparsers(dest="cmd")
    e = sub.add_parser("encode"); e.add_argument("image"); e.add_argument("message"); e.add_argument("-o","--output",default="stego.ppm")
    d = sub.add_parser("decode"); d.add_argument("image")
    t = sub.add_parser("testimg"); t.add_argument("-o","--output",default="test.ppm")
    a = p.parse_args()
    if a.cmd == "encode": encode(a.image, a.message, a.output)
    elif a.cmd == "decode": print(f"Hidden message: {decode(a.image)}")
    elif a.cmd == "testimg": make_test_ppm(a.output)
    else: p.print_help()

if __name__ == "__main__": main()
