# Copyright (c) 2017, shgoy. All rights reserved.
import os
import sys
from PIL import Image, ImageChops

def composite_center(front, bg, scale):
    wf1, hf1 = front.size
    fg = front.resize((int(wf1 * scale), int(hf1 * scale)))
    wf, hf = fg.size
    wb, hb = bg.size
    w = min(wf, wb)
    h = min(hf, hb)
    px = (wf-w)//2
    py = (hf-h)//2
    box = (px, py, px+w, py+h)
    cropped = fg.crop(box)
    
    px2 = (wb-w)//2
    py2 = (hb-h)//2
    boxb = (px2, py2, px2+w, py2+h)
    out = bg.copy()
    out.paste(cropped, boxb)
    return out
    
def main():
    if len(sys.argv) != 3:
        print("Usage: python morimori.py path/to/input.png path/to/output.gif")
        return 1

    filename = sys.argv[1]
    outname  = sys.argv[2]
    img = Image.open(filename)
    im = img.copy().convert("RGBA")
    base = Image.new('RGBA', (im.size), (255,255,255, 0))
    
    im1 = composite_center(im, base, 1.4)
    white = Image.new('RGBA', (im.size), (200,200,200, 0))
    im1 = ImageChops.screen(im1, white)
    
    im2 = composite_center(im, base, 0.9)
    
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    im.save (".tmp/0.png")
    im1.save(".tmp/1.png")
    im2.save(".tmp/2.png")
    os.system("convert -loop 0 -dispose Previous -delay 4 .tmp/0.png -delay 18 .tmp/{1..2}.png -delay 140 .tmp/0.png %s" % outname)
    os.system("rm -r .tmp")

if __name__=="__main__":
    main()