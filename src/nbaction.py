# src/nbaction.py
import os

src = os.environ.get("NB_SOURCE_PATH")
target = os.environ.get("NB_TARGET_PATH")
doc = os.environ.get("NB_DOC_PATH")


print(f'SRC={src}')
print(f'TARGET={target}')
print(f'DOC={doc}')


