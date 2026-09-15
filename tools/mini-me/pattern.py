"""Procedural 90s 'aztec / tribal' surfboard deck print (teal, pink, purple, black, cream).
Texture space: u = along the board length (rows), v = across the width (cols)."""
import cv2, numpy as np, math

TEAL=(0x62,0xC8,0xC4); AQUA=(0x9A,0xDE,0xDA); PINK=(0xE9,0xA8,0xCB); MAUVE=(0xC2,0x7A,0xAB)
PURPLE=(0x3E,0x3C,0x8E); INDIGO=(0x2A,0x27,0x66); BLACK=(0x17,0x17,0x1A); CREAM=(0xF4,0xF0,0xEA)
def bgr(c): return (int(c[2]),int(c[1]),int(c[0]))
AA=cv2.LINE_AA

def band_teeth(img,y0,y1,W):            # black band, white triangles
    cv2.rectangle(img,(0,y0),(W,y1),bgr(BLACK),-1)
    hgt=y1-y0; step=hgt*1.2
    for x in np.arange(0,W+step,step):
        pts=np.array([[x,y1-3],[x+step/2,y0+3],[x+step,y1-3]],np.int32)
        cv2.fillPoly(img,[pts],bgr(CREAM),AA)
def band_hooks(img,y0,y1,W,bgc,fg):     # spiral 'hook' meander
    cv2.rectangle(img,(0,y0),(W,y1),bgr(bgc),-1)
    hgt=y1-y0; t=max(3,hgt//7); step=int(hgt*1.15)
    for x in range(0,W+step,step):
        # a squared spiral drawn as polyline
        m=int(hgt*0.15)
        p=[(x+m,y1-m),(x+m,y0+m),(x+step-2*m,y0+m),(x+step-2*m,y1-2*m),(x+2*m+t,y1-2*m),(x+2*m+t,y0+2*m+t),(x+step-3*m-t,y0+2*m+t)]
        cv2.polylines(img,[np.array(p,np.int32)],False,bgr(fg),t,AA)
def band_diamonds(img,y0,y1,W,bgc,fg,inner):
    cv2.rectangle(img,(0,y0),(W,y1),bgr(bgc),-1)
    hgt=y1-y0; step=int(hgt*1.9); cy=(y0+y1)//2
    for x in range(-step,W+step,step):
        pts=np.array([[x,cy],[x+step//2,y0+2],[x+step,cy],[x+step//2,y1-2]],np.int32)
        cv2.fillPoly(img,[pts],bgr(fg),AA)
        s=0.45; pts2=np.array([[x+step//2-step*s/2,cy],[x+step//2,cy-(hgt//2-2)*s],[x+step//2+step*s/2,cy],[x+step//2,cy+(hgt//2-2)*s]],np.int32)
        cv2.fillPoly(img,[pts2],bgr(inner),AA)
    cv2.line(img,(0,y0),(W,y0),bgr(fg),2); cv2.line(img,(0,y1),(W,y1),bgr(fg),2)
def band_zigzag(img,y0,y1,W,bgc,zig,tri):
    cv2.rectangle(img,(0,y0),(W,y1),bgr(bgc),-1)
    hgt=y1-y0; step=int(hgt*1.1); t=max(3,hgt//6)
    pts=[]
    for i,x in enumerate(range(-step,W+2*step,step//2)):
        pts.append([x,y0+t if i%2==0 else y1-t])
    cv2.polylines(img,[np.array(pts,np.int32)],False,bgr(zig),t,AA)
    for i,x in enumerate(range(-step,W+2*step,step)):   # small triangles in the valleys
        p=np.array([[x+step//2-step//5,y1-2],[x+step//2,y1-hgt//3],[x+step//2+step//5,y1-2]],np.int32)
        cv2.fillPoly(img,[p],bgr(tri),AA)
def band_stripes(img,y0,y1,W,cols):
    n=len(cols); hgt=(y1-y0)/n
    for i,c in enumerate(cols): cv2.rectangle(img,(0,int(y0+i*hgt)),(W,int(y0+(i+1)*hgt)),bgr(c),-1)

# --- motifs (drawn inside a square (x0,y0,s)) ---
def m_pineapple(img,x0,y0,s):
    cx=x0+s//2; body=(cx,int(y0+s*0.62)); ax=(int(s*0.22),int(s*0.30))
    cv2.ellipse(img,body,ax,0,0,360,bgr(BLACK),-1,AA)
    cv2.ellipse(img,body,(ax[0]-4,ax[1]-4),0,0,360,bgr(CREAM),-1,AA)
    for k in range(-3,4):   # crosshatch
        d=int(k*s*0.09)
        cv2.line(img,(body[0]-ax[0]+d,body[1]+ax[1]),(body[0]+ax[0]+d,body[1]-ax[1]),bgr(BLACK),2,AA)
        cv2.line(img,(body[0]-ax[0]+d,body[1]-ax[1]),(body[0]+ax[0]+d,body[1]+ax[1]),bgr(BLACK),2,AA)
    cv2.ellipse(img,body,ax,0,0,360,bgr(BLACK),3,AA)
    # crown leaves
    for ang in (-60,-35,-12,12,35,60):
        L=s*0.30; a=math.radians(ang-90)
        tip=(int(cx+L*math.cos(a)),int(y0+s*0.34+L*math.sin(a)))
        base=(cx,int(y0+s*0.36)); w=int(s*0.05)
        pts=np.array([[base[0]-w,base[1]],[tip[0],tip[1]],[base[0]+w,base[1]]],np.int32)
        cv2.fillPoly(img,[pts],bgr(BLACK),AA)
def m_waves(img,x0,y0,s):
    for r in range(3):
        cy=int(y0+s*(0.3+0.2*r)); pts=[]
        for x in range(x0+int(s*0.12),x0+int(s*0.88)):
            pts.append([x,int(cy+math.sin((x-x0)/s*2*math.pi*2.2)*s*0.05)])
        cv2.polylines(img,[np.array(pts,np.int32)],False,bgr(BLACK),max(3,s//18),AA)
def m_fish(img,x0,y0,s):
    cx=x0+int(s*0.47); cy=y0+int(s*0.42)
    cv2.ellipse(img,(cx,cy),(int(s*0.27),int(s*0.13)),0,0,360,bgr(BLACK),-1,AA)
    tail=np.array([[cx+int(s*0.22),cy],[cx+int(s*0.40),cy-int(s*0.15)],[cx+int(s*0.40),cy+int(s*0.15)]],np.int32)
    cv2.fillPoly(img,[tail],bgr(BLACK),AA)
    cv2.circle(img,(cx-int(s*0.15),cy-int(s*0.02)),max(2,s//30),bgr(CREAM),-1,AA)
    for r in range(2):
        yy=int(y0+s*(0.66+0.14*r)); pts=[]
        for x in range(x0+int(s*0.12),x0+int(s*0.88)):
            pts.append([x,int(yy+math.sin((x-x0)/s*2*math.pi*2.5)*s*0.04)])
        cv2.polylines(img,[np.array(pts,np.int32)],False,bgr(BLACK),max(3,s//20),AA)
def m_palm(img,x0,y0,s):
    bx=x0+int(s*0.52); by=y0+int(s*0.90); top=(x0+int(s*0.46),y0+int(s*0.36))
    cv2.line(img,(bx,by),top,bgr(BLACK),max(4,s//12),AA)
    for ang in (200,235,270,305,340,20):
        a=math.radians(ang); L=s*0.30
        mid=(int(top[0]+L*0.6*math.cos(a)),int(top[1]+L*0.6*math.sin(a)-s*0.06))
        end=(int(top[0]+L*math.cos(a)),int(top[1]+L*math.sin(a)+s*0.08))
        cv2.polylines(img,[np.array([top,mid,end],np.int32)],False,bgr(BLACK),max(4,s//12),AA)
    cv2.circle(img,top,max(3,s//16),bgr(BLACK),-1,AA)
def m_hibiscus(img,x0,y0,s):
    cx=x0+s//2; cy=y0+s//2
    for k in range(5):
        a=math.radians(k*72-90); c=(int(cx+s*0.20*math.cos(a)),int(cy+s*0.20*math.sin(a)))
        cv2.ellipse(img,c,(int(s*0.17),int(s*0.11)),k*72-90,0,360,bgr(BLACK),-1,AA)
    cv2.circle(img,(cx,cy),int(s*0.07),bgr(CREAM),-1,AA)
    cv2.line(img,(cx,cy),(cx+int(s*0.18),cy-int(s*0.22)),bgr(CREAM),2,AA)

MOTIFS={'pine':(m_pineapple,TEAL),'wave':(m_waves,PINK),'fish':(m_fish,AQUA),'palm':(m_palm,CREAM),'hib':(m_hibiscus,PINK)}
def motif_row(img,y0,y1,W,names,gapc):
    cv2.rectangle(img,(0,y0),(W,y1),bgr(gapc),-1)
    n=len(names); cell=W/n; s=int(cell*0.84); pad=int((cell-s)/2)
    for i,nm in enumerate(names):
        fn,bgc=MOTIFS[nm]; x0=int(i*cell+pad); yy=y0+((y1-y0)-s)//2
        cv2.rectangle(img,(x0-6,yy-6),(x0+s+6,yy+s+6),bgr(PURPLE),-1)   # frame
        cv2.rectangle(img,(x0,yy),(x0+s,yy+s),bgr(bgc),-1)
        # dotted inner border
        for d in range(8,s-8,12):
            for (px,py) in ((x0+d,yy+5),(x0+d,yy+s-5),(x0+5,yy+d),(x0+s-5,yy+d)): cv2.circle(img,(px,py),2,bgr(BLACK),-1)
        fn(img,x0,yy,s)

def make_texture(L=2000,W=800):
    img=np.zeros((L,W,3),np.uint8); img[:]=bgr(CREAM)
    seq=[('teeth',34),('hooks_pink',72),('diam_cream',58),('zig_purple',86),('motif_a',210),('hooks_teal',56),('stripes',44),
         ('teeth',34),('diam_black',60),('zig_pink',86),('motif_b',210),('hooks_indigo',64),('stripes2',44)]
    y=0; k=0
    while y<L:
        name,hgt=seq[k%len(seq)]; y1=min(L,y+hgt)
        if name=='teeth': band_teeth(img,y,y1,W)
        elif name=='hooks_pink': band_hooks(img,y,y1,W,PINK,BLACK)
        elif name=='hooks_teal': band_hooks(img,y,y1,W,TEAL,BLACK)
        elif name=='hooks_indigo': band_hooks(img,y,y1,W,INDIGO,AQUA)
        elif name=='diam_cream': band_diamonds(img,y,y1,W,CREAM,BLACK,MAUVE)
        elif name=='diam_black': band_diamonds(img,y,y1,W,BLACK,PINK,PURPLE)
        elif name=='zig_purple': band_zigzag(img,y,y1,W,PURPLE,CREAM,TEAL)
        elif name=='zig_pink': band_zigzag(img,y,y1,W,MAUVE,BLACK,CREAM)
        elif name=='motif_a': motif_row(img,y,y1,W,['pine','wave','fish'],PINK)
        elif name=='motif_b': motif_row(img,y,y1,W,['hib','palm','pine'],TEAL)
        elif name=='stripes': band_stripes(img,y,y1,W,[PURPLE,CREAM,BLACK,PINK,BLACK,CREAM,PURPLE])
        elif name=='stripes2': band_stripes(img,y,y1,W,[TEAL,BLACK,CREAM,MAUVE,CREAM,BLACK,TEAL])
        y=y1; k+=1
    return img
if __name__=="__main__":
    t=make_texture(); cv2.imwrite("texture.png",t)
    cv2.imwrite("texture_preview.png",cv2.resize(t[:1000],None,fx=0.6,fy=0.6,interpolation=cv2.INTER_AREA))
    print(t.shape)
