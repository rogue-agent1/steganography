import argparse

def text_to_bits(text):
    return "".join(f"{ord(c):08b}" for c in text) + "00000000"

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits)-7, 8):
        byte = int(bits[i:i+8], 2)
        if byte == 0: break
        chars.append(chr(byte))
    return "".join(chars)

def encode_pbm(width, height, pixels, message):
    bits = text_to_bits(message)
    flat = list(pixels)
    for i, b in enumerate(bits):
        if i >= len(flat): break
        flat[i] = (flat[i] & ~1) | int(b)
    return flat

def decode_pbm(pixels, max_chars=1000):
    bits = "".join(str(p & 1) for p in pixels[:max_chars*8])
    return bits_to_text(bits)

def main():
    p = argparse.ArgumentParser(description="LSB steganography")
    sub = p.add_subparsers(dest="cmd")
    e = sub.add_parser("encode")
    e.add_argument("message")
    e.add_argument("-s", "--size", type=int, default=32)
    d = sub.add_parser("decode")
    d.add_argument("data", nargs="+", type=int)
    sub.add_parser("demo")
    args = p.parse_args()
    if args.cmd == "encode":
        import random; random.seed(42)
        pixels = [random.randint(0, 255) for _ in range(args.size * args.size)]
        encoded = encode_pbm(args.size, args.size, pixels, args.message)
        decoded = decode_pbm(encoded)
        print(f"Original sample: {pixels[:16]}")
        print(f"Encoded sample:  {encoded[:16]}")
        print(f"Hidden message:  {decoded}")
        print(f"Capacity: {len(pixels)//8} chars in {args.size}x{args.size} image")
    elif args.cmd == "decode":
        print(decode_pbm(args.data))
    elif args.cmd == "demo":
        import random; random.seed(42)
        pixels = [random.randint(0, 255) for _ in range(256)]
        msg = "Hello, World!"
        encoded = encode_pbm(16, 16, pixels, msg)
        decoded = decode_pbm(encoded)
        changes = sum(1 for a, b in zip(pixels, encoded) if a != b)
        print(f"Message: {msg}")
        print(f"Decoded: {decoded}")
        print(f"Pixels changed: {changes}/{len(pixels)} ({changes/len(pixels)*100:.1f}%)")
    else: p.print_help()

if __name__ == "__main__":
    main()
