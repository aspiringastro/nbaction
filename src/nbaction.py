# src/nbaction.py
import os
import os.path
import glob
import subprocess
from pathlib import Path

NOTEBOOK_EXTN = ".ipynb"
HTML_EXTN = ".html"

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
sources = os.environ.get("NB_SOURCES", '').split(' ')
target_path = os.path.join(repo_workspace, os.environ.get("NB_TARGET_PATH", 'target/note'))
doc_path = os.path.join(repo_workspace, os.environ.get("NB_DOC_PATH", 'target/doc'))

all_sources = set([ os.path.join(repo_workspace, f) for f in sources ])
processed = []

print(all_sources)
print(f'Workspace: {repo_workspace}')
print(f'sources = {sources}')
print(f'target_path={target_path}')
print(f'doc_path={doc_path}')

for s in all_sources:
    if '.ipynb_checkpoints' in s:
        continue
    basename = os.path.basename(s)
    f, extn = os.path.splitext(basename)
    print(basename, f, extn)
    if extn.lower() == NOTEBOOK_EXTN:
        print (f'Notebook file detected: {basename}')
        ti = os.path.join(repo_workspace, target_path)
        tif = os.path.join(ti, basename)
        di = os.path.join(repo_workspace, doc_path)
        dif = os.path.join(di, f + HTML_EXTN)

        os.makedirs(ti, exist_ok=True)
        os.makedirs(di, exist_ok=True)

        clean_notebook(s)
        exec_notebook(s, tif)
        publish_notebook(tif, dif)

        processed.append(s)
        processed.append(tif)
        processed.append(dif)
        print(processed)

print(processed)
print("processed=", ' '.join(processed))


