#!/usr/bin/env python3
"""Text steganography — hide messages using invisible characters."""
import sys
def encode_whitespace(cover, secret):
    bits="".join(format(ord(c),"08b") for c in secret)+"00000000"
    lines=cover.split("\n"); result=[]; bi=0
    for line in lines:
        trailing=""
        while bi<len(bits):
            trailing+=" " if bits[bi]=="0" else "\t"
            bi+=1
            if bi%8==0: break
        result.append(line+trailing)
    return "\n".join(result)
def decode_whitespace(text):
    bits=""
    for line in text.split("\n"):
        stripped=line.rstrip()
        trailing=line[len(stripped):]
        for c in trailing: bits+="0" if c==" " else "1"
    chars=[]
    for i in range(0,len(bits)-7,8):
        byte=bits[i:i+8]; val=int(byte,2)
        if val==0: break
        chars.append(chr(val))
    return "".join(chars)
def encode_zwc(cover, secret):
    zwsp="\u200b"; zwnj="\u200c"
    bits="".join(format(ord(c),"08b") for c in secret)
    encoded="".join(zwsp if b=="0" else zwnj for b in bits)
    mid=len(cover)//2
    return cover[:mid]+encoded+cover[mid:]
def cli():
    if len(sys.argv)<2: print("Usage: steganography encode|decode <cover> <secret>"); sys.exit(1)
    cmd=sys.argv[1]
    if cmd=="encode":
        cover=sys.argv[2] if len(sys.argv)>2 else "Nothing to see here"
        secret=sys.argv[3] if len(sys.argv)>3 else "hidden"
        result=encode_zwc(cover, secret)
        print(f"  Cover: {cover}"); print(f"  Encoded: {result}"); print(f"  Length: {len(cover)} → {len(result)} (+{len(result)-len(cover)} invisible)")
    elif cmd=="decode":
        print("  Provide encoded text as argument")
if __name__=="__main__": cli()
