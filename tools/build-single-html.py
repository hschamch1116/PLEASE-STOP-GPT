from __future__ import annotations

import base64
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
SOURCE = SRC_DIR / "index.source.html"
OUTPUT = ROOT / "index.html"
CAR = ROOT / "assets" / "sketchbook" / "car.glb"
BOXMAN = ROOT / "assets" / "sketchbook" / "boxman.glb"

THREE_URL = "https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"
GLTF_URL = "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "PLEASE-STOP-GPT-builder"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8")


def main() -> None:
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    # First run: preserve the current maintainable source before generating the large self-contained index.
    if not SOURCE.exists():
        SOURCE.write_text(OUTPUT.read_text(encoding="utf-8"), encoding="utf-8")

    source = SOURCE.read_text(encoding="utf-8")
    three_js = fetch_text(THREE_URL)
    gltf_js = fetch_text(GLTF_URL)
    car_b64 = base64.b64encode(CAR.read_bytes()).decode("ascii")
    boxman_b64 = base64.b64encode(BOXMAN.read_bytes()).decode("ascii")

    # Remove the runtime CDN loader and replace it with fully inline libraries.
    loader_pattern = re.compile(
        r'<script>\s*\(function loadLibraries\(\)\{.*?\}\)\(\);\s*</script>',
        re.S,
    )
    inline_libs = (
        '<script>\n' + three_js + '\n</script>\n'
        '<script>\n' + gltf_js + '\n</script>\n'
        '<script>window.addEventListener("DOMContentLoaded",function(){'
        'if(window.startPleaseStopGPT){window.startPleaseStopGPT();}'
        'else{setTimeout(function(){window.startPleaseStopGPT&&window.startPleaseStopGPT();},0);}'
        '});</script>'
    )
    built, count = loader_pattern.subn(inline_libs, source, count=1)
    if count != 1:
        raise RuntimeError("Could not locate the external Three.js/GLTFLoader loader block.")

    old_asset_block = re.compile(
        r"var gltfLoader=new THREE\.GLTFLoader\(\);var CAR_URLS=\[[^\]]*\];var CHARACTER_URLS=\[[^\]]*\];\s*"
        r"function loadGLB\(urls,label,onProgress\)\{.*?\}\n",
        re.S,
    )
    embedded_loader = (
        "var gltfLoader=new THREE.GLTFLoader();"
        f"var CAR_B64='{car_b64}';"
        f"var CHARACTER_B64='{boxman_b64}';"
        "function b64ToArrayBuffer(b64){"
        "var binary=atob(b64),len=binary.length,bytes=new Uint8Array(len);"
        "for(var i=0;i<len;i++)bytes[i]=binary.charCodeAt(i);"
        "return bytes.buffer;}"
        "function loadEmbeddedGLB(b64,label,onProgress){"
        "return new Promise(function(resolve,reject){try{"
        "if(onProgress)onProgress(100);"
        "gltfLoader.parse(b64ToArrayBuffer(b64),'',resolve,reject);"
        "}catch(err){reject(err);}});}\n"
    )
    built, count = old_asset_block.subn(embedded_loader, built, count=1)
    if count != 1:
        raise RuntimeError("Could not locate the GLB URL loader block.")

    built = built.replace(
        "Promise.all([loadGLB(CAR_URLS,'car',function(v){loadStatus.car=v;updateLoadText();}),loadGLB(CHARACTER_URLS,'boxman',function(v){loadStatus.character=v;updateLoadText();})])",
        "Promise.all([loadEmbeddedGLB(CAR_B64,'car',function(v){loadStatus.car=v;updateLoadText();}),loadEmbeddedGLB(CHARACTER_B64,'boxman',function(v){loadStatus.character=v;updateLoadText();})])",
        1,
    )

    # The final file must not rely on network or repository-relative runtime assets.
    forbidden = [
        "cdnjs.cloudflare.com",
        "cdn.jsdelivr.net/npm/three",
        "unpkg.com/three",
        "assets/sketchbook/car.glb",
        "assets/sketchbook/boxman.glb",
        "raw.githubusercontent.com/swift502",
        "cdn.jsdelivr.net/gh/swift502",
    ]
    for token in forbidden:
        if token in built:
            raise RuntimeError(f"Generated index still contains external runtime dependency: {token}")

    marker = "<!-- SELF_CONTAINED_BUILD: Three.js + GLTFLoader + car.glb + boxman.glb embedded -->"
    built = built.replace("<title>PLEASE STOP, GPT</title>", "<title>PLEASE STOP, GPT</title>\n" + marker, 1)
    OUTPUT.write_text(built, encoding="utf-8")
    print(f"Generated {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
