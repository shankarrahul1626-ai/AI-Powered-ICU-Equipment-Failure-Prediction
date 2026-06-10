import os
for dirpath,dirs,files in os.walk('.'):
    if '.venv' in dirpath or 'venv' in dirpath or '.streamlit' in dirpath:
        continue
    for f in files:
        if f.endswith('.py') or f.endswith('.md') or f.endswith('.txt'):
            p=os.path.join(dirpath,f)
            try:
                with open(p,encoding='utf-8',errors='ignore') as fh:
                    s=fh.read()
                    if 'Theme toggle button handler' in s or 'navLinks.forEach' in s or 'URLSearchParams' in s or "// Theme toggle button handler" in s:
                        print(p)
            except Exception:
                pass
print('done')
