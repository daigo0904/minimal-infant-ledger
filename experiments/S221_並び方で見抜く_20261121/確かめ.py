import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
x = {k: run(d, f"数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.05, 7, {c})['sha256']") for k, d, c in [('S220差', 'S220_嘘を見抜く_20261121', 'True'), ('S221差', 'S221_並び方で見抜く_20261121', 'True'), ('S220なし', 'S220_嘘を見抜く_20261121', 'False'), ('S221なし', 'S221_並び方で見抜く_20261121', 'False'), ('並び', 'S221_並び方で見抜く_20261121', "'並び'")]}
print({k: v[:12] for k, v in x.items()}); print('差＝S220', x['S220差'] == x['S221差'] != 'ERR', 'なし＝S220', x['S220なし'] == x['S221なし'] != 'ERR', '並びで変わる', x['並び'] not in (x['S221差'], 'ERR'))
