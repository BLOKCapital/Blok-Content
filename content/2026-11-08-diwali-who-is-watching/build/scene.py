# Blender 4.2 scene builder + renderer for "Who's watching your money this Diwali?"
# usage: blender -b -P scene.py -- --aspect 16x9|9x16 --scenes A,B --scale 0.6667 --samples 16 --out frames16/ [--preview t1,t2]
import bpy, bmesh, math, json, random, sys, os
from mathutils import Vector, Euler

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def arg(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d
ASPECT = arg('--aspect', '16x9'); VERT = ASPECT == '9x16'
SCALE = float(arg('--scale', '0.6667')); SAMPLES = int(arg('--samples', '16'))
OUT = arg('--out', '/tmp/frames/'); ONLY = arg('--scenes'); PREVIEW = arg('--preview')
STEP = int(arg('--step', '1'))
FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FONT_X = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
LOGO = os.path.join(HERE, 'logo-wordmark.png')

# ---------- timing from the voice timeline ----------
TL = None
p = os.path.join(HERE, 'timeline.js')
if os.path.exists(p):
    TL = json.loads(open(p).read().split('=', 1)[1].rstrip(';\n '))
EST = [(0.25, 4.6), (4.95, 6.9), (7.35, 15.8), (16.2, 19.9), (20.45, 27.4), (27.85, 33.6), (34.1, 37.2),
       (37.9, 45.3), (45.75, 50.0), (50.45, 53.0), (53.55, 58.0)]
def LS(i): return TL[i]['start'] if TL else EST[i][0]
def LE(i): return TL[i]['end'] if TL else EST[i][1]
def W(i, word, nth=0):
    """start time of a word (case-insensitive prefix match) in line i"""
    if not TL: return LS(i) + 0.5
    hits = [w for w in TL[i]['words'] if w['w'].lower().strip('.,?$!').startswith(word.lower())]
    return hits[min(nth, len(hits) - 1)]['s'] if hits else LS(i)
END = LE(10) + 2.4
CUT = lambda i: max(0.0, LS(i) - 0.12)
SCENES = [('A', 0.0, CUT(2)), ('B', CUT(2), CUT(3)), ('C', CUT(3), CUT(4)), ('D', CUT(4), CUT(5)),
          ('E', CUT(5), CUT(7)), ('G', CUT(7), CUT(9)), ('I', CUT(9), CUT(10)), ('J', CUT(10), END)]
F = lambda t: int(round(t * FPS)) + 1

# ---------- reset ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
S.render.fps = FPS
random.seed(7)

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*c, a)
SKY, INDIGO, LIME, LINEN, CORAL, BROWN = '#7DD2FD', '#004EBA', '#7ED116', '#F6F3E8', '#EC464D', '#844947'
GOLD = '#F5B841'; FLAME = '#FF9A2E'

MATS = {}
def mat(name, color='#888888', rough=0.5, metal=0.0, emit=None, es=0.0, trans=0.0, alpha=1.0, ior=1.45):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexc(color)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['IOR'].default_value = ior
    if trans: b.inputs['Transmission Weight'].default_value = trans
    if emit:
        b.inputs['Emission Color'].default_value = hexc(emit); b.inputs['Emission Strength'].default_value = es
    if alpha < 1: b.inputs['Alpha'].default_value = alpha
    MATS[name] = m; return m

def emat(name, color, strength):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = hexc(color); e.inputs['Strength'].default_value = strength
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0])
    MATS[name] = m; return m

def img_mat(name, path, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(path)
    nt.links.new(t.outputs['Color'], b.inputs['Base Color']); nt.links.new(t.outputs['Alpha'], b.inputs['Alpha'])
    b.inputs['Roughness'].default_value = 0.6
    if emit:
        nt.links.new(t.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = emit
    return m

COLL = {}
CUR = [None]
def scene_coll(name):
    c = bpy.data.collections.new('S_' + name); S.collection.children.link(c); COLL[name] = c; CUR[0] = c; return c
def link(o):
    for c in o.users_collection: c.objects.unlink(o)
    CUR[0].objects.link(o); return o

def box(loc, size, m, bevel=0.0, name='box'):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2); bpy.ops.object.transform_apply(scale=True)
    if bevel:
        md = o.modifiers.new('bv', 'BEVEL'); md.width = bevel; md.segments = 3
    o.data.materials.append(m); return link(o)
def cyl(loc, r, d, m, verts=32, rot=(0, 0, 0), name='cyl'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object; o.name = name
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return link(o)
def sph(loc, r, m, seg=24, name='sph'):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc); o = bpy.context.object; o.name = name
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return link(o)
def ico(loc, r, m):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=loc); o = bpy.context.object
    o.data.materials.append(m); return link(o)
def plane(loc, w, h, m, rot=(0, 0, 0), name='plane'):
    bpy.ops.mesh.primitive_plane_add(location=loc, rotation=rot); o = bpy.context.object; o.name = name
    o.scale = (w / 2, h / 2, 1); bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); return link(o)
FONTS = {}
def text(body, loc, size, m, extrude=0.06, rot=(math.radians(90), 0, 0), font=FONT_B, bevel=0.01, align='CENTER'):
    if font not in FONTS: FONTS[font] = bpy.data.fonts.load(font)
    cu = bpy.data.curves.new('t', 'FONT'); cu.body = body; cu.font = FONTS[font]; cu.size = size
    cu.extrude = extrude; cu.bevel_depth = bevel; cu.bevel_resolution = 2; cu.align_x = align; cu.align_y = 'CENTER'
    o = bpy.data.objects.new('txt', cu); o.location = loc; o.rotation_euler = rot; cu.materials.append(m)
    CUR[0].objects.link(o); return o
def light(kind, loc, energy, color='#FFFFFF', size=1.0, rot=(0, 0, 0)):
    ld = bpy.data.lights.new('L', kind); ld.energy = energy; ld.color = hexc(color)[:3]
    if kind == 'AREA': ld.size = size
    elif kind in ('POINT', 'SPOT'): ld.shadow_soft_size = min(size, 0.06)
    o = bpy.data.objects.new('L', ld); o.location = loc; o.rotation_euler = rot; o.visible_camera = False; o.visible_glossy = False; CUR[0].objects.link(o); return o

from mathutils import Matrix
def parent_to(ch, p):
    ch.parent = p; ch.matrix_parent_inverse = Matrix.Translation(-Vector(p.location))

def kf(o, path, t, v, interp='BEZIER', idx=-1):
    setattr_path(o, path, v)
    fr = F(t) if isinstance(t, float) or isinstance(t, int) else t
    o.keyframe_insert(data_path=path, frame=fr, index=idx)
    ad = o.animation_data if hasattr(o, 'animation_data') else None
    if ad and ad.action:
        for fc in ad.action.fcurves:
            if fc.data_path == path:
                for k in fc.keyframe_points:
                    if k.co[0] == fr: k.interpolation = interp
def setattr_path(o, path, v):
    if '.' in path:
        a, b = path.rsplit('.', 1); setattr(o.path_resolve(a), b, v)
    else:
        setattr(o, path, v)
def ease_out(o, path, t0, v0, t1, v1):
    kf(o, path, t0, v0); kf(o, path, t1, v1)
def pop(o, t, dur=0.35, s=1.0):
    """scale in from 0 with a small overshoot"""
    kf(o, 'scale', t - 0.01, (0.0001,) * 3, 'CONSTANT'); kf(o, 'scale', t, (0.0001,) * 3)
    kf(o, 'scale', t + dur * 0.7, (s * 1.08,) * 3); kf(o, 'scale', t + dur, (s,) * 3)

def dish(loc, r, m):  # diya bowl
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=r)
    for v in [v for v in bm.verts if v.co.z > 0.0001]: bm.verts.remove(v)
    for v in bm.verts: v.co.z *= 0.55; v.co.y *= 0.8 if v.co.y > 0 else 1.0
    me = bpy.data.meshes.new('dish'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('dish', me); o.location = loc; me.materials.append(m)
    sol = o.modifiers.new('s', 'SOLIDIFY'); sol.thickness = r * 0.12
    for p in me.polygons: p.use_smooth = True
    CUR[0].objects.link(o); return o
def diya(loc, r=0.25, flame_light=12.0, flicker=True, light_on=True):
    x, y, z = loc
    d = dish((x, y, z + r * 0.55), r, mat('clay', '#A0522D', 0.7))
    rim = cyl((x, y, z + r * 0.56), r * 0.82, 0.01, mat('oil', '#5A3A10', 0.2), 24)
    fl = sph((x, y, z + r * 0.85), r * 0.16, emat('flame', FLAME, 28), 16, 'flame')
    fl.scale = (1, 1, 2.2)
    core = sph((x, y, z + r * 0.8), r * 0.07, emat('flamecore', '#FFF2C0', 40), 12)
    L = light('POINT', (x, y, z + r * 1.4), flame_light, '#FFB061', 0.05) if light_on else None
    if flicker and L:
        for k in range(0, 80):
            t = k * 0.5 + random.random() * 0.2
            kf(L.data, 'energy', t, flame_light * (0.8 + 0.4 * random.random()))
            kf(fl, 'scale', t, (1, 1, 2.0 + 0.5 * random.random()))
    return d

def bills_burst(origin, n, t0, t1, toward, spread=3.0, m=None):
    m = m or mat('bill', '#6FA86B', 0.6, emit='#9CD48F', es=0.4)
    out = []
    for i in range(n):
        o = plane(origin, 0.42, 0.2, m, name='bill')
        st = t0 + (t1 - t0) * i / n
        end = Vector(origin) + Vector(toward) * (0.6 + random.random() * 0.6) + Vector(((random.random() - .5) * spread, (random.random() - .5) * spread * 0.6, (random.random()) * spread * 0.7))
        kf(o, 'scale', st - 0.1, (0.0001,) * 3, 'CONSTANT'); kf(o, 'scale', st, (1, 1, 1), 'CONSTANT')
        kf(o, 'location', st, origin, 'LINEAR'); kf(o, 'location', st + 2.2, tuple(end), 'LINEAR')
        kf(o, 'rotation_euler', st, (random.random() * 3, random.random() * 3, 0), 'LINEAR')
        kf(o, 'rotation_euler', st + 2.2, (random.random() * 12, random.random() * 12, random.random() * 6), 'LINEAR')
        kf(o, 'scale', st + 2.2, (1, 1, 1)); kf(o, 'scale', st + 2.5, (0.0001,) * 3)
        out.append(o)
    return out

def firework(c, t, n=36, R=2.2, color=GOLD, life=1.6):
    m = emat('fw' + color, color, 18)
    for i in range(n):
        ph = math.acos(1 - 2 * (i + 0.5) / n); th = math.pi * (1 + 5 ** 0.5) * i
        d = Vector((math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph)))
        o = ico(c, 0.05, m)
        kf(o, 'scale', t - 0.1, (0.0001,) * 3, 'CONSTANT'); kf(o, 'scale', t, (1.4, 1.4, 1.4))
        kf(o, 'location', t, c); kf(o, 'location', t + life, tuple(Vector(c) + d * R + Vector((0, 0, -0.6))))
        kf(o, 'scale', t + life * 0.6, (1, 1, 1)); kf(o, 'scale', t + life, (0.0001,) * 3)

def string_lights(p0, p1, n, sag, colors):
    for i in range(n):
        u = i / (n - 1); p = Vector(p0).lerp(Vector(p1), u); p.z -= sag * 4 * u * (1 - u)
        sph(tuple(p), 0.045, emat('sl' + colors[i % len(colors)], colors[i % len(colors)], 12), 10)

CAMS = {}
def camera(name, keys, lens=35, vk=1.6, vz=0.0):
    """keys: list of (t, loc, target). Vertical framing pulls the camera back by vk and shifts target z by vz."""
    cd = bpy.data.cameras.new('C' + name); cd.lens = lens; cd.sensor_fit = 'AUTO'; cd.clip_end = 400
    cam = bpy.data.objects.new('C' + name, cd); CUR[0].objects.link(cam)
    tg = bpy.data.objects.new('T' + name, None); CUR[0].objects.link(tg)
    c = cam.constraints.new('TRACK_TO'); c.target = tg; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    for t, loc, tgt in keys:
        loc = Vector(loc); tgt = Vector(tgt)
        if VERT: tgt = tgt + Vector((0, 0, vz * 0.3)); loc = tgt + (loc - tgt) * (1 + (vk - 1) * 0.3)
        kf(cam, 'location', t, tuple(loc)); kf(tg, 'location', t, tuple(tgt))
    CAMS[name] = cam; return cam

def ground(origin, m, size=80):
    return plane((origin[0], origin[1], 0), size, size, m, name='ground')

# ============ SCENE A: the heist (lines 0-1) ============
def scene_A():
    scene_coll('A'); X = 0
    stone = mat('stone', '#8E9AAF', 0.55); dark = mat('ground_dark', '#0E1424', 0.35)
    ground((X, 0), dark)
    for i, (w, d) in enumerate([(12, 6), (11, 5.4), (10, 4.8)]):
        box((X, 0, 0.2 + i * 0.4), (w, d, 0.4), stone, 0.02)
    for i in range(6):
        cx = X - 3.75 + i * 1.5
        cyl((cx, -1.6, 1.2 + 2.2), 0.32, 4.4, stone, 32)
        box((cx, -1.6, 1.25), (0.85, 0.85, 0.2), stone)
        box((cx, -1.6, 5.55), (0.85, 0.85, 0.2), stone)
    box((X, 0.6, 3.4), (9.2, 3.6, 4.4), mat('wall', '#5B6578', 0.7))
    box((X, -0.5, 5.9), (10.4, 5.0, 0.5), stone, 0.03)
    # pediment
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in [(-5.2, -3, 0), (5.2, -3, 0), (0, -3, 1.6), (-5.2, 2, 0), (5.2, 2, 0), (0, 2, 1.6)]]
    for f in [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]: bm.faces.new([vs[i] for i in f])
    me = bpy.data.meshes.new('ped'); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('ped', me); o.location = (X, 0, 6.15); me.materials.append(stone); CUR[0].objects.link(o)
    # door glow
    plane((X, -1.19, 2.6), 1.8, 2.8, emat('doorglow', '#FFC870', 6), rot=(math.radians(90), 0, 0))
    # alarm lights
    for sx in (-4.6, 4.6):
        al = light('POINT', (X + sx, -2.6, 5.0), 300, CORAL, 0.3)
        for k in range(30):
            t = k * 0.4; kf(al.data, 'energy', t, 600 if k % 2 == 0 else 40, 'CONSTANT')
        sph((X + sx, -2.55, 5.0), 0.16, emat('alarm', CORAL, 30), 16)
    light('AREA', (X - 6, -10, 12), 2500, '#9DB8FF', 8, rot=(math.radians(50), 0, math.radians(-30)))
    light('AREA', (X + 8, -6, 4), 600, SKY, 4, rot=(math.radians(80), 0, math.radians(50)))
    # money flying out of the door
    bills_burst((X, -1.4, 2.4), 70, W(0, 'stole') - 0.3, LE(1), (0, -6, 1.5), spread=6)
    # $81,000,000
    t81 = text('$81,000,000', (X, -3.6, 9.0), 1.25, mat('gold', GOLD, 0.25, 0.9, emit=GOLD, es=0.6), 0.18)
    pop(t81, W(0, 'eighty') - 0.05, 0.45)
    sub = text('STOLEN', (X, -3.6, 8.0), 0.45, mat('linen_e', LINEN, 0.5, emit=LINEN, es=0.8), 0.04, font=FONT_X)
    pop(sub, W(0, 'eighty') + 0.35, 0.35)
    # moon
    sph((X + 24, 30, 20), 2.2, emat('moon', '#DDE6FF', 3), 32)
    camera('A', [(0.0, (X + 2.5, -19, 4.6), (X, 0, 6.4)), (CUT(2), (X - 1.5, -16.5, 4.2), (X, 0, 6.8))], 32, vk=1.75, vz=0.6)

# ============ SCENE B: closed, closed, closed (line 2) ============
def scene_B():
    scene_coll('B'); X = 100
    ground((X, 0), mat('floorB', '#141A2E', 0.3))
    plane((X, 6, 6), 60, 14, mat('wallB', '#1B2340', 0.8), rot=(math.radians(90), 0, 0))
    labels = [('BANGLADESH', 'WEEKEND', W(2, 'bank')), ('NEW YORK', 'WEEKEND', W(2, 'york')), ('PHILIPPINES', 'HOLIDAY', W(2, 'holiday'))]
    wood = mat('signwood', BROWN, 0.6); red = mat('signred', CORAL, 0.4, emit=CORAL, es=0.5)
    spacing = 6.0
    for i, (top, bot, t) in enumerate(labels):
        cx = X + (i - 1) * spacing
        pivot = bpy.data.objects.new('pv', None); pivot.location = (cx, 0, 6.2); CUR[0].objects.link(pivot)
        parts = []
        parts.append(box((cx, 0, 3.6), (4.2, 0.18, 2.6), wood, 0.05))
        parts.append(box((cx, -0.1, 3.6), (3.9, 0.04, 2.3), mat('signface', LINEN, 0.7)))
        tt = text(top, (cx, -0.14, 4.25), 0.42, mat('ink', '#1D2433', 0.6), 0.01, font=FONT_X); parts.append(tt)
        tb = text('CLOSED', (cx, -0.14, 3.45), 0.78, red, 0.03, font=FONT_X); parts.append(tb)
        tl = text(bot, (cx, -0.14, 2.75), 0.32, mat('ink2', BROWN, 0.6), 0.01, font=FONT_X); parts.append(tl)
        for sx in (-1.2, 1.2):
            parts.append(cyl((cx + sx * 0.5, 0, 5.6), 0.02, 1.4, mat('string', '#C9B79C', 0.8), 8, rot=(0, math.radians(-25 if sx < 0 else 25), 0)))
        for pt in parts:
            parent_to(pt, pivot)
        # drop in and swing
        kf(pivot, 'location', t - 0.5, (cx, 0, 14.0)); kf(pivot, 'location', t - 0.05, (cx, 0, 6.2))
        kf(pivot, 'rotation_euler', t - 0.05, (math.radians(-20), 0, math.radians(6)))
        for k, a in enumerate([14, -9, 6, -3.5, 2, 0]):
            kf(pivot, 'rotation_euler', t + 0.35 * (k + 1), (math.radians(a), 0, math.radians(a * 0.2)))
        L = light('SPOT', (cx, -5, 9), 0, '#FFE2B0', 0.4, rot=(math.radians(35), 0, 0)); L.data.spot_size = math.radians(40)
        kf(L.data, 'energy', t - 0.3, 0); kf(L.data, 'energy', t + 0.1, 1800)
    light('AREA', (X, -8, 10), 300, '#7D96D8', 10, rot=(math.radians(40), 0, 0))
    t0, t1 = CUT(2), CUT(3)
    tb = [W(2, 'bank'), W(2, 'york'), W(2, 'holiday')]
    if VERT:
        keys = [(t0, (X - spacing - 1.0, -10, 4.2), (X - spacing, 0, 3.7))]
        for i, t in enumerate(tb[1:], 1):
            keys += [(t - 0.6, (X + (i - 2) * spacing + 0.4, -10, 4.2), (X + (i - 2) * spacing, 0, 3.7)),
                     (t + 0.2, (X + (i - 1) * spacing - 0.6, -10, 4.2), (X + (i - 1) * spacing, 0, 3.7))]
        keys += [(t1 - 1.2, (X + spacing, -10, 4.2), (X + spacing, 0, 3.7)), (t1, (X, -24, 4.6), (X, 0, 3.7))]
        camera('B', keys, 35, vk=1.0)
    else:
        camera('B', [(t0, (X - 4, -11, 4.0), (X - 3, 0, 3.6)), (tb[1] + 0.2, (X - 0.5, -13, 4.3), (X, 0, 3.6)),
                     (t1, (X + 1.0, -17, 4.6), (X, 0, 3.6))], 35)

# ============ SCENE C: the empty vault (line 3) ============
def scene_C():
    scene_coll('C'); X = 200
    steel = mat('steel', '#9AA3AE', 0.3, 0.9); dsteel = mat('dsteel', '#4A525C', 0.35, 0.9)
    ground((X, 0), mat('floorC', '#1A1F2A', 0.25))
    plane((X, 4, 5), 40, 12, mat('wallC', '#232B3A', 0.7), rot=(math.radians(90), 0, 0))
    # shelves (empty)
    for sx in (-3.2, 3.2):
        for h in (1.2, 2.6, 4.0):
            box((X + sx, 3.0, h), (2.6, 1.6, 0.12), dsteel)
        box((X + sx, 3.8, 2.6), (2.6, 0.1, 4.6), dsteel)
    # vault door, swung open
    door = bpy.data.objects.new('door', None); door.location = (X + 2.2, -1.0, 2.6); CUR[0].objects.link(door)
    parts = [cyl((X + 2.2 - 2.2, -1.0, 2.6), 2.2, 0.6, steel, 64, rot=(math.radians(90), 0, 0))]
    parts.append(cyl((X, -1.35, 2.6), 0.35, 0.3, dsteel, 32, rot=(math.radians(90), 0, 0)))
    for a in range(3):
        b = box((X, -1.45, 2.6), (2.4, 0.08, 0.12), dsteel); b.rotation_euler = (0, math.radians(a * 60), 0); parts.append(b)
    for a in range(12):
        ang = a * math.pi / 6
        parts.append(cyl((X + math.cos(ang) * 1.8, -1.32, 2.6 + math.sin(ang) * 1.8), 0.12, 0.1, dsteel, 16, rot=(math.radians(90), 0, 0)))
    for pt in parts: parent_to(pt, door)
    kf(door, 'rotation_euler', CUT(3), (0, 0, math.radians(-60))); kf(door, 'rotation_euler', CUT(4), (0, 0, math.radians(-78)))
    # one last bill floating down
    b = plane((X - 0.4, 0.8, 5.5), 0.42, 0.2, mat('bill', '#6FA86B', 0.6, emit='#9CD48F', es=0.4), name='bill')
    t0 = CUT(3)
    for k in range(9):
        t = t0 + k * 0.5
        kf(b, 'location', t, (X - 0.4 + math.sin(k * 1.3) * 0.6, 0.8, 5.5 - k * 0.6 if k < 9 else 0.05))
        kf(b, 'rotation_euler', t, (math.radians(20 * math.sin(k)), math.radians(30 * math.cos(k * 1.7)), k * 0.4))
    # flickering ceiling light
    L = light('AREA', (X, -1.5, 7.5), 1500, '#CFE0FF', 5, rot=(0, 0, 0))
    light('AREA', (X + 5, -6, 4), 500, SKY, 4, rot=(math.radians(75), 0, math.radians(45)))
    for k in range(20):
        t = t0 + k * 0.25; kf(L.data, 'energy', t, 1500 if random.random() > 0.25 else 300, 'CONSTANT')
    light('POINT', (X - 1, -3, 3), 200, CORAL, 1)
    camera('C', [(t0, (X - 1.5, -12, 3.3), (X - 0.5, 1.5, 2.6)), (CUT(4), (X - 0.8, -8.5, 2.8), (X - 0.4, 1.5, 2.4))], 30, vk=1.5)

# ============ SCENE D: the city goes quiet (line 4) ============
def scene_D():
    scene_coll('D'); X = 300
    ground((X, 0), mat('floorD', '#0B0F1C', 0.4))
    winon = emat('win_on', '#FFD38A', 6); winoff = mat('win_off', '#1B2336', 0.3)
    bld = mat('bld', '#26304A', 0.7)
    t0, t1 = CUT(4), CUT(5)
    random.seed(3)
    targets = []
    for gx in range(-5, 6):
        for gy in range(0, 4):
            w = 1.6 + random.random() * 0.8; h = 2.5 + random.random() * 6 * (1 if gy else 0.7)
            cx = X + gx * 2.8 + random.random() * 0.5; cy = gy * 3.5 + random.random()
            box((cx, cy, h / 2), (w, w, h), bld)
            # windows on the front face
            for wx in range(2):
                for wz in range(int(h // 1.1)):
                    p = plane((cx - w / 4 + wx * w / 2, cy - w / 2 - 0.01, 0.8 + wz * 1.1), 0.42, 0.55, winon, rot=(math.radians(90), 0, 0))
                    off = t0 + 0.3 + random.random() * (t1 - t0 - 1.0)
                    if random.random() < 0.82:
                        kf(p, 'scale', off, (1, 1, 1), 'CONSTANT'); kf(p, 'scale', off + 0.12, (0.0001,) * 3, 'CONSTANT')
                        dk = plane((cx - w / 4 + wx * w / 2, cy - w / 2 - 0.005, 0.8 + wz * 1.1), 0.42, 0.55, winoff, rot=(math.radians(90), 0, 0))
            if gy < 2 and random.random() < 0.35: targets.append((cx, cy - w / 2 - 0.3, h * 0.6))
    # red pings on dark buildings: attacks
    ping = emat('ping', CORAL, 25)
    random.shuffle(targets)
    for i, (x, y, z) in enumerate(targets[:9]):
        t = t0 + 2.2 + i * (t1 - t0 - 3.0) / 9
        s = sph((x, y, z), 0.22, ping, 16); pop(s, t, 0.3)
        r = cyl((x, y - 0.05, z), 0.5, 0.02, emat('ring', CORAL, 10), 32, rot=(math.radians(90), 0, 0))
        kf(r, 'scale', t - 0.1, (0.0001,) * 3, 'CONSTANT'); kf(r, 'scale', t, (0.2, 0.2, 1)); kf(r, 'scale', t + 0.8, (3, 3, 1)); kf(r, 'scale', t + 0.82, (0.0001,) * 3, 'CONSTANT')
        L = light('POINT', (x, y - 0.6, z), 0, CORAL, 0.2); kf(L.data, 'energy', t - 0.05, 0); kf(L.data, 'energy', t + 0.1, 120)
    light('AREA', (X, -20, 20), 1200, '#6E86C9', 20, rot=(math.radians(45), 0, 0))
    sph((X - 12, 40, 18), 2.0, emat('moon', '#DDE6FF', 3), 32)
    camera('D', [(t0, (X, -26, 9), (X, 4, 3.5)), (t1, (X + 3, -19, 6), (X + 1, 4, 3.5))], 30, vk=1.45, vz=1.0)

# ============ SCENE E: Diwali night + the question (lines 5-6) ============
def scene_E():
    scene_coll('E'); X = 400
    ground((X, 0), mat('floorE', '#2A1A14', 0.5))
    # houses with lit doorways
    for i, gx in enumerate(range(-4, 5)):
        h = 3 + (i % 3) * 0.8; cx = X + gx * 3.2
        box((cx, 6, h / 2), (2.8, 2.6, h), mat('house%d' % (i % 3), ['#C46B52', '#D9A55B', '#6F86B5'][i % 3], 0.8))
        plane((cx, 4.69, 1.0), 0.9, 1.7, emat('doorE', '#FFC870', 5), rot=(math.radians(90), 0, 0))
        string_lights((cx - 1.4, 4.6, h - 0.1), (cx + 1.4, 4.6, h - 0.1), 9, 0.35, [GOLD, CORAL, LIME, SKY])
    # rows of diyas
    for k in range(13):
        diya((X - 6 + k * 1.0, -0.5, 0), 0.22, 6 if k % 2 == 0 else 0, light_on=k % 2 == 0)
    for k in range(7):
        diya((X - 3 + k * 1.0, -2.2, 0), 0.22, 6, light_on=k % 3 == 0)
    # floating phones sending money
    t0, t1 = CUT(5), CUT(7)
    ph_m = mat('phone', '#111318', 0.3, 0.5); scr = emat('screen', SKY, 3)
    for j, (px, pz) in enumerate([(-3.0, 3.0), (0.4, 3.6), (3.4, 2.8)]):
        holder = bpy.data.objects.new('ph', None); holder.location = (X + px, 1.5, pz); CUR[0].objects.link(holder)
        a = box((X + px, 1.5, pz), (0.75, 0.08, 1.45), ph_m, 0.05); s = plane((X + px, 1.45, pz), 0.62, 1.25, scr, rot=(math.radians(90), 0, 0))
        g = box((X + px, 1.40, pz + 0.1), (0.3, 0.02, 0.3), emat('gift', CORAL, 6))
        for pt in (a, s, g): parent_to(pt, holder)
        ts = t0 + 0.4 + j * 0.5
        pop(holder, ts, 0.4)
        for k in range(12):
            kf(holder, 'rotation_euler', ts + k * 0.5, (0, 0, math.radians(12 * math.sin(k + j))))
            kf(holder, 'location', ts + k * 0.5, (X + px, 1.5, pz + 0.15 * math.sin(k * 1.4 + j)))
        # coins flying from phone up
        for c in range(6):
            co = cyl((X + px, 1.3, pz + 0.6), 0.12, 0.03, mat('coin', GOLD, 0.25, 1.0, emit=GOLD, es=0.4), 24, rot=(math.radians(90), 0, 0))
            tc = ts + 0.6 + c * 0.45
            kf(co, 'scale', tc - 0.1, (0.0001,) * 3, 'CONSTANT'); kf(co, 'scale', tc, (1, 1, 1))
            kf(co, 'location', tc, (X + px, 1.3, pz + 0.6)); kf(co, 'location', tc + 1.4, (X + px + (c - 2.5) * 0.4, 1.0, pz + 3.2))
            kf(co, 'scale', tc + 1.2, (1, 1, 1)); kf(co, 'scale', tc + 1.4, (0.0001,) * 3)
    # fireworks across the line
    cols = [GOLD, CORAL, SKY, LIME, GOLD, CORAL]
    for i in range(6):
        firework((X - 7 + i * 2.8 + random.random(), 10 + random.random() * 3, 8 + random.random() * 3), t0 + 0.2 + i * 0.9, 40, 2.4, cols[i])
    # the question: a red shadow figure? No faces: a big coral question mark rises over the town
    q = text('?', (X, 3.0, 6.2), 4.2, mat('qm', CORAL, 0.3, emit=CORAL, es=3.0), 0.5, font=FONT_X)
    pop(q, W(6, 'watching') - 0.1, 0.5)
    kf(q, 'rotation_euler', W(6, 'watching'), (math.radians(90), 0, math.radians(-15))); kf(q, 'rotation_euler', t1, (math.radians(90), 0, math.radians(15)))
    light('AREA', (X, -10, 10), 400, '#7A6BC8', 14, rot=(math.radians(40), 0, 0))
    sky = plane((X, 30, 12), 120, 50, mat('skyE', '#0D1030', 0.9), rot=(math.radians(90), 0, 0))
    camera('E', [(t0, (X - 1, -9.5, 2.2), (X, 2, 2.4)), (CUT(6) + 0.3, (X, -11, 2.8), (X, 2, 3.0)), (t1, (X, -17, 4.0), (X, 2, 4.4))], 32, vk=1.55, vz=0.8)

# ============ SCENE G: the glass fund only you control (lines 7-8) ============
def scene_G():
    scene_coll('G'); X = 500
    ground((X, 0), mat('floorG', '#10162A', 0.35))
    ped = cyl((X, 0, 0.5), 1.8, 1.0, mat('pedestal', LINEN, 0.5), 64)
    glass = box((X, 0, 2.3), (2.6, 2.6, 2.6), mat('glass', '#EAF6FF', 0.02, trans=1.0, ior=1.3), 0.06)
    frame = mat('frameG', LIME, 0.3, 0.2, emit=LIME, es=0.8)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box((X + sx * 1.3, sy * 1.3, 2.3), (0.06, 0.06, 2.62), frame)
    for z in (1.0, 3.6):
        for sx in (-1, 1):
            box((X + sx * 1.3, 0, z), (0.06, 2.62, 0.06), frame); box((X, sx * 1.3, z), (2.62, 0.06, 0.06), frame)
    # coins + sapling inside
    for i in range(7):
        cyl((X - 0.3, 0.1, 1.08 + i * 0.07), 0.32, 0.06, mat('coin', GOLD, 0.25, 1.0, emit=GOLD, es=0.4), 32)
    stem = cyl((X + 0.45, 0, 1.6), 0.04, 1.2, mat('stem', '#4E8E1A', 0.6), 12)
    for s in (-1, 1):
        lf = sph((X + 0.45 + s * 0.25, 0, 2.15), 0.22, mat('leaf', LIME, 0.5, emit=LIME, es=0.3), 16); lf.scale = (1.3, 0.35, 0.6); lf.rotation_euler = (0, math.radians(-30 * s), 0)
    sph((X + 0.45, 0, 1.0), 0.25, mat('soil', '#4A2E1E', 0.9), 16).scale = (1.2, 1.2, 0.4)
    # your key, floating in front
    key = bpy.data.objects.new('key', None); key.location = (X + 2.4, -2.2, 2.4); CUR[0].objects.link(key)
    km = mat('keym', LIME, 0.25, 0.6, emit=LIME, es=1.5)
    kparts = [cyl((X + 2.4, -2.2, 2.75), 0.28, 0.08, km, 32, rot=(math.radians(90), 0, 0)), box((X + 2.4, -2.2, 2.15), (0.09, 0.08, 0.9), km),
              box((X + 2.52, -2.2, 1.8), (0.16, 0.08, 0.08), km), box((X + 2.52, -2.2, 1.98), (0.12, 0.08, 0.08), km)]
    for pt in kparts: parent_to(pt, key)
    t0, t1 = CUT(7), CUT(9)
    for k in range(int((t1 - t0) / 0.6) + 2):
        t = t0 + k * 0.6; kf(key, 'location', t, (X + 2.4, -2.2, 2.4 + 0.12 * math.sin(k * 1.2))); kf(key, 'rotation_euler', t, (0, 0, math.radians(20 * math.sin(k * 0.7))))
    # three grabs (bank, broker, us) bounce off the glass
    hits = [W(7, 'bank'), W(7, 'broker'), W(7, 'us')]
    dirs = [(-1, -0.6), (1, -0.9), (-0.2, -1)]
    gm = mat('grab', CORAL, 0.4, emit=CORAL, es=2.0)
    for (dx, dy), t in zip(dirs, hits):
        d = Vector((dx, dy, 0)).normalized(); start = Vector((X, 0, 2.4)) + d * 7; hit = Vector((X, 0, 2.4)) + d * 1.55
        ar = cyl(tuple(start), 0.12, 0.9, gm, 16)
        ar.rotation_euler = Vector((0, 0, 1)).rotation_difference(-d).to_euler()
        kf(ar, 'location', t - 0.45, tuple(start)); kf(ar, 'location', t, tuple(hit), 'LINEAR'); kf(ar, 'location', t + 0.7, tuple(start + Vector((0, 0, 1.5))))
        kf(ar, 'scale', t + 0.5, (1, 1, 1)); kf(ar, 'scale', t + 0.7, (0.0001,) * 3, 'CONSTANT')
        bpy.ops.mesh.primitive_torus_add(location=tuple(hit), major_radius=0.6, minor_radius=0.03); rg = link(bpy.context.object); rg.data.materials.append(emat('ripple', LIME, 8))
        rg.rotation_euler = Vector((0, 0, 1)).rotation_difference(d).to_euler()
        kf(rg, 'scale', t - 0.1, (0.0001,) * 3, 'CONSTANT'); kf(rg, 'scale', t, (0.3, 0.3, 1)); kf(rg, 'scale', t + 0.5, (2.2, 2.2, 1)); kf(rg, 'scale', t + 0.52, (0.0001,) * 3, 'CONSTANT')
    # public record: glowing ledger cards orbit (line 8)
    t8 = LS(8)
    pv = bpy.data.objects.new('orb', None); pv.location = (X, 0, 2.4); CUR[0].objects.link(pv)
    card = mat('card', LINEN, 0.5, emit=LINEN, es=0.6); row = emat('row', INDIGO, 2); tick = emat('tick', LIME, 6)
    for i in range(6):
        a = i * math.pi / 3; cx, cy = X + math.cos(a) * 3.3, math.sin(a) * 3.3
        grp = [plane((cx, cy, 2.4), 1.1, 1.4, card, rot=(math.radians(90), 0, a + math.pi / 2))]
        for r in range(4):
            off = Vector((-math.sin(a), math.cos(a), 0)) * 0
            grp.append(plane((cx - math.cos(a) * 0.02, cy - math.sin(a) * 0.02, 2.8 - r * 0.28), 0.7, 0.08, row, rot=(math.radians(90), 0, a + math.pi / 2)))
            grp.append(sph((cx - math.cos(a) * 0.03 + math.sin(a) * 0.42, cy - math.sin(a) * 0.03 - math.cos(a) * 0.42, 2.8 - r * 0.28), 0.06, tick, 10))
        for g in grp:
            parent_to(g, pv)
            kf(g, 'scale', t8 + i * 0.12 - 0.01, (0.0001,) * 3, 'CONSTANT'); kf(g, 'scale', t8 + i * 0.12 + 0.3, (1, 1, 1))
    kf(pv, 'rotation_euler', t8, (0, 0, 0), 'LINEAR'); kf(pv, 'rotation_euler', t1 + 0.5, (0, 0, math.radians(110)), 'LINEAR')
    light('AREA', (X - 4, -6, 7), 900, '#FFF1DC', 5, rot=(math.radians(45), 0, math.radians(-30)))
    light('AREA', (X + 5, 3, 5), 500, SKY, 4, rot=(math.radians(70), 0, math.radians(120)))
    light('POINT', (X, 0, 2.2), 60, LIME, 0.5)
    camera('G', [(t0, (X + 3.5, -9.5, 3.4), (X + 0.4, 0, 2.3)), (t8 - 0.2, (X + 1.0, -9.0, 3.6), (X, 0, 2.3)),
                 (t1, (X - 3.5, -11.5, 5.2), (X, 0, 2.3))], 35, vk=1.45, vz=0.3)

# ============ SCENE I: $10 seed (line 9) ============
def scene_I():
    scene_coll('I'); X = 600
    ground((X, 0), mat('floorI', '#10162A', 0.35))
    cyl((X, 0, 0.45), 1.4, 0.9, mat('pedestal', LINEN, 0.5), 64)
    coin = cyl((X, 0, 1.0), 0.75, 0.16, mat('coin', GOLD, 0.25, 1.0, emit=GOLD, es=0.4), 64)
    t0, t1 = CUT(9), CUT(10)
    stem = cyl((X, 0, 1.1), 0.05, 1.4, mat('stem', '#4E8E1A', 0.6), 12); stem.location.z = 1.1
    bpy.context.view_layer.objects.active = stem
    stem.data.transform(__import__('mathutils').Matrix.Translation((0, 0, 0.7)))
    kf(stem, 'scale', t0, (1, 1, 0.0001)); kf(stem, 'scale', t0 + 1.4, (1, 1, 1))
    for s in (-1, 1):
        lf = sph((X + s * 0.32, 0, 2.35), 0.3, mat('leaf', LIME, 0.5, emit=LIME, es=0.3), 16)
        lf.rotation_euler = (0, math.radians(-30 * s), 0); kf(lf, 'scale', t0 + 1.0, (0.0001,) * 3); kf(lf, 'scale', t0 + 1.6, (1.3, 0.35, 0.6))
    t10 = text('$10', (X, -0.6, 3.6), 1.5, mat('limeT', LIME, 0.3, emit=LIME, es=1.2), 0.2, font=FONT_X)
    pop(t10, W(9, 'ten') - 0.1, 0.4)
    for k in range(5):
        diya((X - 3.2 + k * 1.6, -2.4, 0), 0.22, 5)
    light('AREA', (X - 3, -6, 7), 700, '#FFF1DC', 5, rot=(math.radians(45), 0, math.radians(-25)))
    camera('I', [(t0, (X + 1.2, -8.0, 2.8), (X, 0, 2.2)), (t1, (X - 0.6, -7.2, 2.6), (X, 0, 2.4))], 35, vk=1.55, vz=0.2)

# ============ SCENE J: Happy Diwali end card (line 10 + tail) ============
def scene_J():
    scene_coll('J'); X = 700
    ground((X, 0), mat('floorJ', '#1C120E', 0.5))
    card = box((X, 0.4, 2.7), (5.6, 0.12, 1.5), mat('cardJ', '#FFFFFF', 0.6), 0.06)
    lg = plane((X, 0.33, 2.7), 5.0, 5.0 * 102 / 520, img_mat('logo', LOGO, 0.4), rot=(math.radians(90), 0, 0))
    lg.data.materials[0].blend_method = 'BLEND' if hasattr(lg.data.materials[0], 'blend_method') else None
    hd = text('Happy Diwali', (X, 0.0, 4.55), 0.85, mat('gold', GOLD, 0.25, 0.9, emit=GOLD, es=0.6), 0.12, font=FONT_X)
    t0 = CUT(10)
    pop(hd, W(10, 'happy') - 0.1, 0.5)
    ys = text('Your money stays yours.', (X, 0.0, 1.55), 0.36, mat('linen_e', LINEN, 0.5, emit=LINEN, es=0.8), 0.03, font=FONT_X)
    pop(ys, W(10, 'your') - 0.05, 0.35)
    for k in range(16):
        a = math.pi * (0.05 + 0.9 * k / 15); diya((X + math.cos(a) * 4.2, -1.0 - math.sin(a) * 1.8, 0), 0.22, 5 if k % 2 == 0 else 0, light_on=k % 2 == 0)
    cols = [GOLD, CORAL, SKY, LIME, GOLD, CORAL, SKY, LIME]
    for i in range(8):
        firework((X - 6 + (i % 4) * 4 + random.random(), 8 + random.random() * 2, 6.5 + random.random() * 2.5), t0 + 0.2 + i * 0.75, 36, 2.0, cols[i])
    light('AREA', (X, -7, 6), 700, '#FFF1DC', 6, rot=(math.radians(55), 0, 0))
    plane((X, 25, 12), 120, 50, mat('skyE', '#0D1030', 0.9), rot=(math.radians(90), 0, 0))
    camera('J', [(t0, (X, -11.5, 3.0), (X, 0, 3.1)), (END, (X, -9.8, 2.9), (X, 0, 3.1))], 35, vk=1.6, vz=0.3)

BUILD = dict(A=scene_A, B=scene_B, C=scene_C, D=scene_D, E=scene_E, G=scene_G, I=scene_I, J=scene_J)
want = ONLY.split(',') if ONLY else [s[0] for s in SCENES]
for n in want: BUILD[n]()

# ---------- world, render settings, glow ----------
w = bpy.data.worlds.new('W'); S.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = hexc('#070B18'); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'; S.cycles.samples = SAMPLES; S.cycles.use_denoising = True
S.cycles.denoiser = 'OPENIMAGEDENOISE'; S.cycles.max_bounces = 6; S.cycles.transmission_bounces = 6; S.cycles.glossy_bounces = 3
S.cycles.diffuse_bounces = 1; S.cycles.caustics_reflective = False; S.cycles.caustics_refractive = False; S.cycles.max_bounces = 4; S.cycles.glossy_bounces = 2; S.cycles.transmission_bounces = 4;
for m_ in bpy.data.materials:
    try: m_.cycles.emission_sampling = 'NONE'
    except Exception as e: print('ES', e)
S.cycles.use_adaptive_sampling = True; S.cycles.adaptive_threshold = float(arg("--thr", "0.05")); S.cycles.use_light_tree = arg("--lt", "1") == "1"; S.render.threads_mode = "FIXED"; S.render.threads = 4
S.render.use_persistent_data = True
S.view_settings.view_transform = 'AgX'; S.view_settings.look = 'AgX - Medium High Contrast'
W0, H0 = (1080, 1920) if VERT else (1920, 1080)
S.render.resolution_x, S.render.resolution_y = W0, H0; S.render.resolution_percentage = int(SCALE * 100)
S.render.image_settings.file_format = 'JPEG'; S.render.image_settings.quality = 93
S.use_nodes = True; nt = S.node_tree; nt.nodes.clear()
rl = nt.nodes.new('CompositorNodeRLayers'); gl = nt.nodes.new('CompositorNodeGlare'); gl.glare_type = 'FOG_GLOW'; gl.quality = 'MEDIUM'; gl.threshold = 0.9; gl.size = 8; gl.mix = -0.55
cp = nt.nodes.new('CompositorNodeComposite'); nt.links.new(rl.outputs['Image'], gl.inputs['Image']); nt.links.new(gl.outputs['Image'], cp.inputs['Image'])

def only_visible(name):
    for n, c in COLL.items():
        lc = bpy.context.view_layer.layer_collection.children['S_' + n]; lc.exclude = (n != name)

os.makedirs(OUT, exist_ok=True)
if PREVIEW:
    for t in [float(x) for x in PREVIEW.split(',')]:
        nm = next(s[0] for s in SCENES if s[1] <= t < s[2] + 1e-6)
        if nm not in COLL: continue
        only_visible(nm); S.camera = CAMS[nm]; S.frame_set(F(t))
        S.render.filepath = os.path.join(OUT, f'prev_{ASPECT}_{t:05.2f}_{nm}.jpg'); bpy.ops.render.render(write_still=True)
else:
    for nm, a, b in SCENES:
        if nm not in want: continue
        only_visible(nm); S.camera = CAMS[nm]
        for fr in range(F(a), F(b), STEP):
            pth = os.path.join(OUT, f'f{fr:05d}.jpg')
            if os.path.exists(pth): continue
            S.frame_set(fr); S.render.filepath = pth; bpy.ops.render.render(write_still=True)
            print('FRAME', fr, flush=True)
print('ALLDONE')
