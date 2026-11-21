"""Generate BREACH brand SVGs with text converted to paths (no font dependency)."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SG = TTFont(os.path.join(HERE, "fonts/SpaceGrotesk-Bold.ttf"))
JB = TTFont(os.path.join(HERE, "fonts/JBM-Medium.ttf"))

NIGHT = "#07090F"
RED = "#FF3D5A"
CYAN = "#2DE2FF"
WHITE = "#FFFFFF"
TEXT2 = "#6B7A99"
# light-mode equivalents (AA on white)
INK = "#07090F"
RED_L = "#E5173A"
CYAN_L = "#0092B3"


def text_path(font, text, size, x=0, y=0, tracking=0.0):
    """Return (d, width, (xmin,ymin,xmax,ymax)) for text, baseline at y."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    bp = BoundsPen(gs)
    cx = 0
    names = [cmap[ord(c)] for c in text]
    for i, n in enumerate(names):
        t = (s, 0, 0, -s, x + cx * s, y)
        gs[n].draw(TransformPen(pen, t))
        gs[n].draw(TransformPen(bp, t))
        cx += gs[n].width
        if i < len(names) - 1:
            cx += tracking * upm
    return pen.getCommands(), cx * s, bp.bounds


def glitch_word(d, bbox, cut_bands, ghost=8, fg=WHITE, red=RED, cyan=CYAN, uid="g"):
    """Word with red/cyan chromatic ghosts and horizontally displaced slices.
    cut_bands: list of (y0, y1, dx) in absolute coords."""
    xmin, ymin, xmax, ymax = bbox
    out = [f'<defs>']
    # clip for un-shifted parts: everything except bands
    ys = sorted([(b[0], b[1]) for b in cut_bands])
    keep = []
    prev = ymin - 50
    for y0, y1 in ys:
        keep.append((prev, y0))
        prev = y1
    keep.append((prev, ymax + 50))
    out.append(f'<clipPath id="{uid}-keep">' + "".join(
        f'<rect x="{xmin-200}" y="{a}" width="{xmax-xmin+400}" height="{b-a}"/>' for a, b in keep) + '</clipPath>')
    for i, (y0, y1, dx) in enumerate(cut_bands):
        out.append(f'<clipPath id="{uid}-b{i}"><rect x="{xmin-200}" y="{y0}" width="{xmax-xmin+400}" height="{y1-y0}"/></clipPath>')
    out.append('</defs>')

    def layer(fill, ox):
        parts = [f'<g clip-path="url(#{uid}-keep)"><path transform="translate({ox} 0)" fill="{fill}" d="{d}"/></g>']
        for i, (y0, y1, dx) in enumerate(cut_bands):
            parts.append(f'<g clip-path="url(#{uid}-b{i})"><path transform="translate({ox+dx} 0)" fill="{fill}" d="{d}"/></g>')
        return "".join(parts)

    out.append(f'<g opacity="0.95">{layer(red, -ghost)}</g>')
    out.append(f'<g opacity="0.95">{layer(cyan, ghost)}</g>')
    out.append(layer(fg, 0))
    return "".join(out)


def svg(w, h, body, bg=None, title="BREACH"):
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{bgr}{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


# ---------------------------------------------------------------- Direction A: glitch "B" mark
def mark_glitch_b(size=512, bg=NIGHT, fg=WHITE, red=RED, cyan=CYAN, rounded=True, uid="mb", with_bg=True, scanlines=True):
    fs = size * 0.78
    d, w, bb = text_path(SG, "B", fs)
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    ox = (size - gw) / 2 - bb[0]
    oy = (size - gh) / 2 - bb[1]
    d, w, bb = text_path(SG, "B", fs, x=ox, y=oy)
    h = bb[3] - bb[1]
    bands = [
        (bb[1] + h * 0.30, bb[1] + h * 0.40, size * 0.055),
        (bb[1] + h * 0.62, bb[1] + h * 0.68, -size * 0.035),
    ]
    body = ""
    if with_bg:
        r = size * 0.22 if rounded else 0
        body += f'<rect width="{size}" height="{size}" rx="{r}" fill="{bg}"/>'
        if scanlines:
            body += (f'<defs><pattern id="{uid}-sl" width="4" height="{size/128}" patternUnits="userSpaceOnUse">'
                     f'<rect width="4" height="{size/256}" fill="#FFFFFF" opacity="0.035"/></pattern>'
                     f'<radialGradient id="{uid}-glow" cx="50%" cy="50%" r="55%"><stop offset="0" stop-color="{red}" stop-opacity="0.22"/>'
                     f'<stop offset="1" stop-color="{red}" stop-opacity="0"/></radialGradient></defs>'
                     f'<rect width="{size}" height="{size}" rx="{r}" fill="url(#{uid}-glow)"/>'
                     f'<rect width="{size}" height="{size}" rx="{r}" fill="url(#{uid}-sl)"/>')
    body += glitch_word(d, bb, bands, ghost=size * 0.018, fg=fg, red=red, cyan=cyan, uid=uid)
    # terminal cursor block, red, bottom-right
    cw, ch = size * 0.085, size * 0.03
    body += f'<rect x="{bb[2] + size*0.03}" y="{bb[3]-ch}" width="{cw}" height="{ch}" fill="{red}"/>'
    return body


# ---------------------------------------------------------------- Direction B: breached perimeter
def mark_perimeter(size=512, bg=NIGHT, fg=WHITE, red=RED, cyan=CYAN, uid="mp", with_bg=True):
    import math
    c = size / 2
    R = size * 0.33
    body = ""
    if with_bg:
        body += (f'<defs><radialGradient id="{uid}-glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{cyan}" stop-opacity="0.16"/>'
                 f'<stop offset="1" stop-color="{cyan}" stop-opacity="0"/></radialGradient></defs>'
                 f'<rect width="{size}" height="{size}" rx="{size*0.22}" fill="{bg}"/>'
                 f'<rect width="{size}" height="{size}" rx="{size*0.22}" fill="url(#{uid}-glow)"/>')
    pts = [(c + R * math.cos(math.radians(-90 + 60 * i)), c + R * math.sin(math.radians(-90 + 60 * i))) for i in range(6)]
    sw = size * 0.035
    # edges: all cyan except edge 0->1 (top-right) which is broken
    for i in range(6):
        a, b = pts[i], pts[(i + 1) % 6]
        if i == 0:
            # broken edge: two stubs
            t = 0.28
            p1 = (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)
            p2 = (b[0] + (a[0]-b[0])*t, b[1] + (a[1]-b[1])*t)
            body += f'<line x1="{a[0]}" y1="{a[1]}" x2="{p1[0]}" y2="{p1[1]}" stroke="{cyan}" stroke-width="{sw}" stroke-linecap="round"/>'
            body += f'<line x1="{b[0]}" y1="{b[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{cyan}" stroke-width="{sw}" stroke-linecap="round"/>'
        else:
            body += f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{cyan}" stroke-width="{sw}" stroke-linecap="round"/>'
    # red intrusion arrow from outside top-right through gap into centre
    gap = ((pts[0][0]+pts[1][0])/2, (pts[0][1]+pts[1][1])/2)
    vx, vy = gap[0]-c, gap[1]-c
    L = math.hypot(vx, vy); ux, uy = vx/L, vy/L
    start = (c + ux * size * 0.47, c + uy * size * 0.47)
    end = (c + ux * size * 0.02, c + uy * size * 0.02)
    body += f'<line x1="{start[0]}" y1="{start[1]}" x2="{end[0]}" y2="{end[1]}" stroke="{red}" stroke-width="{sw*1.3}" stroke-linecap="round"/>'
    # chevron head at end
    px, py = -uy, ux
    hl = size * 0.09
    h1 = (end[0] + ux*hl + px*hl*0.8, end[1] + uy*hl + py*hl*0.8)
    h2 = (end[0] + ux*hl - px*hl*0.8, end[1] + uy*hl - py*hl*0.8)
    body += f'<polyline points="{h1[0]},{h1[1]} {end[0]},{end[1]} {h2[0]},{h2[1]}" fill="none" stroke="{red}" stroke-width="{sw*1.3}" stroke-linecap="round" stroke-linejoin="round"/>'
    # nodes
    for i, (x, y) in enumerate(pts):
        col = red if i in (0, 1) else cyan
        body += f'<circle cx="{x}" cy="{y}" r="{size*0.04}" fill="{bg if with_bg else "none"}" stroke="{col}" stroke-width="{sw*0.8}"/>'
    body += f'<circle cx="{c}" cy="{c}" r="{size*0.03}" fill="{red}"/>'
    return body


# ---------------------------------------------------------------- Direction C: prompt monogram
def mark_prompt(size=512, bg=NIGHT, fg=WHITE, red=RED, cyan=CYAN, uid="mc", with_bg=True):
    body = ""
    if with_bg:
        body += f'<rect width="{size}" height="{size}" rx="{size*0.22}" fill="{bg}"/>'
        body += f'<rect x="{size*0.04}" y="{size*0.04}" width="{size*0.92}" height="{size*0.92}" rx="{size*0.19}" fill="none" stroke="{cyan}" stroke-opacity="0.35" stroke-width="{size*0.008}"/>'
    sw = size * 0.07
    # chevron
    x0, y0 = size * 0.20, size * 0.33
    body += f'<polyline points="{x0},{y0} {x0+size*0.17},{size*0.5} {x0},{size*0.67}" fill="none" stroke="{red}" stroke-width="{sw}" stroke-linecap="square" stroke-linejoin="miter"/>'
    d, w, bb = text_path(SG, "B", size * 0.46)
    gh = bb[3] - bb[1]
    d, w, bb = text_path(SG, "B", size * 0.46, x=size * 0.47 - bb[0], y=size * 0.5 + gh / 2)
    body += f'<path fill="{fg}" d="{d}"/>'
    body += f'<rect x="{bb[2]+size*0.04}" y="{bb[3]-size*0.06}" width="{size*0.1}" height="{size*0.06}" fill="{cyan}"/>'
    return body


# ---------------------------------------------------------------- Wordmark (glitch), shared
def wordmark(fs=200, fg=WHITE, red=RED, cyan=CYAN, bg=None, pad=None, uid="wm", tagline=None, tag_col=TEXT2):
    track = 0.12
    d, w, bb = text_path(SG, "BREACH", fs, tracking=track)
    pad = pad if pad is not None else fs * 0.35
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    W = gw + 2 * pad
    tag_h = fs * 0.32 if tagline else 0
    H = gh + 2 * pad + tag_h
    d, w, bb = text_path(SG, "BREACH", fs, x=pad - bb[0], y=pad - bb[1], tracking=track)
    h = bb[3] - bb[1]
    bands = [
        (bb[1] + h * 0.22, bb[1] + h * 0.30, fs * 0.05),
        (bb[1] + h * 0.58, bb[1] + h * 0.66, -fs * 0.04),
    ]
    body = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    body += glitch_word(d, bb, bands, ghost=fs * 0.022, fg=fg, red=red, cyan=cyan, uid=uid)
    if tagline:
        tfs = fs * 0.12
        td, tw, tbb = text_path(JB, tagline, tfs, tracking=0.35)
        tx = (W - tw) / 2
        td, tw, tbb = text_path(JB, tagline, tfs, x=tx, y=bb[3] + fs * 0.32, tracking=0.35)
        body += f'<path fill="{tag_col}" d="{td}"/>'
    return W, H, body


if __name__ == "__main__":
    # direction exploration board pieces
    S = 512
    write("explore-A-glitch.svg", svg(S, S, mark_glitch_b(S)))
    write("explore-B-perimetre.svg", svg(S, S, mark_perimeter(S)))
    write("explore-C-prompt.svg", svg(S, S, mark_prompt(S)))
    W, H, b = wordmark(200, bg=NIGHT)
    write("explore-wordmark.svg", svg(W, H, b))


# ---------------------------------------------------------------- v2: "cut" style (one clean breach line)
def cut_word(d, bb, cut_y, gap, dx, fg, red, uid, beam=True, beam_x0=None, beam_x1=None, ghost=0, cyan=None):
    xmin, ymin, xmax, ymax = bb
    top = f'<clipPath id="{uid}-t"><rect x="{xmin-500}" y="{ymin-100}" width="{xmax-xmin+1000}" height="{cut_y-gap/2-ymin+100}"/></clipPath>'
    bot = f'<clipPath id="{uid}-b"><rect x="{xmin-500}" y="{cut_y+gap/2}" width="{xmax-xmin+1000}" height="{ymax-cut_y+100}"/></clipPath>'
    out = f'<defs>{top}{bot}</defs>'
    if ghost and cyan:
        # thin chromatic fringe only on the shifted top half
        out += f'<g clip-path="url(#{uid}-t)"><path transform="translate({dx-ghost} 0)" fill="{red}" opacity="0.9" d="{d}"/><path transform="translate({dx+ghost} 0)" fill="{cyan}" opacity="0.9" d="{d}"/></g>'
    out += f'<g clip-path="url(#{uid}-t)"><path transform="translate({dx} 0)" fill="{fg}" d="{d}"/></g>'
    out += f'<g clip-path="url(#{uid}-b)"><path fill="{fg}" d="{d}"/></g>'
    if beam:
        x0 = beam_x0 if beam_x0 is not None else xmin
        x1 = beam_x1 if beam_x1 is not None else xmax
        bh = gap * 0.45
        out += (f'<defs><linearGradient id="{uid}-beam" x1="0" x2="1"><stop offset="0" stop-color="{red}" stop-opacity="0"/>'
                f'<stop offset="0.25" stop-color="{red}"/><stop offset="1" stop-color="{red}"/></linearGradient></defs>'
                f'<rect x="{x0}" y="{cut_y-bh/2}" width="{x1-x0}" height="{bh}" fill="url(#{uid}-beam)"/>')
    return out


def mark_cut(size=512, bg=NIGHT, fg=WHITE, red=RED, cyan=CYAN, uid="mk", with_bg=True, glow=True, ghost=True, radius=0.22):
    fs = size * 0.80
    d, w, bb = text_path(SG, "B", fs)
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    ox = (size - gw) / 2 - bb[0] - size * 0.045
    oy = (size - gh) / 2 - bb[1]
    d, w, bb = text_path(SG, "B", fs, x=ox, y=oy)
    h = bb[3] - bb[1]
    body = ""
    r = size * radius
    if with_bg:
        body += f'<rect width="{size}" height="{size}" rx="{r}" fill="{bg}"/>'
        if glow:
            body += (f'<defs><radialGradient id="{uid}-glow" cx="58%" cy="56%" r="60%"><stop offset="0" stop-color="{red}" stop-opacity="0.20"/>'
                     f'<stop offset="1" stop-color="{red}" stop-opacity="0"/></radialGradient></defs>'
                     f'<rect width="{size}" height="{size}" rx="{r}" fill="url(#{uid}-glow)"/>')
    cut_y = bb[1] + h * 0.56
    body += cut_word(d, bb, cut_y, gap=size * 0.04, dx=size * 0.05, fg=fg, red=red, uid=uid,
                     beam_x0=size * 0.08, beam_x1=bb[2] + size * 0.05, ghost=size * 0.012 if ghost else 0, cyan=cyan)
    # cursor
    body += f'<rect x="{bb[2] + size*0.07}" y="{bb[3]-size*0.045}" width="{size*0.1}" height="{size*0.045}" fill="{cyan}"/>'
    return body


def wordmark_cut(fs=200, fg=WHITE, red=RED, cyan=CYAN, bg=None, uid="wc", tagline=None, tag_col=TEXT2, ghost=True):
    track = 0.12
    d, w, bb = text_path(SG, "BREACH", fs, tracking=track)
    padx, pady = fs * 0.45, fs * 0.35
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    W = gw + 2 * padx + fs * 0.05
    tag_h = fs * 0.32 if tagline else 0
    H = gh + 2 * pady + tag_h
    d, w, bb = text_path(SG, "BREACH", fs, x=padx - bb[0], y=pady - bb[1], tracking=track)
    h = bb[3] - bb[1]
    body = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    cut_y = bb[1] + h * 0.56
    body += cut_word(d, bb, cut_y, gap=fs * 0.05, dx=fs * 0.06, fg=fg, red=red, uid=uid,
                     beam_x0=padx * 0.25, beam_x1=W - padx * 0.25, ghost=fs * 0.014 if ghost else 0, cyan=cyan)
    if tagline:
        tfs = fs * 0.11
        td, tw, tbb = text_path(JB, tagline, tfs, tracking=0.4)
        tx = (W - tw) / 2
        td, tw, tbb = text_path(JB, tagline, tfs, x=tx, y=bb[3] + fs * 0.34, tracking=0.4)
        body += f'<path fill="{tag_col}" d="{td}"/>'
    return W, H, body


if __name__ == "__main__":
    S = 512
    write("v2-mark.svg", svg(S, S, mark_cut(S)))
    W, H, b = wordmark_cut(200, bg=NIGHT, tagline="HACK  ·  DETECT  ·  LEARN")
    write("v2-wordmark.svg", svg(W, H, b))
    W, H, b = wordmark_cut(200, bg="#FFFFFF", fg=INK, red=RED_L, cyan=CYAN_L, ghost=False, uid="wl")
    write("v2-wordmark-light.svg", svg(W, H, b))
    write("v2-mark-nobg.svg", svg(S, S, mark_cut(S, with_bg=False, uid="mn")))
