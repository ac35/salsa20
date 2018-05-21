'''
    kode di bawah ini merupakan implementasi dari contoh fungsi Salsa20 core
    pada laporan "The Salsa20 family of stream ciphers" oleh Daniel J. Bernstein.
    (contoh dapat dilihat di bagian 4.1 What does Salsa20 do?)
    
    Pada contoh tersebut diberikan beberapa variabel:
    - key dalam bentuk array dengan nilai [1,2,3,...,32]
    - nonce [3,1,4,1, 5,9,2,6]
    - block 7 [7,0,0,0, 0,0,0,0]
        # yang benar itu adalah [7,0,0,0, 0,0,0,0]. Bukan [0,0,0,7, 0,0,0,0]
        # > block_counter = [7,0,0,0, 0,0,0,0]
        # > b = [little_endian(block_counter[4*i:4*i+4]) for i in range(2)]
        # > b
        #   [7, 0]
        # > type(b[0]), type(b[1])
        #   (int, int)
        # kalau [0,0,0,7, 0,0,0,0]
        # > block_counter = [0,0,0,7, 0,0,0,0]
        # > b = [little_endian(block_counter[4*i:4*i+4]) for i in range(2)]
        # > b
        #   [117440512, 0]
        # beda hasilnya
        # kesimpulan: block_counter yang akan diberi ke Salsa() bentuknya 
        #             big-endian 7,0,0,0 (jangan berbentuk little-endian 0,0,0,7)
        # catatan: 7,0,0,0 di dalam array [7,0,0,0, 0,0,0,0] merepresentasikan
        #          satu word (32-bit/4-byte). 
        #          ingan block_counter pada Salsa20 ukurannya itu dua word
        #          (64bit/8-byte).
        #          
'''


class Salsa:
  def __init__(self,r=20):
    assert r >= 0
    self._r = r # number of rounds
    self._mask = 0xffffffff # 32-bit mask
  
  def __call__(self,key=[0]*32,nonce=[0]*8,block_counter=[0]*8):
    assert len(key) == 32
    assert len(nonce) == 8
    assert len(block_counter) == 8
    
    ## print(key)
    ## print([key[4*i:4*i+4] for i in range(8)])
    
	# init state
    k = [self._littleendian(key[4*i:4*i+4]) for i in range(8)]
    
    ## print(k)
	
    n = [self._littleendian(nonce[4*i:4*i+4]) for i in range(2)]
    b = [self._littleendian(block_counter[4*i:4*i+4]) for i in range(2)]
    c = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

    
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    # empat constant word khusus untuk contoh kedua
    # empatConstantWord = [211,159,13,115, 1,106,178,219, 116,147,48,113, 88,118,104,54]
    # c = [self._littleendian(empatConstantWord[4*i:4*i+4]) for i in range(4)]
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    
    
    s = [c[0], k[0], k[1], k[2], 
         k[3], c[1], n[0], n[1],
         b[0], b[1], c[2], k[4], 
         k[5], k[6], k[7], c[3]]

    ## print(s)     

    # the state
    self._s = s[:]

    for i in range(self._r):
      self._round()

    # add initial state to the final one
    self._s = [(self._s[i] + s[i]) & self._mask for i in range(16)]

    return self._s

  def _littleendian(self,b):
    assert len(b) == 4
    return b[0] ^ (b[1] << 8) ^ (b[2] << 16) ^ (b[3] << 24)

  def _round(self):

    # quarterround 1
    self._s[ 4] ^= self._rotl32((self._s[ 0] + self._s[12]) & self._mask, 7)
    self._s[ 8] ^= self._rotl32((self._s[ 0] + self._s[ 4]) & self._mask, 9)
    self._s[12] ^= self._rotl32((self._s[ 4] + self._s[ 8]) & self._mask,13)
    self._s[ 0] ^= self._rotl32((self._s[ 8] + self._s[12]) & self._mask,18)

    # quarterround 2
    self._s[ 9] ^= self._rotl32((self._s[ 1] + self._s[ 5]) & self._mask, 7)
    self._s[13] ^= self._rotl32((self._s[ 5] + self._s[ 9]) & self._mask, 9)
    self._s[ 1] ^= self._rotl32((self._s[ 9] + self._s[13]) & self._mask,13)
    self._s[ 5] ^= self._rotl32((self._s[ 1] + self._s[13]) & self._mask,18)

    # quarterround 3
    self._s[14] ^= self._rotl32((self._s[ 6] + self._s[10]) & self._mask, 7)
    self._s[ 2] ^= self._rotl32((self._s[10] + self._s[14]) & self._mask, 9)
    self._s[ 6] ^= self._rotl32((self._s[ 2] + self._s[14]) & self._mask,13)
    self._s[10] ^= self._rotl32((self._s[ 2] + self._s[ 6]) & self._mask,18)

    # quarterround 4
    self._s[ 3] ^= self._rotl32((self._s[11] + self._s[15]) & self._mask, 7)
    self._s[ 7] ^= self._rotl32((self._s[ 3] + self._s[15]) & self._mask, 9)
    self._s[11] ^= self._rotl32((self._s[ 3] + self._s[ 7]) & self._mask,13)
    self._s[15] ^= self._rotl32((self._s[ 7] + self._s[11]) & self._mask,18)

    # transpose
    self._s = [self._s[ 0], self._s[ 4], self._s[ 8], self._s[12],
               self._s[ 1], self._s[ 5], self._s[ 9], self._s[13],
               self._s[ 2], self._s[ 6], self._s[10], self._s[14],
               self._s[ 3], self._s[ 7], self._s[11], self._s[15]]

  def _rotl32(self,w,r):
    # rotate left for 32-bits
    return ( ( ( w << r ) & self._mask) | ( w >> ( 32 - r ) ) ) 
