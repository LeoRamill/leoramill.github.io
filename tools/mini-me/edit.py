"""Re-styles the original surfer mini-me render (see README.md):
Catch-Surf-style tribal deck print, orange + glacier wetsuit, smaller head and hand.
Input must be the ORIGINAL render (git show d196639:assets/media/mini-me.png), not an already edited file."""
import cv2, numpy as np, math, argparse, os
from pattern import make_texture
ap=argparse.ArgumentParser()
ap.add_argument("src",help="original mini-me.png (1086x1448 RGBA)")
ap.add_argument("out",help="output PNG")
ap.add_argument("--debug",action="store_true",help="also write debug.png / out_comp.png mask overlays next to the output")
args=ap.parse_args(); SRC=args.src; OUT=args.out
im=cv2.imread(SRC,cv2.IMREAD_UNCHANGED).astype(np.float32)
H,W=im.shape[:2]
bgr=im[...,:3]; alpha=im[...,3]/255.
hsv=cv2.cvtColor(bgr.astype(np.uint8),cv2.COLOR_BGR2HSV).astype(np.float32)
Hh,S,V=hsv[...,0],hsv[...,1],hsv[...,2]
ys,xs=np.mgrid[0:H,0:W].astype(np.float32)
lum=(0.114*bgr[...,0]+0.587*bgr[...,1]+0.299*bgr[...,2])

def poly_mask(pts):
    m=np.zeros((H,W),np.uint8); cv2.fillPoly(m,[np.array(pts,np.int32)],255); return m>0
def halfplane(p0,d):  # dot(p-p0,d) > 0
    return (xs-p0[0])*d[0]+(ys-p0[1])*d[1]>0
def unit(v): n=math.hypot(*v); return (v[0]/n,v[1]/n)
def to_u8(m): return (np.clip(m,0,1)*255).astype(np.uint8)

# ---------------- basic colour classes ----------------
opaque=alpha>0.02
skin=(Hh>=0)&(Hh<=25)&(S>=35)&(V>=45)&opaque
navy=(Hh>=95)&(Hh<=140)&(S>=40)&(V>=14)&(V<=205)&opaque
white=(S<60)&(V>=165)&opaque
bluewater=(Hh>=95)&(Hh<=112)&(S>=90)&(V>=140)&opaque

# ---------------- BOARD ----------------
far=[(341,1001),(348,978),(362,962),(400,943),(447,934),(497,931),(547,935),(597,950),(647,970),(697,997),(747,1032),(797,1072),(830,1101),(851,1119),(878,1144),(905,1171),(928,1198),(946,1216),(960,1235),(964,1250)]
near=[(958,1276),(942,1300),(918,1322),(890,1336),(855,1346),(820,1352),(785,1350),(745,1342),(700,1328),(650,1306),(608,1290),(563,1270),(519,1248),(480,1224),(441,1192),(408,1160),(380,1125),(358,1086),(345,1048)]
board_poly=far+near
board_region=poly_mask(board_poly)
# ---- enclosed opaque-white pockets left by the old flood-fill: make them transparent ----
whiteish=(S<=6)&(V>=250)&(alpha>0.5)
cand=whiteish&~board_region&(ys>=470)
cand=cv2.morphologyEx(to_u8(cand),cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))>0
ext=np.zeros((H+2,W+2),np.uint8); trans=to_u8(alpha<0.5)
ff=trans.copy(); cv2.floodFill(ff,ext,(0,0),128); exterior=(ff==128)
ext_d=cv2.dilate(to_u8(exterior),np.ones((11,11),np.uint8))>0
n,lab,st,_=cv2.connectedComponentsWithStats(to_u8(cand))
pocket=np.zeros((H,W),bool)
for i in range(1,n):
    comp=lab==i
    if st[i,cv2.CC_STAT_AREA]>=300 and not (comp&ext_d).any():
        pocket|=comp; print("pocket comp bbox x,y,w,h,area:",st[i])
pocket_zone=cv2.dilate(to_u8(pocket),np.ones((15,15),np.uint8))>0
dwhite=np.maximum(255-V,S)
pocket_soft=pocket_zone*np.clip(1-dwhite/45.,0,1)
alpha=alpha*(1-pocket_soft)
opaque=alpha>0.02
skin_core=cv2.erode(to_u8(skin),np.ones((3,3),np.uint8))>0
board=board_region&~skin_core&opaque
# homography: nose N, tail T, far-widest F, near-widest Q
N=np.array(far[0],float); T=np.array(far[-1],float)
ax=(T-N)/np.linalg.norm(T-N); nrm=np.array([-ax[1],ax[0]])  # nrm points "down-left" (towards near edge)
def perp(p): return float(np.dot(np.array(p,float)-N,nrm))
Fp=min(far,key=perp); Qp=max(near,key=perp)
L,Wt=2000,800
src=np.float32([[Wt/2,0],[Wt/2,L],[0,L/2],[Wt,L/2]])   # texture (x=v across, y=u along)
dst=np.float32([N,T,Fp,Qp])
Hm=cv2.getPerspectiveTransform(src,dst); Hinv=np.linalg.inv(Hm)
tex=make_texture(L,Wt)
tex_s=cv2.resize(tex,(Wt//2,L//2),interpolation=cv2.INTER_AREA)
tex_s=cv2.GaussianBlur(tex_s,(0,0),0.8)
pts=np.stack([xs,ys,np.ones_like(xs)],-1).reshape(-1,3)@Hinv.T
pts=pts[:,:2]/pts[:,2:3]
mapx=(pts[:,0]/2).reshape(H,W).astype(np.float32); mapy=(pts[:,1]/2).reshape(H,W).astype(np.float32)
patt=cv2.remap(tex_s,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
# shading from blue deck pixels (normalised convolution), whites interpolated
wgt=((S>=80)&board_region&~skin).astype(np.float32)
sh_num=cv2.GaussianBlur(V/220.*wgt,(0,0),5); sh_den=cv2.GaussianBlur(wgt,(0,0),5)
shade=np.where(sh_den>1e-3,sh_num/np.maximum(sh_den,1e-3),1.0)
# add back specular highlights (very bright, low sat) as a small boost
spec=np.clip((V-238)/17.,0,1)*np.clip((120-S)/120.,0,1)*board
shade=np.clip(shade,0.55,1.25)+0.35*spec
board_soft=cv2.GaussianBlur(to_u8(board),(0,0),0.9)/255.
new_board=np.clip(patt*shade[...,None]**1.1,0,255)
# slight soft-top texture: mild desaturation towards render look
out=bgr.copy()
out=out*(1-board_soft[...,None])+new_board*board_soft[...,None]

# ---------------- WETSUIT ----------------
collar=[(0,300),(350,300),(360,440),(470,440),(505,458),(520,498),(545,512),(580,520),(615,512),(645,498),(660,470),(760,470),(1086,470)]
collar_y=np.interp(xs,[p[0] for p in collar],[p[1] for p in collar])
head_zone=(ys<collar_y)
lwrist=((357,492),unit((0.958,0.287)));   lhand=(~halfplane(*lwrist))&(xs>=185)&(xs<=405)&(ys>=380)&(ys<=550)
rwrist=((837.5,665),unit((0.507,0.862)));  rhand=halfplane(*rwrist)&(xs>=760)&(xs<=985)&(ys>=625)&(ys<=800)&~navy
lankle=((508,982),unit((-0.25,0.97)));   lfoot=halfplane(*lankle)&(xs>=395)&(xs<=605)&(ys>=960)&(ys<=1080)
rankle=((752,1097),unit((0.44,0.90)));   rfoot=halfplane(*rankle)&(xs>=625)&(xs<=860)&(ys>=1075)&(ys<=1220)
excl=head_zone|lhand|rhand|lfoot|rfoot
shorts_poly=[(515,690),(560,678),(650,676),(700,668),(740,652),(775,672),(788,725),(792,790),(784,880),(742,916),(690,902),(640,870),(610,830),(580,850),(540,880),(495,885),(455,850),(465,780),(495,715)]
shorts_region=poly_mask(shorts_poly)
suit_raw=(skin|(navy&shorts_region))&~excl
suit_raw=cv2.morphologyEx(to_u8(suit_raw),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))>0
from scipy import ndimage
suit_raw=ndimage.binary_fill_holes(suit_raw)
suit=cv2.dilate(to_u8(suit_raw),np.ones((3,3),np.uint8))>0
suit=suit&opaque&~(bluewater&~shorts_region)&~excl
# keep the gold chain: corridor + colour test
chain=[(526,488),(530,505),(537,520),(543,535),(549,548),(558,558),(570,567),(592,578),(614,568),(626,558),(634,546),(642,533),(650,520),(657,505),(661,492)]
corr=np.zeros((H,W),np.uint8); cv2.polylines(corr,[np.array(chain,np.int32)],False,255,22); corr=corr>0
gold=corr&(((Hh>=17)&(S>=80))|((V>=246)&(S<130))|(V<140))
suit=suit&~gold
# regions
lseam=((503,508),(522,582)); rseam=((672,522),(655,612))
def side(seg,outward):
    d=unit((seg[1][0]-seg[0][0],seg[1][1]-seg[0][1])); n=(-d[1],d[0])
    if n[0]*outward[0]+n[1]*outward[1]<0: n=(-n[0],-n[1])
    mid=((seg[0][0]+seg[1][0])/2,(seg[0][1]+seg[1][1])/2)
    return halfplane(mid,n)
lsleeve=side(lseam,(-1,0))&(ys<650)&(xs<560)&~((ys>582+(522-xs)*0.28+8)&(xs<560))
rsleeve=side(rseam,(1,0))&(ys<760)&(xs>600)&~((ys>612+(xs-655)*0.36+8)&(xs<795))
skin_strict=(Hh>=3)&(Hh<=22)&(S>=90)&(V>=120)
sleeves=suit&(lsleeve|rsleeve)
shorts=suit&shorts_region&~skin_strict&~sleeves
shorts=cv2.dilate(to_u8(shorts),np.ones((3,3),np.uint8))>0
skin_strict=(Hh>=3)&(Hh<=22)&(S>=90)&(V>=120)
shorts=shorts&suit&shorts_region&~skin_strict
body=suit&~sleeves&~shorts

def ramp(t,stops):
    t=np.clip(t,0,1); xs_=[s[0] for s in stops]; cols=np.array([s[1] for s in stops],np.float32)
    r=np.stack([np.interp(t,xs_,cols[:,i]) for i in range(3)],-1); return r
def rgb(h): return (int(h[4:6],16),int(h[2:4],16),int(h[0:2],16))  # returns BGR
ORANGE=[(0.0,rgb("4A1603")),(0.28,rgb("B83D08")),(0.55,rgb("F26A1B")),(0.82,rgb("FF9A4C")),(1.0,rgb("FFDCB8"))]
GLACIER=[(0.0,rgb("1E4653")),(0.18,rgb("3F7F91")),(0.4,rgb("86C1CF")),(0.62,rgb("BDE1E9")),(0.85,rgb("E6F4F7")),(1.0,rgb("FFFFFF"))]
t_skin=(lum-95.)/(252.-95.)
sl=lum.copy()
lum_s=cv2.bilateralFilter(lum.astype(np.float32),9,18,6)
t_shorts=(lum_s-12.)/(150.-12.)
suit_col=np.zeros_like(bgr)
suit_col[body]=ramp(t_skin,ORANGE)[body]
suit_col[sleeves]=ramp(t_skin,GLACIER)[sleeves]
suit_col[shorts]=ramp(t_shorts,GLACIER)[shorts]
suit_soft=cv2.GaussianBlur(to_u8(suit),(0,0),0.7)/255.
suit_soft=suit_soft*(suit|cv2.dilate(to_u8(suit),np.ones((3,3),np.uint8)).astype(bool))
# blend by soft mask, but only where we computed a colour (dilated pixels take nearest colour via blur of colour*mask)
num=cv2.GaussianBlur(suit_col*suit[...,None],(0,0),1.2); den=cv2.GaussianBlur(suit.astype(np.float32),(0,0),1.2)
suit_fill=np.where(den[...,None]>1e-3,num/np.maximum(den,1e-3)[...,None],suit_col)
out=out*(1-suit_soft[...,None])+suit_fill*suit_soft[...,None]

# ---------------- SEAMS ----------------
seamc=(0x24,0x22,0x20)
seam_layer=np.zeros((H,W),np.uint8)
def walk(p0,d,mask,maxlen=140):
    """from p0 walk +-d while mask true; returns endpoints"""
    ends=[]
    for sgn in (1,-1):
        last=p0; miss=0
        for t in range(1,maxlen):
            x=int(round(p0[0]+sgn*t*d[0])); y=int(round(p0[1]+sgn*t*d[1]))
            if 0<=x<W and 0<=y<H and mask[y,x]: last=(x,y); miss=0
            else:
                miss+=1
                if miss>2: break
        ends.append(last)
    return ends
suit_or_skin=suit|skin
for (p0,d),ml in ((lwrist,48),(rwrist,52),(lankle,60),(rankle,62)):
    n=(-d[1],d[0]); a,b=walk(p0,n,suit_or_skin,ml); cv2.line(seam_layer,(int(a[0]),int(a[1])),(int(b[0]),int(b[1])),255,3,cv2.LINE_AA)
for seg in (lseam,rseam):
    d=unit((seg[1][0]-seg[0][0],seg[1][1]-seg[0][1])); mid=((seg[0][0]+seg[1][0])/2,(seg[0][1]+seg[1][1])/2)
    a,b=walk(mid,d,suit_or_skin,90); cv2.line(seam_layer,a,b,255,3,cv2.LINE_AA)
cv2.polylines(seam_layer,[np.array(collar,np.int32)],False,255,3,cv2.LINE_AA)
seam_m=(seam_layer/255.)*suit_or_skin*(cv2.dilate(to_u8(suit),np.ones((5,5),np.uint8))/255.)
out=out*(1-seam_m[...,None]*0.85)+np.array(seamc,np.float32)*seam_m[...,None]*0.85

# ---------------- WARPS (head + left hand shrink) ----------------
res=np.dstack([out*alpha[...,None],alpha*255]).astype(np.float32)  # premultiplied
def pinch(img,center,anchor,r0,r1,f):
    d=np.hypot(xs-center[0],ys-center[1])
    w=np.clip((r1-d)/(r1-r0),0,1); w=w*w*(3-2*w)   # smoothstep: 1 inside r0, 0 outside r1
    fac=1.0/(1+(f-1)*w)          # scale about anchor: p -> anchor+(p-anchor)*f  => inverse: /f
    mx=(anchor[0]+(xs-anchor[0])*fac).astype(np.float32); my=(anchor[1]+(ys-anchor[1])*fac).astype(np.float32)
    return cv2.remap(img,mx,my,cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
res=pinch(res,center=(578,250),anchor=(580,472),r0=235,r1=305,f=0.87)
res=pinch(res,center=(282,463),anchor=(358,492),r0=92,r1=128,f=0.86)
a=np.clip(res[...,3:4],0,255); col=np.where(a>0.5,res[...,:3]/np.maximum(a,1e-3)*255,0)
# defringe: semi-transparent edge pixels take the colour of neighbouring opaque pixels
solid=(a[...,0]>247).astype(np.float32)
cnum=cv2.GaussianBlur(col*solid[...,None],(0,0),2.5); cden=cv2.GaussianBlur(solid,(0,0),2.5)
edge=((a[...,0]>0.5)&(a[...,0]<=247)&(cden>0.03))
col=np.where(edge[...,None],cnum/np.maximum(cden,1e-3)[...,None],col)
final=np.dstack([np.clip(col,0,255),a]).astype(np.uint8)
cv2.imwrite(OUT,final,[cv2.IMWRITE_PNG_COMPRESSION,9])
print("done",OUT)

# ---------------- DEBUG overlay ----------------
if not args.debug: raise SystemExit(0)
dbg=(bgr*alpha[...,None]+200*(1-alpha[...,None])).astype(np.uint8).copy()
ov=dbg.copy()
ov[body]=(0,120,255); ov[sleeves]=(230,220,120); ov[shorts]=(200,160,60); ov[board]=(160,60,200); ov[gold&corr]=(0,255,255)
dbg=cv2.addWeighted(dbg,0.45,ov,0.55,0)
cv2.polylines(dbg,[np.array(board_poly,np.int32)],True,(0,255,0),1)
cv2.polylines(dbg,[np.array(shorts_poly,np.int32)],True,(255,0,255),1)
cv2.polylines(dbg,[np.array(collar,np.int32)],False,(0,0,255),1)
for p in (N,T,Fp,Qp): cv2.circle(dbg,(int(p[0]),int(p[1])),5,(0,0,255),-1)
dbg[seam_layer>128]=(0,0,255)
cv2.imwrite(os.path.join(os.path.dirname(OUT) or ".","debug.png"),dbg)
comp=(final[...,:3]*(final[...,3:4]/255.)+200*(1-final[...,3:4]/255.)).astype(np.uint8)
cv2.imwrite(os.path.join(os.path.dirname(OUT) or ".","out_comp.png"),comp)

