# Breaking a broken one-time pad.

The following presents a solution to the small challenge posted by
Ente on his [blog.](https://duckpond.ch/security/math/2016/09/15/broken-one-time-pad.html)

## Code inspection

The first step in any endeavour, is to look at what we've
got. Luckily, we're provided with the full source code of the program,
from which we learn the following important facts:

  * The encryption used is (essentially) a [Vigenere Cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher);
  * the key length is provided (denoted by the `PAD_LENGTH` variable);
  * the encrypted data is base64 encoded

In order to break this scheme, we essentially do the following

  * Break the Cipher text into `PAD_LENGTH` chunks such that a byte in
    chunk `i` was encoded with key-byte `i`.
  * For every byte in some chunk, try an decrypt it every possible
    key-byte (there's only 255 of them), and see if the result is a
    valid base64 character; if it is, store the key-byte.

## Acquiring a Ciphertext

We acquire a piece of Ciphertext by connecting to `duckpond.ch` on
port `8888` with netcat:

`
nc duckpond.ch 8888 > ciphertext
`

## Decryption

A small python program was written (see `somecode.py`) which handles
decryption. The relevant functions are `split_ct` and `find_pad`,
corresponding to the first, respectively second, point mentioned
earlier. When done, `find_pad` will write the key to a file called
`key` (granted, in a somewhat stupid format, but whatever). The key is
written to a file because its big (more precisely 100kB), and because
it might have happened that we for some block, got two key-bytes which
both produce valid base64 data (i.e., both are valid key-bytes, as far
as `find_pad` is concerned).

Finally, we can read the key back, the encrypted data, and decrypt it
with an elegant python one-liner:

`
p = ''.join([chr(f[i] ^ k[i][0]) for i in range(PAD_LEN)])
`

The encoded image will be repeated a lot of times in the decrypted
text. We can extract the image with

`
grep -o '^[a-zA-Z0-9][^=]*==' decryptedtext | base64 -d > qrcode.png
`

(The encoding contains two padding chars, which is the reason for the
last two `=`).

Finally, to actually read the QR code, we can use a tool such
as [zbar](http://zbar.sourceforge.net/)

## Conclusion

That was a fun challenge. I'm sure someone smarter, or more python
savvy, than me would be able to find the key faster. Finding all 100kB
probably took around 10-20 minutes.

Thanks to Ente for the fun challenge and the 0.0131583 BTC.
