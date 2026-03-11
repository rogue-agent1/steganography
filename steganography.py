#!/usr/bin/env python3
"""Hide messages in text using zero-width characters."""
import sys
ZWC=['\u200b','\u200c','\u200d','\u2060']  # zero-width chars for 00,01,10,11
def encode(msg,cover):
    bits=''.join(f'{b:08b}' for b in msg.encode())
    encoded=''
    for i in range(0,len(bits),2): encoded+=ZWC[int(bits[i:i+2],2)]
    return cover[:len(cover)//2]+encoded+cover[len(cover)//2:]
def decode(text):
    bits=''
    for c in text:
        if c in ZWC: bits+=f'{ZWC.index(c):02b}'
    return bytes(int(bits[i:i+8],2) for i in range(0,len(bits)-len(bits)%8,8)).decode(errors='replace')
if len(sys.argv)<2: sys.exit("Usage: steganography <encode|decode> [message] [cover_text]")
if sys.argv[1]=='encode':
    msg=sys.argv[2] if len(sys.argv)>2 else 'secret'
    cover=sys.argv[3] if len(sys.argv)>3 else 'This is a normal sentence.'
    result=encode(msg,cover); print(f"Encoded ({len(result)} chars): {result}")
    print(f"Visible: {result.encode().decode('unicode_escape') if False else ''.join(c for c in result if ord(c)>32)}")
else:
    text=sys.argv[2] if len(sys.argv)>2 else sys.stdin.read()
    print(f"Hidden message: {decode(text)}")
