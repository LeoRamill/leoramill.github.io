"""Rimette in proporzione testa e corpo del mini-me e ripristina lo sfondo trasparente.

Vale per il render del surfista con muta blu/arancio e occhiali (quello introdotto dal
commit "change photo"), non per il render precedente trattato da edit.py.

La testa viene rimpicciolita con una deformazione morbida ancorata al punto in cui il mento
appoggia sul collo della muta: dentro la maschera della testa la scala e' piena, fuori e'
identita', e la fascia di transizione cade sullo sfondo bianco e sulle spalle, dove lo
stiramento non si vede. Non ci sono buchi da riempire perche' il campo e' continuo.

    python3 tools/mini-me/headscale.py assets/media/mini-me.png assets/media/mini-me.png
"""
import cv2, numpy as np, argparse
from scipy import ndimage

# silhouette della testa misurata sul render (pixel dell'immagine 1086x1448)
HEAD_POLY=[(534,16),(580,18),(628,40),(668,68),(700,104),(720,148),(730,196),(724,244),(714,292),
           (702,338),(688,382),(672,420),(660,452),(642,478),(616,500),(586,512),
           (505,512),(478,500),(456,478),(440,452),(424,420),(408,382),(392,338),(378,292),
           (366,244),(352,196),(340,148),(360,104),(392,68),(432,40),(480,18)]
PIVOT=(545.,505.)          # mento sul collo della muta: resta fermo
FACE_BOX=(0,520,330,745)   # y0,y1,x0,x1 in cui cercare pelle e capelli

def head_mask(img):
    H,W=img.shape[:2]
    hsv=cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_BGR2HSV)
    Hh,S,V=hsv[...,0].astype(int),hsv[...,1].astype(int),hsv[...,2].astype(int)
    poly=np.zeros((H,W),np.uint8); cv2.fillPoly(poly,[np.array(HEAD_POLY,np.int32)],255)
    y0,y1,x0,x1=FACE_BOX
    box=np.zeros((H,W),bool); box[y0:y1,x0:x1]=True
    cand=(((Hh>=3)&(Hh<=25)&(S>=45)&(V>=95))|(V<90))&box     # pelle, capelli, occhiali
    n,lab,_,_=cv2.connectedComponentsWithStats(cand.astype(np.uint8))
    m=ndimage.binary_fill_holes((poly>0)|(lab==lab[300,532]))
    return cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))>0

def scale_head(img,s,sigma=10.):
    H,W=img.shape[:2]; ys,xs=np.mgrid[0:H,0:W].astype(np.float32)
    w=np.clip(cv2.GaussianBlur(head_mask(img).astype(np.float32),(0,0),sigma)*1.30,0,1)
    f=1.+(s-1.)*w                                            # 1 sul corpo, s sulla testa
    px,py=PIVOT
    mx=(px+(xs-px)/f).astype(np.float32); my=(py+(ys-py)/f).astype(np.float32)
    return np.clip(cv2.remap(img,mx,my,cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE),0,255)

def cut_white(img,d0=6.,d1=32.):
    """Sfondo bianco -> alpha, con i bordi smontati dal bianco per non lasciare aloni.

    Lo sfondo del render e' perfettamente piatto (escursione locale <=2), mentre la schiuma
    dell'onda e il bianco della tavola sono superfici illuminate (escursione ~15). La planarita'
    distingue quindi le sacche di sfondo chiuse dentro la figura, per esempio i vuoti fra i
    ciuffi di capelli o quello fra le gambe, che il riempimento dai bordi non raggiunge.
    """
    H,W=img.shape[:2]
    hsv=cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_BGR2HSV)
    S,V=hsv[...,1].astype(int),hsv[...,2].astype(int)
    d=np.maximum(S,255-V).astype(np.float32)
    near=(d<=8).astype(np.uint8)
    ff=near.copy(); mask=np.zeros((H+2,W+2),np.uint8)
    for seed in ((0,0),(W-1,0),(0,H-1),(W-1,H-1)):
        if ff[seed[1],seed[0]]: cv2.floodFill(ff,mask,seed,2)
    ext=(ff==2)
    g=cv2.cvtColor(img.astype(np.uint8),cv2.COLOR_BGR2GRAY); k3=np.ones((3,3),np.uint8)
    flat=(cv2.dilate(g,k3).astype(int)-cv2.erode(g,k3).astype(int))<=2
    pockets=ndimage.binary_propagation((d<=4)&flat&(~ext),mask=near>0)
    # la carta e' neutra (saturazione media ~0.1), i bianchi dell'onda tirano al blu (~2.4):
    # tengo solo le sacche neutre, cosi' la schiuma e il bianco della tavola restano pieni
    bmr=(img[...,0]-img[...,2]).astype(np.float32)
    n,lab,st,_=cv2.connectedComponentsWithStats(pockets.astype(np.uint8))
    keep=np.zeros_like(pockets)
    for i in range(1,n):
        if st[i,cv2.CC_STAT_AREA]<20: continue
        c=lab==i
        if S[c].mean()<=1.2 and abs(float(bmr[c].mean()))<=1.0: keep|=c
    ext=ext|keep
    zone=cv2.dilate(ext.astype(np.uint8),np.ones((9,9),np.uint8))>0
    # lo sfondo del render ha d<=2, la figura d>=110: la rampa cade tutta sul bordo sfumato
    a=np.where(zone,np.clip((d-d0)/(d1-d0),0,1),1.).astype(np.float32)
    a3=a[...,None]
    col=np.where(a3>0.02,(img-255.*(1.-a3))/np.maximum(a3,0.02),img)
    return np.dstack([np.clip(col,0,255),a*255.]).astype(np.uint8)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--scale",type=float,default=0.70,help="fattore di riduzione della testa")
    ap.add_argument("--keep-white",action="store_true",help="non ritagliare lo sfondo bianco")
    a=ap.parse_args()
    im=cv2.imread(a.src,cv2.IMREAD_UNCHANGED)
    if im.shape[2]==4:
        al=im[...,3:4]/255.; im=im[...,:3]*al+255*(1-al)
    im=im[...,:3].astype(np.float32)
    r=scale_head(im,a.scale)
    r=r.astype(np.uint8) if a.keep_white else cut_white(r)
    cv2.imwrite(a.out,r,[cv2.IMWRITE_PNG_COMPRESSION,9])
    print("scritto",a.out,r.shape)
