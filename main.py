import json as J,os,urllib.request as u
N,E,S,W=-10,1,10,-1
X=(N,E,S,W,N+E,S+E,S+W,N+W)
KN=(-19,-8,12,21,19,8,-12,-21)
D={'P':(N,N+N,N+W,N+E),'N':KN,'B':X[4:],'R':X[:4],'Q':X,'K':X}
P=" "*9+"\n";I=P*2+" rnbqkbnr\n pppppppp\n"+" ........\n"*4+" PPPPPPPP\n RNBQKBNR\n"+P*2
VL=dict(zip('PNBRQK',(100,320,330,500,900,0)))
def V(p,i):
 r=9-i//10;f=i%10-1
 if r//8 or f//8:return 0
 g=min(f,7-f)+min(r,7-r);return 10*r if p=='P' else 3*g-9
T={p:[V(p,i)for i in range(120)]for p in'PNBRQK'}
def A(b,q,w):
 s=1 if w else-1;C,U,K,B,R,Q='PNKBRQ' if w else'pnkbrq'
 if b[q+9*s]==C or b[q+11*s]==C:return 1
 for d in KN:
  if b[q+d]==U:return 1
 for d in X:
  if b[q+d]==K:return 1
 for d in X:
  x=q+d
  while b[x] not in' \n':
   if b[x]!='.':
    if b[x]==Q or(d in X[4:]and b[x]==B)or(d in X[:4]and b[x]==R):return 1
    break
   x+=d
def G(ps):
 b,sc,wc,bc,ep=ps
 for i,p in enumerate(b):
  if p not in'PNBRQK':continue
  for d in D[p]:
   j=i+d
   while 1:
    q=b[j]
    if q in' \nPNBRQKk':break
    if p=='P':
     if d%10==0 and q!='.':break
     if d==2*N and(i<81 or b[i+N]!='.'):break
     if d%10 and q=='.' and j!=ep:break
     if j<29:
      for pr in'NBRQ':yield(i,j,pr)
      break
    yield(i,j,'')
    if p in'PNK' or q in'pnbrqk':break
    j+=d
 if b[95]=='K' and not A(b,95,0):
  if wc[1] and b[98]=='R' and b[96]=='.' and b[97]=='.' and not A(b,96,0) and not A(b,97,0):yield(95,97,'')
  if wc[0] and b[91]=='R' and b[92]=='.' and b[93]=='.' and b[94]=='.' and not A(b,94,0) and not A(b,93,0):yield(95,93,'')
def H(b,i,c):return b[:i]+c+b[i+1:]
def M(ps,mv):
 b,sc,wc,bc,ep=ps;i,j,pr=mv;p=b[i];q=b[j];oe=ep;d=-(VL[p]+T[p][i])
 if q!='.':d+=VL[q.upper()]+T[q.upper()][119-j]
 b=H(H(b,j,p),i,'.');wc=(wc[0] and i!=91,wc[1] and i!=98);bc=(bc[0] and j!=21,bc[1] and j!=28)
 if p=='K':
  wc=(0,0)
  if abs(j-i)==2:
   r=91 if j<i else 98;k=(i+j)//2;d-=VL['R']+T['R'][r];d+=VL['R']+T['R'][k];b=H(H(b,r,'.'),k,'R')
 ep=0
 if p=='P':
  if j<29:b=H(b,j,pr)
  if j-i==2*N:ep=i+N
  if j==oe and q=='.':d+=VL['P']+T['P'][119-(j+S)];b=H(b,j+S,'.')
 d+=VL[pr or p]+T[pr or p][j];nb=b[::-1].swapcase();ne=119-ep if ep else 0;return(nb,-(sc+d),bc,wc,ne)
MT=10**5;MP=128;ND=[0];LM=[0];AB=[0];TT={}
def O(bd,mvs,tt):
 return sorted(mvs,key=lambda m:-(100000 if m==tt else(10000+VL[m[2]] if m[2] else(1000+10*VL[bd[m[1]].upper()]-VL[bd[m[0]]] if bd[m[1]]!='.' else 0))))
def Z(pos,d,a,be,ply):
 bd,sc,wc,bc,ep=pos;k=bd.index('K');chk=A(bd,k,0)
 if chk:d+=1
 ND[0]+=1
 if LM[0] and ND[0]>=LM[0]:AB[0]=1;return 0
 if ply>=MP:return sc
 qs=d<=0;best=-MT-1
 if qs and not chk:
  if sc>=be:return sc
  best=sc
  if sc>a:a=sc
 tt=TT.get(pos,0)
 mvs=[m for m in G(pos) if not qs or chk or bd[m[1]]!='.' or m[2]];mvs=O(bd,mvs,tt);leg=0;bm=0
 for m in mvs:
  np=M(pos,m);nb=np[0]
  if 'k' not in nb or A(nb,nb.index('k'),1):continue
  leg+=1;s=-Z(np,d-1,-be,-a,ply+1)
  if AB[0]:return 0
  if s>best:best=s;bm=m
  if s>a:a=s
  if a>=be:break
 if leg==0:return -MT+ply if chk else(sc if qs else 0)
 if qs:return best
 TT[pos]=bm;return best
def R(pos,nb):
 mvs=list(G(pos))
 if not mvs:return None
 best=mvs[0]
 for d in range(1,65):
  LM[0]=0 if d==1 else nb;AB[0]=0;ND[0]=0;a=-MT-1
  mvs.sort(key=lambda m:m!=TT.get(pos,0))
  for m in mvs:
   q=M(pos,m);b2=q[0]
   if 'k' not in b2 or A(b2,b2.index('k'),1):continue
   s=-Z(q,d-1,-MT-1,-a,1)
   if AB[0]:break
   if s>a:a=s;best=m
  if AB[0]:break
  if a<=-MT:return None
 return best
U=os.getenv('MAKEFUN_ENV_URL')
def P2(p,b):return J.load(u.urlopen(U+p,J.dumps(b).encode()))
def Y(i):return chr(96+i%10)+str(10-i//10)
def q(a):return 4-10*int(a[1])+ord(a[0])
def rp(mvs):
 pos=(I,0,(1,1),(1,1),0);k=0
 for mv in mvs:
  i=q(mv[:2]);j=q(mv[2:4]);pr=mv[4:].upper()
  if k%2:i=119-i;j=119-j
  pos=M(pos,(i,j,pr));k+=1
 return pos,k
while 1:
 g=P2('/game',{})
 if g['status']=='done':break
 gn=g['game']
 while g['status']=='your_move':
  pos,k=rp(g['moves']);m=R(pos,50000)
  if m is None:g=P2('/resign',{'game':gn});break
  i,j,pr=m
  if k%2:i=119-i;j=119-j
  mv=Y(i)+Y(j)+pr.lower()
  L=g['legal_moves']
  g=P2('/move',{'game':gn,'move':mv if mv in L else L[0]})