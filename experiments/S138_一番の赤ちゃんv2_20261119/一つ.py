import sys, importlib.util
_sp = importlib.util.spec_from_file_location('S138一覧', '../S138_一番の赤ちゃんv2_20261119/一覧.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
print(sys.argv[1], sys.argv[2], G.one((900, sys.argv[2], sys.argv[1])))
