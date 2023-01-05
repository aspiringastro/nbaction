# src/nbaction.py
import os
import os.path
import glob
import subprocess

def exec_notebooks(src_path, target_path):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--to",  "notebook", "--execute", "--output-dir=" + target_path, src_path]
    subprocess.run(cmd)

def clean_notebooks(src_path):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--clear-output", src_path ]
    subprocess.run(cmd)

def publish_notebooks(src_path, doc_path):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--to", "html", "--output-dir=" + doc_path,  src_path ]
    subprocess.run(cmd)

repo_workspace = os.environ.get("GITHUB_WORKSPACE", '.')
src_path = os.path.join(repo_workspace, os.environ.get("NB_SOURCE_PATH", 'src'))
target_path = os.path.join(repo_workspace, os.environ.get("NB_TARGET_PATH", 'target/note'))
doc_path = os.path.join(repo_workspace, os.environ.get("NB_DOC_PATH", 'target/doc'))


all_sources = set([ os.path.dirname(f)[len(repo_workspace)+1:] for f in glob.glob(f'{src_path}/**/*.ipynb', recursive=True) ])
for s in all_sources:
    if '.ipynb_checkpoints' in s:
        continue
    si = os.path.join(repo_workspace, s, "*.ipynb")
    ti = os.path.join(repo_workspace, target_path)
    di = os.path.join(repo_workspace, doc_path)
    os.makedirs(ti, exist_ok=True)
    os.makedirs(di, exist_ok=True)
    clean_notebooks(si)
    exec_notebooks(si, ti)
    publish_notebooks(os.path.join(ti, "*.ipynb"), di)



