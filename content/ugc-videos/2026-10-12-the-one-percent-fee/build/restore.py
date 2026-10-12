import sys, os, cv2, numpy as np, torch, json, time
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, "vend"))
from gfpgan.archs.gfpganv1_clean_arch import GFPGANv1Clean
from facexlib.utils.face_restoration_helper import FaceRestoreHelper
from torchvision.transforms.functional import normalize
from facexlib.utils.misc import img2tensor
torch.set_num_threads(4)
src, boxes_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
weight = float(sys.argv[4]) if len(sys.argv) > 4 else 0.85
skip = set()
if len(sys.argv) > 5:
    E = json.load(open(sys.argv[5]))
    for _, a, b in E["inserts"]: skip |= set(range(int(round(a*30))+2, int(round(b*30))-2))
net = GFPGANv1Clean(out_size=512, num_style_feat=512, channel_multiplier=2, decoder_load_path=None, fix_decoder=False, num_mlp=8, input_is_latent=True, different_w=True, narrow=1, sft_half=True)
ck = torch.load(os.path.join(here, "gf/GFPGANv1.4.pth"), map_location="cpu", weights_only=False)
net.load_state_dict(ck["params_ema"] if "params_ema" in ck else ck["params"], strict=True); net.eval()
helper = FaceRestoreHelper(1, face_size=512, crop_ratio=(1, 1), det_model="retinaface_resnet50", save_ext="png", use_parse=False, device=torch.device("cpu"))
boxes = json.load(open(boxes_path))
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
vw = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
i = 0; t = time.time()
while True:
    ok, f = cap.read()
    if not ok: break
    res = f
    if i in skip:
        vw.write(f); i += 1; continue
    helper.clean_all(); helper.read_image(f)
    helper.get_face_landmarks_5(only_center_face=True, resize=480, eye_dist_threshold=5); helper.align_warp_face()
    if helper.cropped_faces:
        cf = helper.cropped_faces[0]
        x = img2tensor(cf / 255., bgr2rgb=True, float32=True); normalize(x, (0.5,)*3, (0.5,)*3, inplace=True)
        with torch.no_grad(): o = net(x.unsqueeze(0), return_rgb=False, weight=0.5)[0]
        o = o.squeeze(0).float().clamp_(-1, 1).numpy().transpose(1, 2, 0)
        o = ((o[:, :, ::-1] + 1) / 2 * 255).round().astype(np.uint8)  # BGR
        helper.add_restored_face(o); helper.get_inverse_affine(None)
        full = helper.paste_faces_to_input_image()
        # blend restored result only around the mouth
        b = boxes[min(i, len(boxes)-1)]; x1, y1, x2, y2 = b; w, h = x2-x1, (y2-y1)*1.12
        m = np.zeros((H, W), np.float32)
        cv2.ellipse(m, (int((x1+x2)/2), int(y1+h*0.74)), (int(w*0.40), int(h*0.27)), 0, 0, 360, 1, -1)
        m = cv2.GaussianBlur(m, (0, 0), w*0.06)[..., None] * weight
        res = (f.astype(np.float32)*(1-m) + full.astype(np.float32)*m).clip(0, 255).astype(np.uint8)
    vw.write(res); i += 1
    if i % 50 == 0: print("restore", i, round(time.time()-t), flush=True)
vw.release(); print("done", i)
