#!/usr/bin/env python3
"""Generate the saddle-pad textures for edoras_horse.

The pad is rendered as a colorised overlay on the BODY texture layer (layer 2 of
the 3-layer set in init.lua refresh_textures): a white mask is composited onto the
coat with `^[multiply:#rrggbb` at equip time, so one mask serves every dye colour.

The mask is built from the mesh itself: we select the torso faces in a band around
the saddle (behind the withers, in front of the croup) from the back-top down the
upper flanks -- excluding the belly -- and paint each selected triangle's UV
polygon. That makes the pad sit flat on the back AND come down the sides a little,
correctly aligned to the body unwrap no matter how the mesh is unwrapped.

Tunables (BAND / Y_DOWN / NY_BELLY) are how you reshape the pad after eyeballing it
in-game: edit, re-run, redeploy. Head is at +z (zmax), tail at -z (zmin).

Outputs (128x128 RGBA):
  textures/edoras_horse_saddlepad.png       -- white body mask (multiply target)
  textures/edoras_horse_saddlepad_item.png  -- 16x16 white inventory icon
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MOD  = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import b3d
from PIL import Image, ImageDraw, ImageFilter

PATH = os.path.join(MOD, "models", "edoras_horse.b3d")
OUT_MASK = os.path.join(MOD, "textures", "edoras_horse_saddlepad.png")
OUT_ICON = os.path.join(MOD, "textures", "edoras_horse_saddlepad_item.png")

# --- pad footprint tunables (mesh units; head=+z, tail=-z, up=+y) ---
Z_LO, Z_HI = -2.8, 2.8     # front-to-back extent (saddle band, behind the withers)
Y_DOWN     = 4.3           # lowest y painted -> how far down the flanks it drapes
NY_BELLY   = -0.55         # drop faces pointing more steeply down than this (belly)


def _ci(b, o): return struct.unpack('<i', b[o:o+4])[0]
def _cf(b, o): return struct.unpack('<f', b[o:o+4])[0]


def load_mesh(payload):
    p, vrts, tris = 4, None, []
    while p + 8 <= len(payload):
        tag = payload[p:p+4]; ln = _ci(payload, p+4); body = p+8; nend = body+ln
        if tag == b'VRTS': vrts = payload[body:nend]
        elif tag == b'TRIS': tris.append(payload[body:nend])
        p = nend
    flags = _ci(vrts, 0); tcs = _ci(vrts, 4); tcss = _ci(vrts, 8)
    stride = 3 + (3 if flags & 1 else 0) + (4 if flags & 2 else 0) + tcs*tcss
    vcount = (len(vrts) - 12)//(stride*4)
    uvbase = (3 + (3 if flags & 1 else 0) + (4 if flags & 2 else 0))*4
    V = []
    for i in range(vcount):
        base = 12 + i*stride*4
        V.append((_cf(vrts, base), _cf(vrts, base+4), _cf(vrts, base+8),
                  _cf(vrts, base+uvbase), _cf(vrts, base+uvbase+4)))
    F = []
    for tp in tris:
        n = (len(tp)-4)//12
        for i in range(n):
            F.append((_ci(tp, 4+i*12), _ci(tp, 4+i*12+4), _ci(tp, 4+i*12+8)))
    return V, F


def main():
    _, top = b3d.parse(PATH)
    meshes = []
    def rec(o):
        if isinstance(o, b3d.Node):
            for c in o.children:
                if isinstance(c, b3d.Chunk):
                    if c.tag == b'MESH': meshes.append(c.payload)
                else: rec(c)
    for o in top:
        if isinstance(o, b3d.Node): rec(o)
    # mesh[1] is the main body layer (mesh[0]=chest boxes, mesh[2]=saddle).
    V, F = load_mesh(meshes[1])

    def cross(u, v): return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

    mask = Image.new('L', (128, 128), 0)
    d = ImageDraw.Draw(mask)
    n = 0
    for a, b, c in F:
        pa, pb, pc = V[a][:3], V[b][:3], V[c][:3]
        cz = (pa[2]+pb[2]+pc[2])/3; cy = (pa[1]+pb[1]+pc[1])/3
        if not (Z_LO <= cz <= Z_HI) or cy < Y_DOWN:
            continue
        nx, ny, nz = cross(sub(pb, pa), sub(pc, pa))
        m = (nx*nx+ny*ny+nz*nz)**0.5
        if m and ny/m < NY_BELLY:
            continue
        d.polygon([(V[a][3]*128, V[a][4]*128), (V[b][3]*128, V[b][4]*128),
                   (V[c][3]*128, V[c][4]*128)], fill=255)
        n += 1
    mask = mask.filter(ImageFilter.MaxFilter(3))  # close seams between triangles
    rgba = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    white = Image.new('RGBA', (128, 128), (255, 255, 255, 255))
    rgba.paste(white, (0, 0), mask)
    rgba.save(OUT_MASK)
    print("wrote", OUT_MASK, "(%d torso tris)" % n)

    # Inventory icon: a small white folded-blanket shape (border a touch darker so
    # the colorised result reads as cloth, not a flat square).
    icon = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    di = ImageDraw.Draw(icon)
    di.rectangle([2, 4, 13, 12], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255))
    di.line([2, 7, 13, 7], fill=(210, 210, 210, 255))
    di.line([2, 10, 13, 10], fill=(210, 210, 210, 255))
    icon.save(OUT_ICON)
    print("wrote", OUT_ICON)


if __name__ == "__main__":
    main()
