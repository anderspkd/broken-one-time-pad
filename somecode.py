#!/usr/bin/python

from base64 import b64encode
from time import time

PAD_LEN = 1024*100

# Valid plaintext chars, i.e., true if c in [a-zA-Z0-9]
def valid_ptc(c):
    return (( c > 64 and c < 91  ) or
            ( c > 96 and c < 123 ) or
            ( c > 47 and c < 58  ) or
            ( c == 43) or
            ( c == 47) or
            ( c == 61 ))

def split_ct():
    a=[[] for i in range(PAD_LEN)]
    with open('out','rb') as f:
        i=0
        done=False
        while not done:
            c=f.read(1)
            if c != b'':
                a[i % PAD_LEN]+=[ord(c)]
                i+=1
                continue
            done=True
    return a

def find_pad():
    a=split_ct()
    ka=[[] for i in range(PAD_LEN)]
    j=0
    t=time()
    for j in range(PAD_LEN):
        chk=a[j]
        gk=[]
        for i in range(2**8):
            b=False
            for c in chk:
                if valid_ptc(c^i):
                    continue
                b=True
            if not b:
                gk+=[i]
        # Print the key array if we happend to get more than one hit.
        if len(gk) > 1:
            print('ka[{}]: {}'.format(j,gk))
        ka[j]=gk
        if time()-t > 5:
            t=time()
            print('Progress: {:4f}%'.format(100*(float(j)/PAD_LEN)))
    write_key(ka)

def write_key(k):
    with open('key', 'w') as f:
        f.write(str(k))

def read_key():
    with open('key','r') as f:
        k = eval(f.read()) # don't do this at home kids
    return k

if __name__ == '__main__':
    # find_pad() <- will find and write the key
    k = read_key()
    f=''
    with open('out', 'rb') as f_in:
        f = f_in.read()

    # Turns out PAD_LEN was longer than the image :-)
    p=''.join([chr(f[i] ^ k[i][0]) for i in range(PAD_LEN)])
    print(p)
