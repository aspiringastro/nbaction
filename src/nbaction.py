# src/nbaction.py
import sys
import os
import os.path
import subprocess

NOTEBOOK_EXTN = ".ipynb"
HTML_EXTN = ".html"

def exec_notebook(src, target):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--to",  "notebook", "--execute", "--output=" + target, src ]
    return subprocess.run(cmd)

def clean_notebook(src):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--clear-output", src ]
    return subprocess.run(cmd)

def publish_notebook(src, target):
    cmd = ["jupyter", "nbconvert", "--ExecutePreprocessor.timeout=600", "--to", "html", "--output=" + target,  src ]
    return subprocess.run(cmd)

# Main
repo_workspace = os.environ.get("NB_WORKSPACE", '.')
sources = set([ s for s in os.environ.get("NB_SOURCES", '').split(' ') if s.endswith(NOTEBOOK_EXTN) ])
target_path = os.path.join(repo_workspace, os.environ.get("NB_TARGET_PATH", "publish/notebook"))
doc_path = os.path.join(repo_workspace, os.environ.get("NB_DOC_PATH", "publish/doc"))
print(f'Notebook Workspace   : {repo_workspace}')
print(f'Notebook Sources     : {sources}')
print(f'Target Path          : {target_path}')
print(f'Documentation Path   : {doc_path}')
processed = []

for s in sources:
    if '.ipynb_checkpoints' in s:
        continue
    basename = os.path.basename(s)
    f, _ = os.path.splitext(basename)
    sif = os.path.join(repo_workspace, s)
    ti = os.path.join(target_path, os.path.dirname(s))
    tif = os.path.join(ti, basename)
    di = os.path.join(doc_path, os.path.dirname(s))
    dif = os.path.join(di, f + HTML_EXTN)

    os.makedirs(ti, exist_ok=True)
    os.makedirs(di, exist_ok=True)

    result = clean_notebook(sif)
    if result.returncode != 0:
        print(f"ERROR: clean_notebook {basename} args:{sif} failed with code {result.returncode}")
    result = exec_notebook(sif, tif)
    if result.returncode != 0:
        print(f"ERROR: exec_notebook {sif} -> {tif} args:{sif}, {tif} failed with code {result.returncode}")
    result = publish_notebook(tif, dif)
    if result.returncode != 0:
        print(f"ERROR: publish_notebook {tif} -> {dif} args:{tif}, {dif} failed with code {result.returncode}")

    processed.append(sif)
    processed.append(tif)
    processed.append(dif)
    print(f"sif: {sif}")
    print(f"tif: {tif}")
    print(f"dif: {dif}")

print("{0}={1}".format("published", ' '.join(processed)), file=sys.stdout)
if "GITHUB_OUTPUT" in os.environ :
    with open(os.environ["GITHUB_OUTPUT"], "a") as f :
        print("{0}={1}".format("published", ' '.join(processed)), file=f)



