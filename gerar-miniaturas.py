# Gera as miniaturas (160 px) das fotos dos produtos em dist/produtos/mini/.
# A plataforma embute essas miniaturas no PDF da cotação. Rode de novo quando entrar foto nova:
#   python gerar-miniaturas.py
from pathlib import Path
from PIL import Image

origem = Path("dist/produtos")
destino = origem / "mini"
destino.mkdir(exist_ok=True)
feitas = 0
for foto in sorted(origem.glob("*.jpg")):
    im = Image.open(foto).convert("RGB")
    im.thumbnail((160, 160))
    im.save(destino / foto.name, "JPEG", quality=80, optimize=True)
    feitas += 1
print(f"{feitas} miniaturas em {destino}")
