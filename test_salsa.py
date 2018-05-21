#!/usr/bin/env python
from salsa import Salsa

def print_state(s):
  assert len(s) == 16
  for i in range(4):
    print("{:08x} {:08x} {:08x} {:08x}".format(s[4*i],s[4*i+1],s[4*i+2],s[4*i+3]))

if __name__ == '__main__':
  salsa20 = Salsa()
  
  # import time
  # iter = 12000
  # totalWaktu = 0
  # for i in range(iter):
      # start = time.time()
      # s = salsa20(range(1,33), [3,1,4,1,5,9,2,6], [7,0,0,0,0,0,0,0])
      # waktuDiperlukan = time.time() - start
      # totalWaktu += waktuDiperlukan
  # print(totalWaktu)    
  
  
  s = salsa20(range(1,33), [3,1,4,1,5,9,2,6], [7,0,0,0,0,0,0,0])
  print_state(s)
  




  
  # -------------------------------------------------------------------------------------------------------------------
  # -------------------------------------------------------------------------------------------------------------------


  
  # stateContoh2 (state pada contoh kedua di fungsi Salsa20)
  
  # empat constant word, delapan key word, dua nonce word dan dua block-counter word 
  # diambil dari contoh kedua di dalam laporan "Salsa20 Specification" 
  # oleh Daniel J. Bernstein

  
  # -------------------------------------------------------------------------------------------------------------------
  # format pemanggilan salsa20(delapan_key_word, dua_nonce_word, dua_block-counter_word)
  # stateContoh2 =  salsa20([76,55,82,183,  3,117,222,37,  191,187,234,136, 49,237,179,48,     # empat key word pertama
                      # 238,55,204,36, 79,201,235,79, 3,81,156,47,     203,26,244,243],   # empat key word selanjutnya
                     # [175,199,166,48, 86,16,179,207],       # dua nonce word                
                     # [31,240,32,63,   15,83,93,161])        # dua block-counter word
  # print_state(stateContoh2)    
  # -------------------------------------------------------------------------------------------------------------------


  
  # -------------------------------------------------------------------------------------------------------------------
  # -------------------------------------------------------------------------------------------------------------------
  