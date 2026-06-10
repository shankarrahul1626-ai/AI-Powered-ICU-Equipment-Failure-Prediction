import os
matches=[]
for dirpath,dirs,files in os.walk('.'):
    if '.venv' in dirpath or 'venv' in dirpath or '.streamlit' in dirpath:
        continue
    for f in files:
        if f.endswith('.py') or f.endswith('.md') or f.endswith('.html'):
            p=os.path.join(dirpath,f)
            try:
                with open(p,encoding='utf-8',errors='ignore') as fh:
                    for i,line in enumerate(fh,1):
                        if 'Executive%20Dashboard' in line or '?page=' in line:
                            matches.append((p,i,line.strip()))
            except Exception:
                pass
for p,i,l in matches:
    print(f"{p}:{i}: {l}")
print('---done---')
