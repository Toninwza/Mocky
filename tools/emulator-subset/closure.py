import re,glob,sys
deps={}
for d in glob.glob('services/service-*/Cargo.toml'):
    name=d.split('/')[1].replace('service-com-amazonaws-','')
    txt=open(d).read().split('[dev-dependencies]')[0]
    deps[name]=set(x.replace('service-com-amazonaws-','') for x in re.findall(r'^(service-com-[\w-]+)\s*=',txt,re.M))
def closure(seed):
    seen=set();st=list(seed)
    while st:
        s=st.pop()
        if s in seen: continue
        seen.add(s); st+=deps[s]
    return seen
