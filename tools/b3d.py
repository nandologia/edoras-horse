"""Minimal Blitz3D (.b3d) reader/writer for animation editing.

We recurse only into NODE chunks (the scene graph); every other chunk
(TEXS, BRUS, MESH, BONE, KEYS, ANIM, ...) is kept as an opaque blob so a
parse -> serialize round-trip is byte-exact. KEYS/ANIM are edited by
locating them in the tree and replacing their payloads.
"""
import struct

def _ci(b, o): return struct.unpack('<i', b[o:o+4])[0]

class Node:
    __slots__ = ('header', 'children')  # header = name+pos+scale+rot bytes
    def __init__(self, header, children):
        self.header = header; self.children = children

class Chunk:
    __slots__ = ('tag', 'payload')      # opaque
    def __init__(self, tag, payload):
        self.tag = tag; self.payload = payload

def _parse_node_payload(b, o, end):
    # name (null-terminated) + 3f pos + 3f scale + 4f rot, then child chunks
    e = b.index(b'\x00', o)
    hdr_end = e + 1 + 40
    header = b[o:hdr_end]
    children = []
    p = hdr_end
    while p + 8 <= end:
        tag = b[p:p+4]; ln = _ci(b, p+8-4)
        body = p+8; nend = body+ln
        if tag == b'NODE':
            children.append(_parse_node_payload(b, body, nend))
        else:
            children.append(Chunk(tag, b[body:nend]))
        p = nend
    return Node(header, children)

def parse(path):
    b = open(path, 'rb').read()
    assert b[:4] == b'BB3D', b[:4]
    total = _ci(b, 4)
    ver = _ci(b, 8)
    top = []
    p = 12
    end = 8 + total
    while p + 8 <= end:
        tag = b[p:p+4]; ln = _ci(b, p+4)
        body = p+8; nend = body+ln
        if tag == b'NODE':
            top.append(_parse_node_payload(b, body, nend))
        else:
            top.append(Chunk(tag, b[body:nend]))
        p = nend
    return ver, top

def _ser(obj):
    if isinstance(obj, Node):
        pay = obj.header + b''.join(_ser(c) for c in obj.children)
        return b'NODE' + struct.pack('<i', len(pay)) + pay
    else:
        return obj.tag + struct.pack('<i', len(obj.payload)) + obj.payload

def write(path, ver, top):
    pay = struct.pack('<i', ver) + b''.join(_ser(o) for o in top)
    data = b'BB3D' + struct.pack('<i', len(pay)) + pay
    open(path, 'wb').write(data)
    return len(data)

def node_name(node):
    return node.header.split(b'\x00', 1)[0].decode('latin1')
