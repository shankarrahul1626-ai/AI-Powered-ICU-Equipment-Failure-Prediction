import os
root='streamlit_app'
matches=[]
for dirpath,dirs,files in os.walk(root):
    for f in files:
        if f.endswith('.py'):
            p=os.path.join(dirpath,f)
            with open(p,encoding='utf-8',errors='ignore') as fh:
                for i,line in enumerate(fh,1):
                    if '<script' in line or '</script>' in line or 'document.' in line or 'URLSearchParams' in line or 'window.location' in line or 'navLinks' in line or 'theme-toggle' in line:
                        matches.append((p,i,line.strip()))
for p,i,l in matches:
    print(f"{p}:{i}: {l}")
print('---done---')
