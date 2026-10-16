cipher='BAIN{bA73_Q8R_ArhHC_X4yGcD}'
def dec(key,adv,mode):
    out=[];ki=0
    for ch in cipher:
        if ch.isalpha():
            c=ord(ch.upper())-65
            k=ord(key[ki%len(key)])-65
            p=(k-c)%26 if mode=='beaufort' else ((c-k)%26 if mode=='vig' else (c+k)%26)
            out.append(chr(p+65) if ch.isupper() else chr(p+97)); ki+=1
        elif ch=='_' or ch=='{':
            if adv=='reset': ki=0
            elif adv=='all': ki+=1
            out.append(ch)
        else:
            if adv in ('all','letdig','reset-dig'): ki+=1
            out.append(ch)
    return ''.join(out)
fams=[('Beaufort key=CYBR','CYBR','beaufort'),
      ('Vigenere key=ACPJ','ACPJ','vig'),
      ('Variant-Beaufort key=AYLR','AYLR','venc')]
for adv in ('letters','all','letdig','reset','reset-dig'):
    for name,key,mode in fams:
        print(f'{name:28s} adv={adv:10s} {dec(key,adv,mode)}')
print()
print('raw b64 decode            :', cipher)
