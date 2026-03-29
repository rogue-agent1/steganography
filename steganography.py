#!/usr/bin/env python3
"""steganography - Zero-width character steganography."""
import sys,argparse,json
ZWC={"0":"\u200b","1":"\u200c"}
def hide(cover,secret):
    bits="".join(format(ord(c),"08b") for c in secret)
    encoded="".join(ZWC[b] for b in bits)
    mid=len(cover)//2
    return cover[:mid]+encoded+cover[mid:]
def reveal(text):
    bits=""
    for ch in text:
        if ch=="\u200b":bits+="0"
        elif ch=="\u200c":bits+="1"
    chars=[]
    for i in range(0,len(bits),8):
        byte=bits[i:i+8]
        if len(byte)==8:chars.append(chr(int(byte,2)))
    return "".join(chars)
def main():
    p=argparse.ArgumentParser(description="Steganography")
    sub=p.add_subparsers(dest="cmd")
    h=sub.add_parser("hide");h.add_argument("cover");h.add_argument("secret")
    r=sub.add_parser("reveal");r.add_argument("text")
    args=p.parse_args()
    if args.cmd=="hide":
        result=hide(args.cover,args.secret)
        print(json.dumps({"cover_length":len(args.cover),"result_length":len(result),"hidden_chars":len(result)-len(args.cover),"result":result}))
    elif args.cmd=="reveal":
        secret=reveal(args.text)
        print(json.dumps({"revealed":secret,"length":len(secret)}))
    else:p.print_help()
if __name__=="__main__":main()
