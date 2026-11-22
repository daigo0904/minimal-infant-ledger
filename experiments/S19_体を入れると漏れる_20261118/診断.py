import sys, json, numpy as np
sys.path.insert(0, '../S17_右脳左脳_20261118')
import 脳 as B
記 = []
class K(B.赤ちゃん):
    def 選ぶ(self, φ): 記.append(self.h); return super().選ぶ(φ)
B.赤ちゃん = K
out = {}
for 段, 種 in [('本', range(6600, 6610)), ('追試', range(6700, 6710))]:
    for 腕 in ['一つ128', '一つ128体']:
        v = {'上限の割合': [], 'P他_上限': [], 'P他_未満': []}
        for s in 種:
            記.clear(); o = B.一生(s, 腕); H = np.array(記).reshape(8000, 8)[7000:8000]; A = o['行動列'][7000:8000]; 相 = o['相手列'][7000:8000]; b = o['一番']
            w = 相 > 0; 上 = H >= 0.999
            v['上限の割合'].append(float(上.mean())); v['P他_上限'].append(float((A[w & 上] == b).mean()) if (w & 上).any() else np.nan); v['P他_未満'].append(float((A[w & ~上] == b).mean()))
        out[f'{段}_{腕}'] = {k: round(float(np.nanmedian(x)), 3) for k, x in v.items()}
        print(段, 腕, out[f'{段}_{腕}'], flush=True)
json.dump(out, open('結果_診断.json', 'x'), ensure_ascii=False, indent=1)
