#!/usr/bin/env python3

import base64
import re
import zlib
import sys
import json
from pyzbar.pyzbar import decode as qr_decode
from PIL import Image

def decode(data):
  missing_padding = len(data) % 4
  if missing_padding:
      data += "="* (4 - missing_padding)
  return base64.urlsafe_b64decode(data)

def main():
    if len(sys.argv) < 2:
        print('Usage: ', sys.argv[0], ' <qr.jpg>')
        exit

    filename = sys.argv[1]
    try:
        img = Image.open(filename)
    except:
        print('Couldn\'t open ', filename)
        exit

    qr_raw = qr_decode(img)
    qr_data = qr_raw[0].data.decode('utf-8')

    parts = re.findall("..", qr_data[5:])

    jws = ""
    for p in parts:
      jws += chr(int(p)+ 45)

    # print("JWS:", jws)


    jws_parts = list(map(decode, jws.split(".")))

    #print("JWS Header:")
    print(jws_parts[0].decode('utf-8'))

# https://bugs.python.org/issue5784
    shc_data = zlib.decompress(jws_parts[1], wbits=-15)

    #print("SHC Data:")
    print(shc_data.decode('utf-8'))

if __name__ == "__main__":
    main()
