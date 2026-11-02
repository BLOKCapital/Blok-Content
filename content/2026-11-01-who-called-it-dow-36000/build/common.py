import re
ones='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
tens='_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()
def n2w(n):
    n=int(n)
    if n<20: return ones[n]
    if n<100: return tens[n//10]+('' if n%10==0 else ' '+ones[n%10])
    if n<1000: return ones[n//100]+' hundred'+('' if n%100==0 else ' '+n2w(n%100))
    if 1100<=n<2000 and n%100!=0 and n//100!=10: return n2w(n//100)+' '+(n2w(n%100) if n%100>=10 else 'oh '+ones[n%100])
    if 2010<=n<2100: return 'twenty '+n2w(n%100)
    return n2w(n//1000)+' thousand'+('' if n%1000==0 else ' '+n2w(n%1000))
def norm(s):
    s=s.lower().replace('$','').replace('-',' ')
    s=re.sub(r'(\d),(\d)',r'\1\2',s)
    s=re.sub(r'\d+',lambda m:n2w(m.group()),s)
    s=re.sub(r'\bdollars?\b','',s)
    return re.sub(r"[^a-z' ]",' ',s).split()
