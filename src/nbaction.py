# src/nbaction.py
import os
import os.path
import glob
import subprocess
from pathlib import Path

def exec_notebook(src, target):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--to",  "notebook", "--execute", "--output=" + target, src ]
    subprocess.run(cmd)

def clean_notebook(src):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--clear-output", src ]
    subprocess.run(cmd)

def publish_notebook(src, target):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--to", "html", "--output=" + target,  src ]
    subprocess.run(cmd)

repo_workspace = os.environ.get("GITHUB_WORKSPACE", '.')
sources = os.path.join(repo_workspace, os.environ.get("NB_SOURCES"))
target_path = os.path.join(repo_workspace, os.environ.get("NB_TARGET_PATH", 'target/note'))
doc_path = os.path.join(repo_workspace, os.environ.get("NB_DOC_PATH", 'target/doc'))

all_sources = set([ os.path.join(repo_workspace, os.path.dirname(f)) for f in sources ])
processed = []

for s in all_sources:
    if '.ipynb_checkpoints' in s:
        continue
    f = Path(s).stem
    basename = os.path.basename(s)
    sif = os.path.join(repo_workspace, s)
    ti = os.path.join(repo_workspace, target_path)
    tif = os.path.join(ti, basename)
    di = os.path.join(repo_workspace, doc_path)
    dif = os.path.join(di, f + ".html")

    os.makedirs(ti, exist_ok=True)
    os.makedirs(di, exist_ok=True)

    clean_notebook(sif)
    exec_notebook(sif, tif)
    publish_notebook(tif, dif)

    processed.add(sif)
    processed.add(tif)
    processed.add(dif)

print("processed=", ' '.join(map(str, processed)))


