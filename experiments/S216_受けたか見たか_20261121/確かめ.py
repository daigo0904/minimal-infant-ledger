import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
x = {}
for 名, d, 私 in [('S215両方', 'S215_私的な評判_20261121', 'True'), ('S216両方', 'S216_受けたか見たか_20261121', 'True'), ('S215なし', 'S215_私的な評判_20261121', 'False'), ('S216なし', 'S216_受けたか見たか_20261121', 'False'), ('受けた', 'S216_受けたか見たか_20261121', "'受けた'"), ('見た', 'S216_受けたか見たか_20261121', "'見た'")]:
    x[名] = run(d, f"数え.一生(900, 5.0, {私}, (0,1,2,3), 3000)['sha256']")
print({k: v[:12] for k, v in x.items()}); print('両方＝S215', x['S215両方'] == x['S216両方'] != 'ERR', '共有＝S215', x['S215なし'] == x['S216なし'] != 'ERR', '3つが違う', len({x['S216両方'], x['受けた'], x['見た']}) == 3 and 'ERR' not in x.values())
