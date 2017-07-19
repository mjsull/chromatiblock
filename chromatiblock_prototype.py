import sys
from argparse import ArgumentParser
import subprocess
import os
import glob
from ete3 import Tree
import sys
from ete3 import NodeStyle
from ete3 import TreeStyle


def colorstr(rgb):
    return "#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2])


# take a hue, saturation and lightness value and return a RGB hex string
def hsl_to_str(h, s, l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs(h *1.0 / 60 % 2 - 1))
    m = l - c/2
    if h < 60:
        r, g, b = c + m, x + m, 0 + m
    elif h < 120:
        r, g, b = x + m, c+ m, 0 + m
    elif h < 180:
        r, g, b = 0 + m, c + m, x + m
    elif h < 240:
        r, g, b, = 0 + m, x + m, c + m
    elif h < 300:
        r, g, b, = x + m, 0 + m, c + m
    else:
        r, g, b, = c + m, 0 + m, x + m
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return "#%02x%02x%02x" % (r,g,b)


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs(h *1.0 / 60 % 2 - 1))
    m = l - c/2
    if h < 60:
        r, g, b = c + m, x + m, 0 + m
    elif h < 120:
        r, g, b = x + m, c+ m, 0 + m
    elif h < 180:
        r, g, b = 0 + m, c + m, x + m
    elif h < 240:
        r, g, b, = 0 + m, x + m, c + m
    elif h < 300:
        r, g, b, = x + m, 0 + m, c + m
    else:
        r, g, b, = c + m, 0 + m, x + m
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return (r,g,b)

class scalableVectorGraphics:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.out = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   height="%d"
   width="%d"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.4 r9939"
   sodipodi:docname="easyfig">
  <metadata
     id="metadata122">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>Easyfig</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs120" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="640"
     inkscape:window-height="480"
     id="namedview118"
     showgrid="false"
     inkscape:zoom="0.0584"
     inkscape:cx="2500"
     inkscape:cy="75.5"
     inkscape:window-x="55"
     inkscape:window-y="34"
     inkscape:window-maximized="0"
     inkscape:current-layer="svg2" />
  <title
     id="title4">Easyfig</title>
  <g
     style="fill-opacity:1.0; stroke:black; stroke-width:1;"
     id="g6">''' % (self.height, self.width)

    def drawLine(self, x1, y1, x2, y2, th=1, cl=(0, 0, 0), alpha = 1.0):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="butt" />\n' % (x1, y1, x2, y2, th, colorstr(cl), alpha)

    def drawPath(self, xcoords, ycoords, th=1, cl=(0, 0, 0), alpha=0.9):
        self.out += '  <path d="M%d %d' % (xcoords[0], ycoords[0])
        for i in range(1, len(xcoords)):
            self.out += ' L%d %d' % (xcoords[i], ycoords[i])
        self.out += '"\n        stroke-width="%d" stroke="%s" stroke-opacity="%f" stroke-linecap="butt" fill="none" z="-1" />\n' % (th, colorstr(cl), alpha)


    def writesvg(self, filename):
        outfile = open(filename, 'w')
        outfile.write(self.out + ' </g>\n</svg>')
        outfile.close()

    def drawRightArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + wid - ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x1, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y, x, y+ht, x + wid, y1)

    def drawLeftArrow(self, x, y, wid, ht, fc, oc=(0,0,0), lt=1):
        if lt > ht /2:
            lt = ht/2
        x1 = x + wid
        y1 = y + ht/2
        x2 = x + ht / 2
        ht -= 1
        if wid > ht/2:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y+ht/4, x2, y+ht/4,
                                                                                                x2, y, x, y1, x2, y+ht,
                                                                                                x2, y+3*ht/4, x1, y+3*ht/4)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fc), colorstr(oc), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x, y1, x1, y+ht, x1, y)

    def drawBlastHit(self, x1, y1, x2, y2, x3, y3, x4, y4, fill=(0, 0, 255), lt=2, alpha=0.1):
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0,0,0)), lt, alpha)
        self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y2, x3, y3, x4, y4)

    def drawGradient1(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n  </defs>\n'
        self.out += '  <rect fill="url(#MyGradient)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d"/>\n' % (x1, y1, wid, hei)

    def drawGradient2(self, x1, y1, wid, hei, minc, maxc):
        self.out += '  <defs>\n    <linearGradient id="MyGradient2" x1="0%" y1="0%" x2="0%" y2="100%">\n'
        self.out += '      <stop offset="0%%" stop-color="%s" />\n' % colorstr(maxc)
        self.out += '      <stop offset="100%%" stop-color="%s" />\n' % colorstr(minc)
        self.out += '    </linearGradient>\n</defs>\n'
        self.out += '  <rect fill="url(#MyGradient2)" stroke-width="0"\n'
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawOutRect(self, x1, y1, wid, hei, fill, outfill, lt=1, alpha=1.0, alpha2=1.0):
        self.out += '  <rect stroke="%s" stroke-width="%d" stroke-opacity="%f"\n' % (colorstr(outfill), lt, alpha)
        self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha2)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawGradient(self, id, gradient):
        self.out += '  <defs>\n'
        self.out += '    <linearGradient id="lg%d"\n' % id
        self.out += '            x1="0%" y1="0%"\n'
        self.out += '            x2="100%" y2="0%"\n'
        self.out += '            spreadMethod="pad">\n'
        for i in gradient:
            self.out += '    <stop offset="%d%%" stop-color="%s" stop-opacity="1"/>\n' % (i[0], colorstr(i[1]))
        self.out += '    </linearGradient>\n'
        self.out += '  </defs>\n'

    def drawAlignment(self, x, y, id, lt, fill):
        if id is None:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" \n' % (colorstr(fill), '#000000', lt)
        else:
            self.out += '  <polygon style="fill:url(#lg%d)re; stroke: %s; stroke-width: %d;"\n' % (id, '#000000', lt)
        self.out += '  points="'
        for i, j in zip(x, y):
            self.out += str(i) + ',' + str(j) + ' '
        self.out += '" />\n'

    def create_diag_pattern(self, id, fill, pattern, width):
        if pattern == 'horizontal':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="%d" y2="0" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'forward_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'
        elif pattern == 'reverse_diag':
            self.out += '    <defs>\n'
            self.out += '      <pattern id="%s" width="%d" height="%d" patternTransform="rotate(135 0 0)" patternUnits="userSpaceOnUse">\n' % (id, width, width)
            self.out += '        <line x1="0" y1="0" x2="0" y2="%d" style="stroke:%s; stroke-width:%d; fill:#FFFFFF" />\n' % (width, fill, width)
            self.out += '      </pattern>\n'
            self.out += '   </defs>\n'


    def drawStripedRect(self, x, y, width, height, id, fill, lt):
        self.out += '  <rect style="fill:#FFFFFF; stroke: %s; stroke-width: %d;"\n' % (fill, lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)
        self.out += '  <rect style="fill:url(#%s); stroke: %s; stroke-width: %d; stroke-alignment: inner;"\n' % (id, fill, lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x, y, width, height)

    def drawSymbol(self, x, y, size, fill, symbol, alpha=1.0, lt=1):
        x0 = x - size/2
        x1 = size/8 + x - size/2
        x2 = size/4 + x - size/2
        x3 = size*3/8 + x - size/2
        x4 = size/2 + x - size/2
        x5 = size*5/8 + x - size/2
        x6 = size*3/4 + x - size/2
        x7 = size*7/8 + x - size/2
        x8 = size + x - size/2
        y0 = y - size/2
        y1 = size/8 + y - size/2
        y2 = size/4 + y - size/2
        y3 = size*3/8 + y - size/2
        y4 = size/2 + y - size/2
        y5 = size*5/8 + y - size/2
        y6 = size*3/4 + y - size/2
        y7 = size*7/8 + y - size/2
        y8 = size + y - size/2
        if symbol == 'o':
            self.out += '  <circle stroke="%s" stroke-width="%d" stroke-opacity="%f"\n' % (colorstr((0, 0, 0)), lt, alpha)
            self.out += '        fill="%s" fill-opacity="%f"\n' % (colorstr(fill), alpha)
            self.out += '        xc="%d" yc="%d" r="%d" />\n' % (x, y, size/2)
        elif symbol == 'x':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y2, x2, y0, x4, y2, x6, y0, x8, y2,
                                                                                                                             x6, y4, x8, y6, x6, y8, x4, y6, x2, y8,
                                                                                                                             x0, y6, x2, y4)
        elif symbol == '+':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x2, y0, x6, y0, x6, y2, x8, y2, x8, y6,
                                                                                                                             x6, y6, x6, y8, x2, y8, x2, y6, x0, y6,
                                                                                                                             x0, y2, x2, y2)
        elif symbol == 's':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x0, y8, x8, y8, x8, y0)
        elif symbol == '^':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y0, x2, y0, x4, y4, x6, y0, x8, y0, x4, y8)
        elif symbol == 'v':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x0, y8, x2, y8, x4, y4, x6, y8, x8, y8, x4, y0)
        elif symbol == 'u':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y8, x4, y0, x8, y8)
        elif symbol == 'd':
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d" stroke-opacity="%f" fill-opacity="%f"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt, alpha, alpha)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x0, y0, x4, y8, x8, y0)
        else:
            sys.stderr.write(symbol + '\n')
            sys.stderr.write('Symbol not found, this should not happen.. exiting')
            sys.exit()








    def drawRightFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht/2
            y2 = y + ht * 3/8
            y3 = y + ht * 1/4
        elif frame == 2:
            y1 = y + ht * 3/8
            y2 = y + ht * 1/4
            y3 = y + ht * 1/8
        elif frame == 0:
            y1 = y + ht * 1/4
            y2 = y + ht * 1/8
            y3 = y + 1
        x1 = x
        x2 = x + wid - ht/8
        x3 = x + wid
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawRightFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht / 4
        elif frame == 2:
            y1 = y + ht /8
        elif frame == 0:
            y1 = y + 1
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawLeftFrame(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht
            y2 = y + ht * 7/8
            y3 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 7/8
            y2 = y + ht * 3/4
            y3 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht * 3/4
            y2 = y + ht * 5/8
            y3 = y + ht / 2
        x1 = x + wid
        x2 = x + ht/8
        x3 = x
        if wid > ht/8:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d %d,%d %d,%d" />\n' % (x1, y1, x2, y1, x3, y2, x2, y3, x1, y3)
        else:
            self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
            self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y1, x3, y2, x1, y3)

    def drawLeftFrameRect(self, x, y, wid, ht, lt, frame, fill):
        if lt > ht /2:
            lt = ht /2
        if frame == 1:
            y1 = y + ht * 3/4
        elif frame == 2:
            y1 = y + ht * 5/8
        elif frame == 0:
            y1 = y + ht / 2
        hei = ht /4
        x1 = x
        self.out += '  <rect fill="%s" stroke-width="%d"\n' % (colorstr(fill), lt)
        self.out += '        x="%d" y="%d" width="%d" height="%d" />\n' % (x1, y1, wid, hei)

    def drawPointer(self, x, y, ht, lt, fill):
        x1 = x - int(round(0.577350269 * ht/2))
        x2 = x + int(round(0.577350269 * ht/2))
        y1 = y + ht/2
        y2 = y + 1
        self.out += '  <polygon fill="%s" stroke="%s" stroke-width="%d"\n' % (colorstr(fill), colorstr((0, 0, 0)), lt)
        self.out += '           points="%d,%d %d,%d %d,%d" />\n' % (x1, y2, x2, y2, x, y1)

    def drawDash(self, x1, y1, x2, y2, exont):
        self.out += '  <line x1="%d" y1="%d" x2="%d" y2="%d"\n' % (x1, y1, x2, y2)
        self.out += '       style="stroke-dasharray: 5, 3, 9, 3"\n'
        self.out += '       stroke="#000" stroke-width="%d" />\n' % exont

    def drawPolygon(self, x_coords, y_coords, colour=(0,0,255)):
        self.out += '  <polygon points="'
        for i,j in zip(x_coords, y_coords):
            self.out += str(i) + ',' + str(j) + ' '
        self.out += '"\nstyle="fill:%s;stroke=none" />\n'  % colorstr(colour)
    def writeString(self, thestring, x, y, size, ital=False, bold=False, rotate=0, justify='left'):
        if rotate != 0:
            x, y = y, x
        self.out += '  <text\n'
        self.out += '    style="font-size:%dpx;font-style:normal;font-weight:normal;z-index:10\
;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans"\n' % size
        if justify == 'right':
            self.out += '    text-anchor="end"\n'
        elif justify == 'middle':
            self.out += '    text-anchor="middle"\n'
        if rotate == 1:
            self.out += '    x="-%d"\n' % x
        else:
            self.out += '    x="%d"\n' % x
        if rotate == -1:
            self.out += '    y="-%d"\n' % y
        else:
            self.out += '    y="%d"\n' % y
        self.out += '    sodipodi:linespacing="125%"'
        if rotate == -1:
            self.out += '\n    transform="matrix(0,1,-1,0,0,0)"'
        if rotate == 1:
            self.out += '\n    transform="matrix(0,-1,1,0,0,0)"'
        self.out += '><tspan\n      sodipodi:role="line"\n'
        if rotate == 1:
            self.out += '      x="-%d"\n' % x
        else:
            self.out += '      x="%d"\n' % x
        if rotate == -1:
            self.out += '      y="-%d"' % y
        else:
            self.out += '      y="%d"' % y
        if ital and bold:
            self.out += '\nstyle="font-style:italic;font-weight:bold"'
        elif ital:
            self.out += '\nstyle="font-style:italic"'
        elif bold:
            self.out += '\nstyle="font-style:normal;font-weight:bold"'
        self.out += '>' + thestring + '</tspan></text>\n'

# contains element of each genome line
class genome_line:
    def __init__(self, name, seqDict, contig_order):
        self.name = name
        self.contig_order = contig_order
        self.contig_list = seqDict.keys()
        self.seq_dict = seqDict
        self.length_dict = {}
        self.block_dict = {}
        for i in seqDict:
            self.length_dict[i] = len(seqDict[i])
            self.block_dict[i] = []
# stores information about each alignment
class alignment:
    def __init__(self, fasta, contig, start, size, strand, nucl, core, key):
        self.fasta = fasta
        self.contig = contig
        self.start = start
        self.size = size
        self.size_gapped = len(nucl)
        self.strand = strand
        self.nucl = nucl
        self.core = core
        self.key = key

# contains list of blocks between each core colinear block
class between_core:
    def __init__(self, orient, block_list):
        self.orient = orient
        self.block_list = block_list


# creates a genome line from each Fasta entry in the glob
def get_seq_dict(glob_list):
    out_dict = {}
    for the_glob in glob_list: # for each fasta file create a genome line with name, dictionary of sequences and contig order
        for i in glob.glob(the_glob):
            if i.endswith('.fna') or i.endswith('.fa') or i.endswith('.fasta'):
                seqDict = {}
                contig_order = []
                with open(i) as ff:
                    for line in ff:
                        if line.startswith('>'):
                            name = line.rstrip()[1:]
                            seqDict[name] = ''
                            contig_order.append(name)
                        else:
                            try:
                                seqDict[name] += line.rstrip()
                            except IndexError:
                                sys.stderr.write(i + ' not a valid FASTA.')
                                sys.exit()
                if len(seqDict) >= 1:
                    if i.endswith('.fna'):
                        name = i.split('/')[-1][:-4]
                    elif i.endswith('.fa'):
                        name = i.split('/')[-1][:-3]
                    elif i.endswith('.fasta'):
                        name = i.split('/')[-1][:-6]
                aninstance = genome_line(name, seqDict, contig_order)
                out_dict[name] = aninstance
            else:
                sys.stderr.write(i + ' not fasta.. skipping.')
    return out_dict


# read in a mugsy alignment (.maf) attaches alignments to the dictionary of genome lines
def read_mugsy(mugsy_file, genome_line_dict):
    min_align_size = 1000
    align_list = []
    with open(mugsy_file) as mf: # get all alignment blocks from mugsy
        for line in mf:
            if line.startswith('a'):
                if len(align_list) > 0 and align_list[0].core == 'core':
                    getit = False
                    for a in align_list:
                        if a.size >= min_align_size:
                            getit = True
                    if getit:
                        for a in align_list:
                            genome_line_dict[a.fasta].block_dict[a.contig].append(a)
                elif len(align_list) >= 1:
                    for a in align_list:
                        genome_line_dict[a.fasta].block_dict[a.contig].append(a)
                if int(line.split()[3].split('=')[1]) == len(genome_line_dict):
                    core = 'core'
                else:
                    core = 'noncore'
                key = line.split()[2].split('=')[1]
                align_list = []
            elif line.startswith('s'):
                splitline = line.split()
                src = splitline[1]
                fasta = src.split('.')[0]
                contig = src.split('.')[1]
                start = int(splitline[2])
                size = int(splitline[3])
                strand = splitline[4]
                srcSize = int(splitline[5])
                nucl = splitline[6]
                if strand == '-':
                    start = srcSize - start - size
                if size >= min_align_size or core == 'core':
                    aninstance = alignment(fasta, contig, start, size, strand, nucl, core, key)
                    align_list.append(aninstance)
        if len(align_list) > 0 and align_list[0].core == 'core':
            getit = False
            for a in align_list:
                if a.size >= min_align_size:
                    getit = True
            if getit:
                for a in align_list:
                    genome_line_dict[a.fasta].block_dict[a.contig].append(a)
        elif len(align_list) >= 1:
            for a in align_list:
                genome_line_dict[a.fasta].block_dict[a.contig].append(a)
    for fasta, genome_line in genome_line_dict.iteritems(): # create "single" blocks for unaligned regions
        col_no = 0
        for contig, alignments in genome_line.block_dict.iteritems():
            alignments.sort(key=lambda x: x.start)
            lastend = 0
            new_blocks = []
            for i in alignments:
                if i.core == 'core':
                    i.colour = col_no
                    col_no += 1
                if i.start > lastend:
                     aninstance = alignment(fasta, contig, lastend, i.start-lastend, '+', genome_line.seq_dict[contig][lastend:i.start], 'single', 'na')
                     new_blocks.append(aninstance)
                lastend = i.start + i.size
            if genome_line.length_dict[contig] > lastend:
                aninstance = alignment(fasta, contig, lastend, genome_line.length_dict[contig]-lastend, '+', genome_line.seq_dict[contig][lastend:], 'single', 'na')
                new_blocks.append(aninstance)
            alignments += new_blocks
            alignments.sort(key=lambda x: x.start)


# get average color of two colors
def get_ave_col(col1, col2):
    r1 = int(col1[1:3], 16)
    g1 = int(col1[3:5], 16)
    b1 = int(col1[5:], 16)
    r2 = int(col2[1:3], 16)
    g2 = int(col2[3:5], 16)
    b2 = int(col2[5:], 16)
    r, g, b = int(((r1**2 + r2**2)/2) ** 0.5), int(((g1**2 + g2**2)/2) ** 0.5), int(((b1**2 + b2**2)/2) ** 0.5)
    return "#%02x%02x%02x" % (r,g,b)


# gets the position of each variant between two strains and add them to a dictionary
def getGraphDict(the_glob):
    out_dict = {}
    for i in the_glob:
        with open(i) as varf:
            for line in varf:
                if line.startswith('Variant'):
                    stuff, qname, pos1, pos2, rname, pos3, pos4 = line.split()[:7]
                    if qname in out_dict:
                        out_dict[qname].append(int(pos1))
                    else:
                        out_dict[qname] = [int(pos1)]
                    if rname in out_dict:
                        out_dict[rname].append(int(pos3))
                    else:
                        out_dict[rname] = [int(pos3)]
    return out_dict


# creates a graph of variant counts in each core block
def graphit(genome_line_dict, ref_name, graph_dict):
    bin_size = 5000
    if ref_name is None:
        for i in genome_line_dict:
            ref_name = i
            break
    for i in genome_line_dict:
        if ref_name in i:
            ref_name = i
    core_order = []
    for contig, alignments in genome_line_dict[ref_name].block_dict.iteritems():
        for i in alignments:
            if i.core == 'core':
                core_order.append((i.key, i.strand, i.size_gapped))
    out_graph = {}
    for fasta, genome_line in genome_line_dict.iteritems():
        for contig, alignments in genome_line.block_dict.iteritems():
            new_fasta = None
            for j in graph_dict:
                if fasta[:-5] in j:
                    new_fasta = j
            if new_fasta is None:
                break
            for blocks in alignments:
                if blocks.core == 'core':
                    for j in graph_dict[new_fasta]:
                        if blocks.start <= j <= blocks.start + blocks.size:
                            curr_k = blocks.start
                            if blocks.strand == '+':
                                for align_num, k in enumerate(blocks.nucl):
                                    if k == '-':
                                        pass
                                    else:
                                        curr_k += 1
                                        if curr_k == j:
                                            if blocks.key in out_graph:
                                                if align_num/bin_size in out_graph[blocks.key]:
                                                    out_graph[blocks.key][align_num/bin_size] += 1
                                                else:
                                                    out_graph[blocks.key][align_num/bin_size] = 1
                                            else:
                                                out_graph[blocks.key] = {align_num/bin_size:1}
                                            break
                            else:
                                for align_num, k in enumerate(blocks.nucl[::-1]):
                                    if k == '-':
                                        pass
                                    else:
                                        curr_k += 1
                                        if curr_k == j:
                                            pos_in_block = blocks.size_gapped - align_num
                                            if blocks.key in out_graph:
                                                if align_num/bin_size in out_graph[blocks.key]:
                                                    out_graph[blocks.key][pos_in_block/bin_size] += 1
                                                else:
                                                    out_graph[blocks.key][pos_in_block/bin_size] = 1
                                            else:
                                                out_graph[blocks.key] = {pos_in_block/bin_size:1}
                                            break
    out_list = []
    for i in core_order:
        aninstance = []
        for j in range(0, i[2]/bin_size):
            try:
                aninstance.append(out_graph[i[0]][j])
            except:
                aninstance.append(0)
        out_list.append(aninstance)
    return out_list



# get the position for each of the blocks in each genome_line
def get_block_coords(genome_line_dict, ref_name=None):
    if ref_name is None:
        for i in genome_line_dict:
            ref_name = i
            break
    core_order = []
    ref_seq = {}
    min_gap = 1000
    for i in genome_line_dict:
        if ref_name in i:
            ref_name = i
    for contig, alignments in genome_line_dict[ref_name].block_dict.iteritems():
        for i in alignments:
            if i.core == 'core':
                core_order.append((i.key, i.strand))
                ref_seq[i.key] = i.nucl
    out_dict = {}
    between_where = {}
    for fasta, genome_line in genome_line_dict.iteritems():
        plasmid_dict = {}
        last_core = None
        ordered_core = []
        between = []
        for i in core_order:
            for contig, alignments in genome_line.block_dict.iteritems():
                last_core_align = None
                for j in alignments:
                    if j.core == 'core':
                        if (j.key, j.strand) == i:
                            j.snps = []
                            gap_size = 0
                            j.gaps = []
                            for base in range(len(j.nucl)):
                                if j.nucl[base] != ref_seq[j.key][base]:
                                    j.snps.append(base)
                                if j.nucl[base] == '-':
                                    if gap_size == 0:
                                        gap_start = base
                                    gap_size += 1
                                else:
                                    if gap_size >= min_gap:
                                        j.gaps.append((gap_start, gap_start + gap_size))
                                    gap_size = 0
                            if last_core is None:
                                ordered_core.append(j)
                            elif last_core_align == last_core:
                                ordered_core.append(between_core('middle', between))
                                ordered_core.append(j)
                            else:
                                ordered_core.append('break')
                                ordered_core.append(j)
                            j.backward = between
                            j.backward_block = last_core_align
                        elif j.key == i[0]:
                            j.forward = between[::-1]
                            j.forward_block = last_core_align
                        between_where[tuple(between)] = (last_core_align, (j.key, j.strand))
                        last_core_align = (j.key, j.strand)
                        between = []
                    else:
                        between.append((j.key, j.size))
                if last_core_align is None:
                    plasmid_dict[contig] = between
                    between = []
                last_core_align = None
                for j in alignments[::-1]:
                    if j.core == 'core':
                        if j.key == i[0] and j.strand != i[1]:
                            j.backward = between
                            j.snps = []
                            gap_size = 0
                            j.gaps = []
                            for base in range(len(j.nucl)):
                                if j.nucl[base] != ref_seq[j.key][base]:
                                    j.snps.append(base)
                                if j.nucl[base] == '-':
                                    if gap_size == 0:
                                        gap_start = base
                                    gap_size += 1
                                else:
                                    if gap_size >= min_gap:
                                        j.gaps.append((gap_start, gap_start + gap_size))
                                    gap_size = 0
                            if last_core is None:
                                ordered_core.append(j)
                            elif last_core_align == last_core:
                                ordered_core.append(between_core('middle', between))
                                ordered_core.append(j)
                            else:
                                ordered_core.append('break')
                                ordered_core.append(j)
                            j.backward = between
                            j.backward_block = last_core_align
                        elif j.key == i[0]:
                            j.forward = between[::-1]
                            j.forward_block = last_core_align
                        if j.strand == '+':
                            last_core_align = (j.key, '-')
                            between_where[tuple(between)] = (last_core_align, (j.key, '-'))
                        else:
                            last_core_align = (j.key, '+')
                            between_where[tuple(between)] = (last_core_align, (j.key, '+'))
                        between = []
                    else:
                        between.append((j.key, j.size))
            last_core = i
        out_dict[fasta] = (ordered_core, plasmid_dict)
    return out_dict


# determine which core and noncore blocks are adjacent
def attached_to_place(out_dict):
    for i in out_dict:
        genome_line = out_dict[i][0]
        for j in range(len(genome_line)):
            if genome_line[j] == 'break':
                if genome_line[j-1].forward != [] and not genome_line[j-1].forward is None:
                    genome_line[j] = between_core('left', genome_line[j-1].forward)
                    test = genome_line[j-1].forward[:]
                    genome_line[j-1].forward = None
                    for count, k in enumerate(genome_line):
                        if count % 2 == 0 and k.key == genome_line[j-1].forward_block[0]:
                            if not k.forward is None and (k.forward[::-1] == test or k.forward == test):
                                k.forward = None
                            if not k.backward is None and (k.backward[::-1] == test or k.backward == test):
                                k.backward = None
                elif genome_line[j+1].backward != [] and not genome_line[j+1].backward is None:
                    genome_line[j] = between_core('right', genome_line[j+1].backward)
                    test = genome_line[j+1].backward[:]
                    genome_line[j+1].backward = None
                    for count, k in enumerate(genome_line):
                        if count % 2 == 0 and k.key == genome_line[j+1].backward_block[0]:
                            if not k.forward is None and (k.forward[::-1] == test or k.forward == test):
                                k.forward = None
                            if not k.backward is None and (k.backward[::-1] == test or k.backward == test):
                                k.backward = None
            elif j % 2 == 1:
                genome_line[j-1].forward = None
                genome_line[j+1].backward = None






# convert base pair positon to an x coordinate in the figure
def x_coord(bp_pos, genome_width, max_width_bp, width, x_margin, align='left'):
    if align == 'center':
        return (bp_pos * 1.0 + (max_width_bp - genome_width) * 1.0/2) / max_width_bp * width + x_margin
    elif align == 'left':
        return bp_pos * 1.0 / max_width_bp * width + x_margin

# draws a tree with ete toolkit and writes to an svg - this is then read an incorporated into the final figure
def draw_tree(the_tree, out_file, color_dict=None, label=False):
    t = Tree(the_tree)
    o = t.get_midpoint_outgroup()
    t.set_outgroup(o)
    the_leaves = []
    for leaves in t.iter_leaves():
        the_leaves.append(leaves)
    groups = {}
    num = 0
    # set cutoff value for clades as 1/20th of the distance between the furthest two branches
    clade_cutoff = t.get_distance(the_leaves[0], the_leaves[-1]) /20
    # assign nodes to groups
    last_node = None
    if color_dict is None:
        out_list = []
        for node in the_leaves:
            i = node.name
            out_list.append(i)
            if not last_node is None:
                if t.get_distance(node, last_node) <= clade_cutoff:
                    groups[group_num].append(i)
                else:
                    groups[num] = [num, i]
                    group_num = num
                    num += 1
            else:
                groups[num] = [num, i]
                group_num = num
                num += 1
            last_node = node
    else:
        out_list = []
        the_colors = {}
        tree_colours = {}
        with open(color_dict) as cd:
            for num, line in enumerate(cd):
                the_colors[line.split()[0]] = [line.split()[1], num]
                tree_colours[num] = line.split()[1]
        for node in the_leaves:
            i = node.name
            for j in the_colors:
                if j in i:
                    group_num = the_colors[j][1]
                    if group_num in groups:
                        out_list.append(node.name)
                        groups[group_num].append(i)
                    else:
                        out_list.append('gap')
                        out_list.append(node.name)
                        groups[group_num] = [group_num, i]
        out_list = out_list[1:]
        ca_list = []
        # Colour each group and then get the common ancestor node of each group
        for i in groups:
            the_col = tree_colours[groups[i][0]]
            style = NodeStyle()
            style['size'] = 0
            style["vt_line_color"] = the_col
            style["hz_line_color"] = the_col
            style["vt_line_width"] = 2
            style["hz_line_width"] = 2
            if len(groups[i]) == 2:
                ca = t.search_nodes(name=groups[i][1])[0]
                ca.set_style(style)
            else:
                ca = t.get_common_ancestor(groups[i][1:])
                ca.set_style(style)
                tocolor = []
                for j in ca.children:
                    tocolor.append(j)
                while len(tocolor) > 0:
                    x = tocolor.pop(0)
                    x.set_style(style)
                    for j in x.children:
                        tocolor.append(j)
            ca_list.append((ca, the_col))
        # for each common ancestor node get it's closest common ancestor neighbour and find the common ancestor of those two nodes
        # colour the common ancestor then add it to the group - continue until only the root node is left
        while len(ca_list) > 1:
            distance = float('inf')
            for i, col1 in ca_list:
                for j, col2 in ca_list:
                    if not i is j:
                        parent = t.get_common_ancestor(i, j)
                        getit = True
                        for children in parent.children:
                            if children != i and children != j:
                                getit = False
                                break
                        if getit:
                            the_dist = t.get_distance(i, j)
                            if the_dist <= distance:
                                distance = the_dist
                                the_i = i
                                the_j = j
                                the_i_col = col1
                                the_j_col = col2
            ca_list.remove((the_i, the_i_col))
            ca_list.remove((the_j, the_j_col))
            the_col = get_ave_col(the_i_col, the_j_col)
            new_node = t.get_common_ancestor(the_i, the_j)
            style = NodeStyle()
            style['size'] = 0
            style["vt_line_color"] = the_col
            style["hz_line_color"] = the_col
            style["vt_line_width"] = 2
            style["hz_line_width"] = 2
            new_node.set_style(style)
            ca_list.append((new_node, the_col))
    ts = TreeStyle()
    # Set these to False if you 2don't want bootstrap/distance values
    ts.show_branch_length = False
    ts.show_branch_support = False
    ts.margin_left = 10
    ts.margin_right = 0
    ts.margin_top = 0
    ts.margin_bottom = 0
    ts.scale = 1000
    t.render(out_file, h=len(the_leaves) * (genome_line_space + 1) * 2, units='px', tree_style=ts)
    return out_list


# draw the figure with all information
def draw_fig(in_dict, working_dir, order_list, graph_list):
    new_order_list = order_list
    order_list = []
    genome_line_thick = 30
    y_gap_size = 100
    conserved_thick = 200
    conserved_gap_thick = 66
    filler_block_width = 150
    max_snp = 20
    figure_width = 10000
    fill_gap = 10
    x_margin = 50
    gradient_count = 0
    gap_sizes = []
    for i in in_dict:
        lengths = []
        for num, j in enumerate(in_dict[i][0]):
            if num % 2 == 0:
                lengths.append(j.size_gapped)
            elif j == 'break':
                lengths.append(0)
            else:
                size = 0
                for k in j.block_list:
                    size += k[1]
                lengths.append(size)
        gap_sizes.append(lengths)
    max_fill = [0 for i in range(len(gap_sizes[0]))]
    for i in range(len(gap_sizes[0])):
        for j in gap_sizes:
            if j[i] >= max_fill[i]:
                max_fill[i] = j[i]
    bin_size = 1000
    the_tree = ''
    with open(working_dir + '/tree.svg') as tree:
        for line in tree:
            the_tree += line.rstrip()
    tf_list = []
    tf_start = None
    for i in range(0, len(the_tree)):
        if the_tree[i:i+2] == '<g':
            tf_start = i
        elif the_tree[i:i+4] == '</g>' and not tf_start is None:
            tf_list.append(the_tree[tf_start:i+4])
            tf_start = None
    svg_stuff = ''
    y_pos_dict = {}
    max_x = 0
    y_pos_list = []
    for i in tf_list:
        if '<text ' in i:
            get_next = 0
            for j in i.split('"'):
                if 'transform=' in j:
                    get_next = 1
                elif ' y=' == j:
                    get_next = 2
                elif get_next == 1:
                    get_next = 0
                    a,b,c,d,e,f = map(float, j[7:-1].split(','))
                elif get_next == 2:
                    get_next = 0
                    y = int(j)
                    new_y = d*y + f
            name = i.split('>')[-3].split('<')[0]
            y_pos_list.append(new_y)
    gap_list = []
    count = 0
    for i in new_order_list:
        if i == 'gap':
            gap_list.append((y_pos_list[count-1] + y_pos_list[count]) / 2)
        else:
            order_list.append(i)
            count += 1
    max_y = 0
    y_tree_mod = 70
    for i in tf_list:
        if '<polyline ' in i:
            get_next = 0
            new_line = '    '
            first = True
            to_add = None
            for j in i.split('"'):
                if 'transform=' in j:
                    get_next = 1
                elif 'points=' in j:
                    get_next = 2
                    new_line += '"' + j
                elif 'stroke-width=' in j:
                    get_next = 3
                    try:
                        a = a
                        new_line += '"' + j
                    except UnboundLocalError:
                        to_add = ['"' + j]
                elif get_next == 1:
                    get_next = 0
                    a,b,c,d,e,f = map(float, j[7:-1].split(','))
                    if not to_add is None:
                        new_line += to_add[0]
                        new_line += '"' + str(float(to_add[1]) * a)
                        to_add = None
                elif get_next == 2:
                    get_next = 0
                    new_line += '"'
                    for k in j.split():
                        x, y = map(float, k.split(','))
                        new_x = a*x + c*y + e
                        new_y = b*x + d*y + f
                        gap_num = 0
                        for qq in gap_list:
                            if new_y < qq:
                                break
                            else:
                                gap_num += 1
                        new_y += gap_num * y_gap_size
                        new_y += y_tree_mod
                        if new_x > max_x:
                            max_x = new_x
                        new_line += str(new_x) + ',' + str(new_y) + ' '
                elif get_next == 3:
                    get_next = 0
                    try:
                        new_line += '"' + str(float(j) * a)
                    except UnboundLocalError:
                        to_add.append(j)
                else:
                    if first:
                        first = False
                        new_line += j
                    else:
                        new_line += '"' + j
            svg_stuff += new_line + '\n'
        elif '<text ' in i:
            get_next = 0
            for j in i.split('"'):
                if 'transform=' in j:
                    get_next = 1
                elif ' y=' == j:
                    get_next = 2
                elif get_next == 1:
                    get_next = 0
                    a,b,c,d,e,f = map(float, j[7:-1].split(','))
                elif get_next == 2:
                    get_next = 0
                    y = int(j)
                    new_y = d*y + f
            name = i.split('>')[-3].split('<')[0]
            gap_num = 0
            for qq in gap_list:
                if new_y < qq:
                    break
                else:
                    gap_num += 1
            new_y += gap_num * y_gap_size
            y_pos_dict[name] = new_y
            if max_y < new_y:
                max_y = new_y
    max_x += 20
    plasmid_sizes = []
    for i in in_dict:
        total_size =0
        for j in in_dict[i][1]:
            for k in in_dict[i][1][j]:
                total_size += k[1]
            total_size = int(total_size * 1.1)
        plasmid_sizes.append(total_size)
    svg = scalableVectorGraphics(max_y + genome_line_space + 300, figure_width + max_x + x_margin + 1000)
    svg.out += svg_stuff
    new_order_list = []
    for i in order_list:
        for j in in_dict:
            if i in j:
                new_order_list.append(j)
                y_pos_dict[j] = y_pos_dict[i]
                break
    x_scale = (sum(max_fill) + max(plasmid_sizes)) / (figure_width - len(max_fill) * fill_gap)
    s = 0.8
    new_hue = 0
    pattern_list = ['horizontal', 'forward_diag', 'reverse_diag']
    saturation_list = [0.4, 0.6, 0.8]
    lightness_list = [0.3, 0.5]
    hue_list = [0, 40, 80, 120, 160, 200, 240, 280, 320, 20, 60, 100, 140, 180, 220, 260, 300, 340]
    color_patt = []
    for l in saturation_list:
        for k in lightness_list:
            for j in pattern_list:
                for i in hue_list:
                    color_patt.append((i, j, k, l))
    align_dict = {}
    for i in new_order_list:
        for num, j in enumerate(in_dict[i][0]):
            if num % 2 == 1 and not j == 'break' and not j.block_list == []:
                for k in j.block_list:
                    if k[0] != 'na' and not k[0] in align_dict:
                        the_hue = hsl_to_str(color_patt[new_hue % len(color_patt)][0], color_patt[new_hue % len(color_patt)][3], color_patt[new_hue % len(color_patt)][2])
                        pattern = color_patt[new_hue % len(color_patt)][1]
                        align_dict[k[0]] = ('diag' + str(new_hue), the_hue)
                        svg.create_diag_pattern('diag' + str(new_hue), the_hue, pattern, 75)
                        new_hue += 1
        for j in in_dict[i][1]:
            for k in in_dict[i][1][j]:
                if k[0] != 'na' and not k[0] in align_dict:
                    the_hue = hsl_to_str(color_patt[new_hue % len(color_patt)][0], color_patt[new_hue % len(color_patt)][3], color_patt[new_hue % len(color_patt)][2])
                    pattern = color_patt[new_hue % len(color_patt)][1]
                    align_dict[k[0]] = ('diag' + str(new_hue), the_hue)
                    svg.create_diag_pattern('diag' + str(new_hue), the_hue, pattern, 75)
                    new_hue += 1
    for i in new_order_list:
        core_block_no = float(len(in_dict[i][0]) / 2)
        curr_y = y_pos_dict[i]
        for num, j in enumerate(in_dict[i][0]):
            curr_x = sum(max_fill[:num]) / x_scale + fill_gap * num + max_x
            x_size = max_fill[num] / x_scale
            x_size_bp = max_fill[num]
            if num % 2 == 0:
                h = (j.colour * 1.0 / core_block_no * 340)
                y_pos_align = curr_y + conserved_thick / 2
                y_pos = curr_y - conserved_thick /2
                y_pos_gap_a = curr_y + conserved_gap_thick / 2
                y_pos_gap_b = curr_y - conserved_gap_thick / 2
                x_coords = [curr_x, curr_x]
                y_coords = [y_pos, y_pos_align]
                for gap in j.gaps:
                    x_coords.append(curr_x + gap[0] / x_scale)
                    x_coords.append(curr_x + gap[0] / x_scale)
                    x_coords.append(curr_x + gap[1] / x_scale)
                    x_coords.append(curr_x + gap[1] / x_scale)
                    y_coords.append(y_pos_align)
                    y_coords.append(y_pos_gap_a)
                    y_coords.append(y_pos_gap_a)
                    y_coords.append(y_pos_align)
                x_coords.append(curr_x + x_size)
                x_coords.append(curr_x + x_size)
                y_coords.append(y_pos_align)
                y_coords.append(y_pos)
                for gap in j.gaps[::-1]:
                    x_coords.append(curr_x + gap[1] / x_scale)
                    x_coords.append(curr_x + gap[1] / x_scale)
                    x_coords.append(curr_x + gap[0] / x_scale)
                    x_coords.append(curr_x + gap[0] / x_scale)
                    y_coords.append(y_pos)
                    y_coords.append(y_pos_gap_b)
                    y_coords.append(y_pos_gap_b)
                    y_coords.append(y_pos)
                if j.gaps != [] and j.gaps[-1][1] == x_size:
                    x_coords = x_coords[:len(x_coords)/2-1] + x_coords[len(x_coords)/2+3:]
                    y_coords = y_coords[:len(y_coords)/2-1] + y_coords[len(y_coords)/2+3:]
                if j.gaps != [] and j.gaps[0][0] == 0:
                    x_coords = x_coords[3:-1]
                    y_coords = y_coords[3:-1]
                if j.snps != []:
                    freqList = [0 for burk in range(0, x_size_bp, bin_size)]
                    for snp in j.snps:
                        freqList[snp / bin_size] += 1
                    gradients = []
                    for burk, freqs in enumerate(freqList):
                        l = 0.6 - (min([max_snp, freqs]) * 1.0 / max_snp) * 0.1
                        gradients.append((burk * 100.0 / len(freqList) + 50.0/len(freqList), hsl_to_rgb(h, s, l)))
                    svg.drawGradient(gradient_count, gradients)
                    grad_id = gradient_count
                    gradient_count += 1
                else:
                    grad_id = None
                svg.drawAlignment(x_coords, y_coords, grad_id, 0, hsl_to_rgb(h,s,0.6))
            elif not j == 'break':
                if j.block_list == []:
                    pass
                else:
                    total_size =0
                    for k in j.block_list:
                        total_size += k[1]
                    if j.orient == 'middle':
                        gap_start = curr_x + x_size /2 - total_size/2/x_scale
                        gap_end = curr_x + x_size /2 + total_size/2/x_scale
                    elif j.orient == 'left':
                        gap_start = curr_x - 10
                        gap_end = curr_x + total_size / x_scale - 10
                    elif j.orient == 'right':
                        gap_start = curr_x + x_size - total_size / x_scale + 10
                        gap_end = curr_x + x_size + 10

                    svg.drawLine(gap_start, curr_y, gap_end, curr_y, genome_line_thick)
                    new_x = 0
                    for k in j.block_list:
                        if k[0] != 'na':
                            svg.drawStripedRect(gap_start + new_x / x_scale, curr_y-filler_block_width/2, k[1]/x_scale, filler_block_width, align_dict[k[0]][0], align_dict[k[0]][1], 2)
                        new_x += k[1]
        curr_x = sum(max_fill) / x_scale + fill_gap * num + max_x + 20
        for j in in_dict[i][1]:
            total_size =0
            for k in in_dict[i][1][j]:
                total_size += k[1]
            gap_start = curr_x
            gap_end = curr_x + total_size/x_scale
            svg.drawLine(gap_start, curr_y, gap_end, curr_y, genome_line_thick)
            new_x = 0
            for k in in_dict[i][1][j]:
                if k[0] != 'na':
                    svg.drawStripedRect(gap_start + new_x / x_scale, curr_y-filler_block_width/2, k[1]/x_scale, filler_block_width, align_dict[k[0]][0], align_dict[k[0]][1], 2)
                new_x += k[1]
            curr_x += total_size/x_scale + 20
        svg.writeString(i, curr_x, curr_y, 96)
    svg.drawLine(max_x, 100 + curr_y + conserved_thick, max_x + figure_width, 100 + curr_y + conserved_thick, 5)
    for num, j in enumerate(graph_list):
        curr_x = sum(max_fill[:num * 2]) / x_scale + fill_gap * num * 2 + max_x
        x_size = max_fill[num * 2] / x_scale
        y_pos = curr_y + conserved_thick
        try:
            x_gap = x_size * 1.0 / len(j)
        except:
            x_gap = 10
        xs = [curr_x + x_size, curr_x]
        ys = [y_pos, y_pos]
        for anum, freq in enumerate(j):
            xs.append(curr_x + anum * x_gap)
            xs.append(curr_x + anum * x_gap + x_gap)
            ys.append(freq * 1.0 / 20 * 200 + y_pos)
            ys.append(freq * 1.0 / 20 * 200 + y_pos)
        svg.drawPolygon(xs, ys)
    scale_bar_size = 250000
    gap_start = 100
    svg.drawLine(gap_start, 50, gap_start, 150, th=3)
    svg.drawLine(gap_start + scale_bar_size / x_scale, 50, gap_start + scale_bar_size / x_scale, 150, th=6)
    svg.drawLine(gap_start, 100, gap_start + scale_bar_size / x_scale, 100, th=6)
    svg.writeString(str(scale_bar_size) + ' bp', gap_start + scale_bar_size /2 / x_scale, 95, 72, justify='middle')
    svg.writesvg('testaburger.svg')







parser = ArgumentParser()
parser.add_argument("-o", "--output_svg", help="Create SVG here", metavar="FIGURE.SVG")
parser.add_argument("-m", "--mugsy_alignment", help="Mugsy alignment file", metavar="alignment.maf")
parser.add_argument("-c", "--color_tsv", default=None, help="tab seperated text file of string to match in strain name for grouping and color")
parser.add_argument("-t", "--tree_file", help="Tree in newick format.", metavar="tree.nw")
parser.add_argument("-a", "--min_alignment_size", help="Remove alignments smaller than this size", metavar="SIZE_BP", default=1000)
parser.add_argument("-d", "--working_dir", help="Working directory for peforming BLAST", metavar="DIR")
parser.add_argument("-f", "--fasta_files", help="List of fasta files - will glob argument (i.e. *.fa is a valid argument)", nargs='+', metavar="DIR")
parser.add_argument("-v", "--diff", help="List of difference files - will glob argument (i.e. *.fa is a valid argument)", nargs='+', metavar="DIR")
args = parser.parse_args()

var_dict = getGraphDict(args.diff)
genome_line_space = 150
order_list = draw_tree(args.tree_file, args.working_dir + '/tree.svg', args.color_tsv)
genome_line_dict = get_seq_dict(args.fasta_files)
read_mugsy(args.mugsy_alignment, genome_line_dict)
out_dict = get_block_coords(genome_line_dict, order_list[0])
graph_list = graphit(genome_line_dict, order_list[0], var_dict)
attached_to_place(out_dict)
draw_fig(out_dict, args.working_dir, order_list, graph_list)