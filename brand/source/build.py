import os, sys, importlib.util
spec = importlib.util.spec_from_file_location("gen", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen.py"))
g = importlib.util.module_from_spec(spec); sys.argv=[sys.argv[0], sys.argv[1]+"/_tmp"]; spec.loader.exec_module(g)
OUT = sys.argv[1].rsplit("/_tmp",1)[0]
def w(rel, s):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(s)
S = 512
TAG = "HACK · DETECT · LEARN"
# marks
w("svg/breach-avatar.svg", g.svg(S, S, g.mark_cut(S, radius=0, uid="av"), title="BREACH"))
w("svg/breach-mark.svg", g.svg(S, S, g.mark_cut(S), title="BREACH"))
w("svg/breach-mark-light.svg", g.svg(S, S, g.mark_cut(S, bg="#FFFFFF", fg=g.INK, red=g.RED_L, cyan=g.CYAN_L, glow=False, ghost=False, uid="ml"), title="BREACH"))
w("svg/breach-mark-transparent-dark-bg.svg", g.svg(S, S, g.mark_cut(S, with_bg=False, uid="mtd"), title="BREACH"))
w("svg/breach-mark-transparent-light-bg.svg", g.svg(S, S, g.mark_cut(S, with_bg=False, fg=g.INK, red=g.RED_L, cyan=g.CYAN_L, ghost=False, uid="mtl"), title="BREACH"))
w("svg/favicon.svg", g.svg(S, S, g.mark_cut(S, glow=False, ghost=False, uid="fv"), title="BREACH"))
# wordmarks (transparent)
W,H,b = g.wordmark_cut(200, uid="wd"); w("svg/breach-wordmark-dark-bg.svg", g.svg(W,H,b))
W,H,b = g.wordmark_cut(200, fg=g.INK, red=g.RED_L, cyan=g.CYAN_L, ghost=False, uid="wl"); w("svg/breach-wordmark-light-bg.svg", g.svg(W,H,b))
W,H,b = g.wordmark_cut(200, uid="wtd", tagline=TAG); w("svg/breach-wordmark-tagline-dark-bg.svg", g.svg(W,H,b))
W,H,b = g.wordmark_cut(200, fg=g.INK, red=g.RED_L, cyan=g.CYAN_L, ghost=False, uid="wtl", tagline=TAG, tag_col="#4A5670"); w("svg/breach-wordmark-tagline-light-bg.svg", g.svg(W,H,b))
# social preview 1280x640
W,H,b = g.wordmark_cut(170, uid="sp", tagline=TAG)
sx, sy = (1280-W)/2, (640-H)/2 - 10
url_d, uw, _ = g.text_path(g.JB, "github.com/breach-game", 18, tracking=0.15)
url_d, uw, _ = g.text_path(g.JB, "github.com/breach-game", 18, x=(1280-uw)/2, y=590, tracking=0.15)
bg = ('<defs><pattern id="sl" width="8" height="4" patternUnits="userSpaceOnUse"><rect width="8" height="1" fill="#fff" opacity="0.03"/></pattern>'
      '<radialGradient id="gl" cx="50%" cy="48%" r="60%"><stop offset="0" stop-color="#FF3D5A" stop-opacity="0.14"/><stop offset="1" stop-color="#FF3D5A" stop-opacity="0"/></radialGradient></defs>'
      '<rect width="1280" height="640" fill="#07090F"/><rect width="1280" height="640" fill="url(#gl)"/><rect width="1280" height="640" fill="url(#sl)"/>')
w("svg/social-preview.svg", g.svg(1280, 640, bg + f'<g transform="translate({sx} {sy})">{b}</g><path fill="#6B7A99" d="{url_d}"/>'))
