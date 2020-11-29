import argparse
import random

from PIL import Image

def probability(prob):
    return random.random() < prob

def main():
    skeleton_xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   id="svg2"
   version="1.1"
   width="%(width)i"
   height="%(height)i"
   viewBox="0 0 %(vb_width)i %(vb_height)i">
  <metadata
     id="metadata8">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <rect
     id="background"
     x="0"
     y="0"
     height="%(vb_height)i"
     width="%(vb_width)i"
     style="opacity: 1; fill: #%(background_color)s;" />
     %(data)s
</svg>"""

    pixel_xml = """  <g
     id="pixel-%(row)i-%(col)i"
     transform="translate(%(xpos)i, %(ypos)i)">
    <circle
       id="peg-active"
       cx="89"
       cy="483"
       r="50"
       style="opacity: 1; fill: #%(active_peg_color)s;" />
    <circle
       id="peg-inactive"
       cx="484"
       cy="88"
       r="50"
       style="opacity: 1; fill: #%(inactive_peg_color)s;" />
    <rect
       id="axis"
       x="85"
       y="-17"
       height="34"
       width="640"
       transform="matrix(0.707,0.707,-0.707,0.707,0,0)"
       style="opacity: 1; fill: #%(axis_color)s;" />
    <path
       id="flipdot-inactive"
       d="m 163,65 c -48,47 -97,94 -145,141 0,67 0,133 0,200 48,47 96,94 145,141 68,0 136,0 205,0 48,-47 97,-94 145,-141 0,-67 0,-133 0,-200 -7,-7 -14,-14 -22,-21 -57,11 -114,-43 -106,-101 -1,-8 -12,-13 -17,-19 -68,0 -136,0 -205,0 z"
       style="opacity: %(inactive)i; fill: #%(inactive_color)s;" />
    <path
       id="flipdot-active"
       d="m 409,507 c 48,-47 97,-94 145,-141 0,-67 0,-133 0,-200 -48,-47 -96,-94 -145,-141 -68,0 -136,0 -205,0 -48,47 -97,94 -145,141 0,67 0,133 0,200 7,7 14,14 22,21 57,-11 114,43 106,101 1,8 12,13 17,19 68,0 136,0 205,0 z"
       style="opacity: %(active)i; fill: #%(active_color)s;" />
    <path
       id="support-top-left"
       d="m 147,0 -147,147 0,-147 z"
       style="opacity: 1; fill: #%(support_color)s;" />
    <path
       id="support-bottom-right"
       d="m 425,572 147,-147 0,147 z"
       style="opacity: 1; fill: #%(support_color)s;" />
  </g>"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-mw', '--matrix-width', type = int, required = True)
    parser.add_argument('-mh', '--matrix-height', type = int, required = True)
    parser.add_argument('-ic', '--inactive-color', type = str, required = False, default = "cdcfcc")
    parser.add_argument('-ac', '--active-color', type = str, required = False, default = "544548")
    parser.add_argument('-sc', '--support-color', type = str, required = False, default = "bbad89")
    parser.add_argument('-axc', '--axis-color', type = str, required = False, default = "373737")
    parser.add_argument('-ipc', '--inactive-peg-color', type = str, required = False, default = "544548")
    parser.add_argument('-apc', '--active-peg-color', type = str, required = False, default = "373737")
    parser.add_argument('-bc', '--background-color', type = str, required = False, default = "777777")
    parser.add_argument('-if', '--image-file', type = argparse.FileType('rb'), required = False)
    parser.add_argument('-dpr', '--dead-pixel-ratio', type = float, required = False, default = 0.0)
    args = parser.parse_args()

    if args.image_file:
        img = Image.open(args.image_file).convert('L') # Convert to grayscale
        pixels = img.load()

    data = ""
    for m in range(args.matrix_height):
        for n in range(args.matrix_width):
            pixel_data = {
                'row': m,
                'col': n,
                'xpos': n * 572,
                'ypos': m * 572,
                'inactive': 1,
                'active': 0,
                'inactive_color': args.inactive_color,
                'active_color': args.active_color,
                'support_color': args.support_color,
                'axis_color': args.axis_color,
                'inactive_peg_color': args.inactive_peg_color,
                'active_peg_color': args.active_peg_color
            }

            if args.image_file:
                pixel_data['active'] = pixels[n, m] < 128
                pixel_data['inactive'] = not pixel_data['active']

            if args.dead_pixel_ratio:
                if probability(args.dead_pixel_ratio):
                    # Flip random pixels to simulate faulty flipdots
                    pixel_data['active'] = not pixel_data['active']
                    pixel_data['inactive'] = not pixel_data['inactive']

            data += pixel_xml % pixel_data

    print(skeleton_xml % {
        'data': data,
        'width': args.matrix_width * 572 / 25,
        'height': args.matrix_height * 572 / 25,
        'vb_width': args.matrix_width * 572,
        'vb_height': args.matrix_height * 572,
        'background_color': args.background_color
    })

if __name__ == "__main__":
    main()