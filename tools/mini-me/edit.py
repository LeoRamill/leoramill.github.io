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
tex_a=cv2.GaussianBlur(cv2.resize(tex,(Wt//2,L//2),interpolation=cv2.INTER_AREA),(0,0),0.8)
tex_b=cv2.GaussianBlur(tex_a,(0,0),2.6)          # mip used where the print compresses over the rail
pts=np.stack([xs,ys,np.ones_like(xs)],-1).reshape(-1,3)@Hinv.T
pts=pts[:,:2]/pts[:,2:3]
TV=pts[:,0].reshape(H,W); TU=pts[:,1].reshape(H,W)     # across (0..Wt) and along (0..L) the board

# ---- outline in board space: centre line and half width at every station ----
NB=200; idx=np.arange(NB)
ub=np.clip((TU/L*NB).astype(int),0,NB-1)
vlo=np.full(NB,np.nan); vhi=np.full(NB,np.nan)
for i in range(NB):
    m=board_region&(ub==i)
    if m.sum()>40:
        v=TV[m]; vlo[i]=np.percentile(v,0.4); vhi[i]=np.percentile(v,99.6)
ok=~np.isnan(vlo)
vlo=np.interp(idx,idx[ok],vlo[ok]); vhi=np.interp(idx,idx[ok],vhi[ok])
ker=np.ones(9)/9.
vlo=np.convolve(np.pad(vlo,4,mode="edge"),ker,"valid"); vhi=np.convolve(np.pad(vhi,4,mode="edge"),ker,"valid")
station=np.clip(TU/L*NB,0,NB-1)
vcen=(np.interp(station,idx,vlo)+np.interp(station,idx,vhi))/2.
half=np.maximum((np.interp(station,idx,vhi)-np.interp(station,idx,vlo))/2.,1.)

# ---- cross-section: flat deck closed by a quarter-round rail of radius Rr ----
side=np.where(TV>=vcen,1.,-1.)                            # +1 near rail (lower left), -1 far rail
Rr=np.where(side>0,76.,22.)                               # the far rail is foreshortened to a sliver
dist=np.maximum(half-np.abs(TV-vcen),0.)                  # distance inward from the outline
q=np.clip(dist/Rr,0,1)
slope=np.minimum((1-q)/np.sqrt(np.maximum(q*(2-q),1e-4)),7.0)   # |dh/dd|: 0 on the deck, vertical at the edge
crown=0.62*np.clip(np.abs(TV-vcen)/half,0,1)**1.6         # the deck itself is gently domed
nx=-side*(slope+crown); nn=np.sqrt(nx*nx+1.); nx=nx/nn; nz=1./nn  # surface normal in the cross plane

# ---- the print is painted on the surface, so it maps by arc length and squeezes over the rail ----
arc=np.where(dist<Rr,Rr*np.arccos(np.clip(1-q,-1,1)),Rr*(np.pi/2)+(dist-Rr))
half_arc=(half-Rr)+Rr*np.pi/2
kscale=(Wt/2.)/float(np.nanmax(np.where(board_region,half_arc,np.nan)))
v_tex=Wt/2.+side*(half_arc-arc)*kscale
mapx=(v_tex/2).astype(np.float32); mapy=(TU/2).astype(np.float32)
pa=cv2.remap(tex_a,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
pb=cv2.remap(tex_b,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
mip=np.clip((np.sqrt(1+slope**2)-1.35)/1.6,0,1)[...,None]
patt=pa*(1-mip)+pb*mip

# ---- foam rail: like the reference board, the print stops short of the edge ----
def smoothstep(e0,e1,x):
    t=np.clip((x-e0)/(e1-e0),0,1); return t*t*(3-2*t)
railmix=smoothstep(0.24,0.52,q)[...,None]
FOAM=np.array([246,248,250],np.float32)
base=patt*railmix+FOAM*(1-railmix)
under=(smoothstep(0.30,0.0,q)*(side>0))[...,None]         # the rail turns under and picks up the water
base=base*(1-0.40*under)+np.array([196,156,96],np.float32)*0.40*under
pin=(np.exp(-((q-0.54)/0.07)**2)*(side>0))[...,None]      # thin shadow where the print meets the rail
base=base*(1-0.16*pin)

# ---- lighting: diffuse across the curved section, gloss, and a fresnel rim at the silhouette ----
def _n(v): v=np.array(v,float); return v/np.linalg.norm(v)
Lv=_n([-0.40,-0.55,0.73]); Vv=_n([0.30,-0.12,0.95]); Hv=_n(Lv+Vv)
kd=(0.44+0.56*np.clip(nx*Lv[0]+nz*Lv[2],0,1))/(0.44+0.56*Lv[2])
ndh=np.clip(nx*Hv[0]+nz*Hv[2],0,1)
gloss=0.55*ndh**60+0.09*ndh**10
fres=np.clip(1-np.clip(nx*Vv[0]+nz*Vv[2],0,1),0,1)**2.6
along=0.40+0.60*np.exp(-((TU/L-0.46)/0.40)**2)            # the highlight fades towards nose and tail
rim=0.22*fres+0.66*along*np.exp(-((q-0.44)/0.15)**2)*(side>0)   # specular line along the near rail
u_c=np.clip((TV-vcen)/half,-1,1)
sheen=0.11*np.exp(-((u_c+0.18)/0.44)**2)*np.exp(-((TU/L-0.40)/0.55)**2)   # broad gloss over the deck

# ---- keep the render's own light: the wave's cast shadow and the overall gradient ----
# the old deck had lengthwise stripes of two tones: take the local upper envelope of V so the
# estimate follows the light and not the stripes (the kernel spans the width, where they alternate)
Vb=np.where(board_region&~skin_core,V,0).astype(np.float32)
illum=cv2.dilate(Vb,cv2.getStructuringElement(cv2.MORPH_RECT,(41,111)))
bmf=board_region.astype(np.float32)
illum=np.where(cv2.GaussianBlur(bmf,(0,0),16)>1e-3,
               cv2.GaussianBlur(illum*bmf,(0,0),16)/np.maximum(cv2.GaussianBlur(bmf,(0,0),16),1e-3),0.)
ref=float(np.percentile(illum[board_region],86))
shade=np.clip(illum/max(ref,1e-3),0.62,1.12)
shade=np.clip(1.+(shade-1.)*1.25,0.60,1.15)               # the render's own light on the board
# the boy's legs drop a shadow onto the deck, thrown away from the light
caster=cv2.GaussianBlur((skin|navy).astype(np.float32),(0,0),3)
caster=cv2.warpAffine(caster,np.float32([[1,0,17],[0,1,25]]),(W,H))
legsh=np.clip(cv2.GaussianBlur(caster,(0,0),11)*1.5,0,1)*(1-cv2.GaussianBlur((skin|navy).astype(np.float32),(0,0),1.5))
shade=shade*(1-0.30*legsh)

new_board=base*(shade*kd)[...,None]
g=np.clip((gloss+0.55*rim+sheen),0,0.92)[...,None]
new_board=255-(255-new_board)*(1-g)
# contact shadow of the feet on the deck, thrown away from the light
feet=(skin_core&board_region).astype(np.float32)
ao=cv2.warpAffine(cv2.GaussianBlur(feet,(0,0),7),np.float32([[1,0,6],[0,1,7]]),(W,H))
ao=np.clip(ao*1.9,0,1)*(1-feet)
new_board=np.clip(new_board*(1-0.42*ao)[...,None],0,255)
board_soft=cv2.GaussianBlur(to_u8(board),(0,0),0.9)/255.
out=bgr.copy()
out=out*(1-board_soft[...,None])+new_board*board_soft[...,None]
# ---- the board has thickness: a side wall hangs under the near silhouette ----
col_has=board_region.any(0); xcol=np.arange(W,dtype=np.float32)
ymax=np.where(col_has,H-1-np.argmax(board_region[::-1],0),np.nan).astype(np.float32)
okc=~np.isnan(ymax)
ymax_s=ymax.copy()
ymax_s[okc]=np.convolve(np.pad(ymax[okc],7,mode="edge"),np.ones(15)/15.,"valid")   # smooth, sub-pixel edge
ymax_s=np.where(okc,ymax_s,-1e6)
thick=13.0+15.0*np.clip((xcol-float(N[0]))/(float(T[0])-float(N[0])),0,1)   # the tail is nearer, so it reads thicker
dep=np.clip((ys-ymax_s[None,:])/thick[None,:],0,1)
wall_a=np.clip(ys-ymax_s[None,:],0,1)*np.clip(ymax_s[None,:]+thick[None,:]-ys,0,1)
wall_a=wall_a*(~board_region)*(~skin_core)*(okc[None,:])
wall_a=np.clip(cv2.GaussianBlur(wall_a,(0,0),0.7),0,1)*(~board_region)*(~skin_core)
wall=wall_a>0.5
# the wall continues the colour of the pixel right above it, so rail and wall stay one surface
erow=np.clip(np.round(ymax_s)-1,0,H-1).astype(int)
edge_col=out[erow,np.arange(W)]                                  # (W,3)
ramp=(1.0-0.52*dep**1.15)
wtint=np.clip((dep-0.40)/0.60,0,1)*0.45
wcol=edge_col[None,:,:]*ramp[...,None]*(1-wtint[...,None])+np.array([176,132,74],np.float32)*wtint[...,None]
bounce=0.26*np.exp(-((dep-0.88)/0.11)**2)                        # light bouncing up off the water
wcol=255-(255-wcol)*(1-bounce[...,None])
out=out*(1-wall_a[...,None])+np.clip(wcol,0,255)*wall_a[...,None]
alpha=np.maximum(alpha,wall_a)
# ---- the board sits IN the wave: contact shadow thrown onto the water below it ----
bm=np.clip(board_region.astype(np.float32)+wall_a,0,1)*(alpha>0.05)
drop=cv2.warpAffine(cv2.GaussianBlur(bm,(0,0),11),np.float32([[1,0,9],[0,1,13]]),(W,H))
occ=cv2.GaussianBlur(bm,(0,0),5)
edge_ao=np.clip(cv2.GaussianBlur(bm,(0,0),3.2)*1.7,0,1)                 # the board occludes the wave behind it
cast=np.clip(np.maximum(np.maximum(0.66*drop,0.44*occ),0.62*edge_ao),0,1)*(1-cv2.GaussianBlur(bm,(0,0),1.0))
cast=cast*(1-np.clip(wall_a*1.6,0,1))*(~board_region)*(~skin)*(alpha>0.05)
out=out*(1-0.40*cast)[...,None]
if os.environ.get("BDEBUG"):
    dd=os.path.dirname(OUT) or "."
    for nm,fld,sc in (("q",q,255),("kd",kd*128,1),("shade",shade*128,1),("rim",rim*255,1),("cast",cast*255,1),("dep",dep*255,1)):
        cv2.imwrite(os.path.join(dd,f"dbg_{nm}.png"),np.clip(fld*sc if sc!=1 else fld,0,255).astype(np.uint8))

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

