import sys, numpy as np, 世界 as W
keep=[]
class K(W.赤ちゃん):
    def __init__(s,*a):super().__init__(*a);keep.append(s)
W.赤ちゃん=K
for s in [int(x) for x in sys.argv[1:]]:
    keep.clear();o=W.一生(s,'依存','獲得型',寿命=8000,離乳=8000)
    世=np.random.default_rng([s,0]);世.permutation(4);face=世.normal(0,1,(9,8));rng=np.random.default_rng(5)
    rows=[]
    for c in keep:
        out={}
        for who in range(9):
            φs=[c.感覚(face[who]+rng.normal(0,W.見た目雑音,8)) for _ in range(100)]
            out[who]=(np.mean([c.つながり.予測(φ) for φ in φs]), np.array([[m.予測(φ) for m in c.評価] for φ in φs]).mean(0), np.array([c.Q@φ for φ in φs]).mean(0))
        rows.append(out)
    u_c=np.mean([r[0][0] for r in rows]);u_p=np.mean([np.mean([r[w][0] for w in range(1,9)]) for r in rows])
    print(s,'好み',o['好み'],'つながり 養育者',round(u_c,3),'赤ちゃん平均',round(u_p,3))
    r=rows[0];print('  ê養育者',np.round(r[0][1],2),'ê赤ちゃん',np.round(r[3][1],2),'Q養育者',np.round(r[0][2],3),'Q赤ちゃん',np.round(r[3][2],3))
