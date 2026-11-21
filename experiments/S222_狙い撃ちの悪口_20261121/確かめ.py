import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S221_並び方で見抜く_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.05, 7, '並び')['sha256']"); b = run('S222_狙い撃ちの悪口_20261121', "数え.一生(900, (0,1,2,3), 7, None, 寿命=3000)['sha256']"); c = run('S222_狙い撃ちの悪口_20261121', "数え.一生(900, (0,1,2,3), 7, 0, 寿命=3000)['sha256']")
print('悪口なし（逆さの嘘）＝S221', a == b != 'ERR', a[:12], b[:12]); print('悪口で変わる', c != b and c != 'ERR', c[:12])
