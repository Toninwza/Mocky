"""Trim aws-emulator workspace to a service subset (closure of seeds). Usage: trim.py <repo> <seed>..."""
import re,glob,sys,os
repo=sys.argv[1]; os.chdir(repo)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'closure.py')).read())
keep=closure(sys.argv[2:])
full=lambda n:'service-com-amazonaws-'+n
mod=lambda n:full(n).replace('-','_')
# root members
txt=open('Cargo.toml').read()
head,rest=txt.split('members = [',1); body,tail=rest.split(']',1)
lines=[l for l in body.splitlines() if 'services/service-com' not in l or any(l.strip().strip('",')=='services/'+full(k) for k in keep)]
open('Cargo.toml','w').write(head+'members = ['+'\n'.join(lines)+']'+tail)
# router Cargo.toml
t=open('core/router/Cargo.toml').read().splitlines()
t=[l for l in t if not re.match(r'^service-com-',l) or l.split()[0] in {full(k) for k in keep}]
open('core/router/Cargo.toml','w').write('\n'.join(t)+'\n')
# router lib.rs
t=open('core/router/src/lib.rs').read().splitlines()
km={mod(k) for k in keep}
def ok(l):
    m=re.search(r'(service_com_amazonaws_\w+)::',l)
    return not m or m.group(1) in km
open('core/router/src/lib.rs','w').write('\n'.join(l for l in t if ok(l))+'\n')
print(len(keep),'services kept'); print('\n'.join(sorted(keep)))
