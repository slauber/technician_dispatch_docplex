Maximize
 obj: - Startzeit_0 - Startzeit_1 - Startzeit_2 + 1500
Subject To
 c1: Startzeit_0 >= 0
 c2: Startzeit_1 >= 0
 c3: Startzeit_2 >= 0
 c4: Startzeit_0 <= 455
 c5: Startzeit_1 <= 490
 c6: Startzeit_2 <= 490
 lc7: Fahrten_0_0_3 = 1 <-> Startzeit_0 <= 435
 lc8: Fahrten_1_0_4 = 1 <-> Startzeit_0 <= 440
 lc9: Fahrten_0_1_3 = 1 <-> Startzeit_1 <= 460
 lc10: Fahrten_1_1_4 = 1 <-> Startzeit_1 <= 465
 lc11: Fahrten_0_2_3 = 1 <-> Startzeit_2 <= 440
 lc12: Fahrten_1_2_4 = 1 <-> Startzeit_2 <= 445
 lc7: Fahrten_0_0_3 = 1 <-> Startzeit_0 <= 435
 lc8: Fahrten_1_0_4 = 1 <-> Startzeit_0 <= 440
 lc9: Fahrten_0_1_3 = 1 <-> Startzeit_1 <= 460
 lc10: Fahrten_1_1_4 = 1 <-> Startzeit_1 <= 465
 lc11: Fahrten_0_2_3 = 1 <-> Startzeit_2 <= 440
 lc12: Fahrten_1_2_4 = 1 <-> Startzeit_2 <= 445
 c7: Fahrten_0_0_4 = 0
 c8: Fahrten_0_1_4 = 0
 c9: Fahrten_0_2_4 = 0
 c10: Fahrten_0_3_4 = 0
 c11: Fahrten_0_4_4 = 0
 c12: Fahrten_1_0_3 = 0
 c13: Fahrten_1_1_3 = 0
 c14: Fahrten_1_2_3 = 0
 c15: Fahrten_1_3_3 = 0
 c16: Fahrten_1_4_3 = 0
 c17: Fahrten_0_4_0 = 0
 c18: Fahrten_0_4_1 = 0
 c19: Fahrten_0_4_2 = 0
 c20: Fahrten_0_4_3 = 0
 c21: Fahrten_0_4_4 = 0
 c22: Fahrten_1_3_0 = 0
 c23: Fahrten_1_3_1 = 0
 c24: Fahrten_1_3_2 = 0
 c25: Fahrten_1_3_3 = 0
 c26: Fahrten_1_3_4 = 0
 c27: Fahrten_0_3_0 + Fahrten_0_3_1 + Fahrten_0_3_2 <= 1
 c28: Fahrten_1_4_0 + Fahrten_1_4_1 + Fahrten_1_4_2 <= 1
 c29: Fahrten_0_0_3 + Fahrten_0_1_3 + Fahrten_0_2_3 <= 1
 c30: Fahrten_1_0_4 + Fahrten_1_1_4 + Fahrten_1_2_4 <= 1
 c31: Fahrten_0_0_0 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c32: Fahrten_0_0_1 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c33: Fahrten_0_0_2 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c34: Fahrten_0_1_0 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c35: Fahrten_0_1_1 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c36: Fahrten_0_1_2 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c37: Fahrten_0_2_0 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c38: Fahrten_0_2_1 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c39: Fahrten_0_2_2 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c40: - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c41: - Fahrten_0_3_0 - Fahrten_0_3_2 <= 0
 c42: - Fahrten_0_3_0 - Fahrten_0_3_1 <= 0
 c43: Fahrten_0_4_0 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c44: Fahrten_0_4_1 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c45: Fahrten_0_4_2 - Fahrten_0_3_0 - Fahrten_0_3_1 - Fahrten_0_3_2 <= 0
 c46: Fahrten_1_0_0 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c47: Fahrten_1_0_1 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c48: Fahrten_1_0_2 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c49: Fahrten_1_1_0 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c50: Fahrten_1_1_1 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c51: Fahrten_1_1_2 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c52: Fahrten_1_2_0 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c53: Fahrten_1_2_1 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c54: Fahrten_1_2_2 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c55: Fahrten_1_3_0 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c56: Fahrten_1_3_1 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c57: Fahrten_1_3_2 - Fahrten_1_4_0 - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c58: - Fahrten_1_4_1 - Fahrten_1_4_2 <= 0
 c59: - Fahrten_1_4_0 - Fahrten_1_4_2 <= 0
 c60: - Fahrten_1_4_0 - Fahrten_1_4_1 <= 0
 c61: Fahrten_0_0_1 - Fahrten_0_1_3 - Fahrten_0_2_3 <= 0
 c62: Fahrten_0_0_2 - Fahrten_0_1_3 - Fahrten_0_2_3 <= 0
 c63: Fahrten_0_1_0 - Fahrten_0_0_3 - Fahrten_0_2_3 <= 0
 c64: Fahrten_0_1_2 - Fahrten_0_0_3 - Fahrten_0_2_3 <= 0
 c65: Fahrten_0_2_0 - Fahrten_0_0_3 - Fahrten_0_1_3 <= 0
 c66: Fahrten_0_2_1 - Fahrten_0_0_3 - Fahrten_0_1_3 <= 0
 c67: Fahrten_0_3_0 - Fahrten_0_0_3 - Fahrten_0_1_3 - Fahrten_0_2_3 <= 0
 c68: Fahrten_0_3_1 - Fahrten_0_0_3 - Fahrten_0_1_3 - Fahrten_0_2_3 <= 0
 c69: Fahrten_0_3_2 - Fahrten_0_0_3 - Fahrten_0_1_3 - Fahrten_0_2_3 <= 0
 c70: Fahrten_1_0_1 - Fahrten_1_1_4 - Fahrten_1_2_4 <= 0
 c71: Fahrten_1_0_2 - Fahrten_1_1_4 - Fahrten_1_2_4 <= 0
 c72: Fahrten_1_1_0 - Fahrten_1_0_4 - Fahrten_1_2_4 <= 0
 c73: Fahrten_1_1_2 - Fahrten_1_0_4 - Fahrten_1_2_4 <= 0
 c74: Fahrten_1_2_0 - Fahrten_1_0_4 - Fahrten_1_1_4 <= 0
 c75: Fahrten_1_2_1 - Fahrten_1_0_4 - Fahrten_1_1_4 <= 0
 c76: Fahrten_1_4_0 - Fahrten_1_0_4 - Fahrten_1_1_4 - Fahrten_1_2_4 <= 0
 c77: Fahrten_1_4_1 - Fahrten_1_0_4 - Fahrten_1_1_4 - Fahrten_1_2_4 <= 0
 c78: Fahrten_1_4_2 - Fahrten_1_0_4 - Fahrten_1_1_4 - Fahrten_1_2_4 <= 0
 c79: Fahrten_0_0_0 + Fahrten_0_0_1 + Fahrten_0_0_2 + Fahrten_0_0_3
      + Fahrten_0_0_4 <= 1
 c80: Fahrten_0_1_0 + Fahrten_0_1_1 + Fahrten_0_1_2 + Fahrten_0_1_3
      + Fahrten_0_1_4 <= 1
 c81: Fahrten_0_2_0 + Fahrten_0_2_1 + Fahrten_0_2_2 + Fahrten_0_2_3
      + Fahrten_0_2_4 <= 1
 c82: Fahrten_0_4_0 + Fahrten_0_4_1 + Fahrten_0_4_2 + Fahrten_0_4_3
      + Fahrten_0_4_4 <= 1
 c83: Fahrten_1_0_0 + Fahrten_1_0_1 + Fahrten_1_0_2 + Fahrten_1_0_3
      + Fahrten_1_0_4 <= 1
 c84: Fahrten_1_1_0 + Fahrten_1_1_1 + Fahrten_1_1_2 + Fahrten_1_1_3
      + Fahrten_1_1_4 <= 1
 c85: Fahrten_1_2_0 + Fahrten_1_2_1 + Fahrten_1_2_2 + Fahrten_1_2_3
      + Fahrten_1_2_4 <= 1
 c86: Fahrten_1_3_0 + Fahrten_1_3_1 + Fahrten_1_3_2 + Fahrten_1_3_3
      + Fahrten_1_3_4 <= 1
 c87: Fahrten_0_0_1 - Fahrten_0_2_0 - Fahrten_0_3_0 - Fahrten_0_4_0 <= 0
 c88: Fahrten_0_0_2 - Fahrten_0_1_0 - Fahrten_0_3_0 - Fahrten_0_4_0 <= 0
 c89: Fahrten_0_0_3 - Fahrten_0_1_0 - Fahrten_0_2_0 - Fahrten_0_4_0 <= 0
 c90: Fahrten_0_0_4 - Fahrten_0_1_0 - Fahrten_0_2_0 - Fahrten_0_3_0 <= 0
 c91: Fahrten_0_1_0 - Fahrten_0_2_1 - Fahrten_0_3_1 - Fahrten_0_4_1 <= 0
 c92: Fahrten_0_1_2 - Fahrten_0_0_1 - Fahrten_0_3_1 - Fahrten_0_4_1 <= 0
 c93: Fahrten_0_1_3 - Fahrten_0_0_1 - Fahrten_0_2_1 - Fahrten_0_4_1 <= 0
 c94: Fahrten_0_1_4 - Fahrten_0_0_1 - Fahrten_0_2_1 - Fahrten_0_3_1 <= 0
 c95: Fahrten_0_2_0 - Fahrten_0_1_2 - Fahrten_0_3_2 - Fahrten_0_4_2 <= 0
 c96: Fahrten_0_2_1 - Fahrten_0_0_2 - Fahrten_0_3_2 - Fahrten_0_4_2 <= 0
 c97: Fahrten_0_2_3 - Fahrten_0_0_2 - Fahrten_0_1_2 - Fahrten_0_4_2 <= 0
 c98: Fahrten_0_2_4 - Fahrten_0_0_2 - Fahrten_0_1_2 - Fahrten_0_3_2 <= 0
 c99: Fahrten_1_0_1 - Fahrten_1_2_0 - Fahrten_1_3_0 - Fahrten_1_4_0 <= 0
 c100: Fahrten_1_0_2 - Fahrten_1_1_0 - Fahrten_1_3_0 - Fahrten_1_4_0 <= 0
 c101: Fahrten_1_0_3 - Fahrten_1_1_0 - Fahrten_1_2_0 - Fahrten_1_4_0 <= 0
 c102: Fahrten_1_0_4 - Fahrten_1_1_0 - Fahrten_1_2_0 - Fahrten_1_3_0 <= 0
 c103: Fahrten_1_1_0 - Fahrten_1_2_1 - Fahrten_1_3_1 - Fahrten_1_4_1 <= 0
 c104: Fahrten_1_1_2 - Fahrten_1_0_1 - Fahrten_1_3_1 - Fahrten_1_4_1 <= 0
 c105: Fahrten_1_1_3 - Fahrten_1_0_1 - Fahrten_1_2_1 - Fahrten_1_4_1 <= 0
 c106: Fahrten_1_1_4 - Fahrten_1_0_1 - Fahrten_1_2_1 - Fahrten_1_3_1 <= 0
 c107: Fahrten_1_2_0 - Fahrten_1_1_2 - Fahrten_1_3_2 - Fahrten_1_4_2 <= 0
 c108: Fahrten_1_2_1 - Fahrten_1_0_2 - Fahrten_1_3_2 - Fahrten_1_4_2 <= 0
 c109: Fahrten_1_2_3 - Fahrten_1_0_2 - Fahrten_1_1_2 - Fahrten_1_4_2 <= 0
 c110: Fahrten_1_2_4 - Fahrten_1_0_2 - Fahrten_1_1_2 - Fahrten_1_3_2 <= 0
 c111: Fahrten_0_0_0 + Fahrten_0_1_0 + Fahrten_0_2_0 + Fahrten_0_3_0
       + Fahrten_0_4_0 + Fahrten_1_0_0 + Fahrten_1_1_0 + Fahrten_1_2_0
       + Fahrten_1_3_0 + Fahrten_1_4_0 = 1
 c112: Fahrten_0_0_1 + Fahrten_0_1_1 + Fahrten_0_2_1 + Fahrten_0_3_1
       + Fahrten_0_4_1 + Fahrten_1_0_1 + Fahrten_1_1_1 + Fahrten_1_2_1
       + Fahrten_1_3_1 + Fahrten_1_4_1 = 1
 c113: Fahrten_0_0_2 + Fahrten_0_1_2 + Fahrten_0_2_2 + Fahrten_0_3_2
       + Fahrten_0_4_2 + Fahrten_1_0_2 + Fahrten_1_1_2 + Fahrten_1_2_2
       + Fahrten_1_3_2 + Fahrten_1_4_2 = 1
 c114: Fahrten_0_0_0 = 0
 c115: Fahrten_0_1_1 = 0
 c116: Fahrten_0_2_2 = 0
 c117: Fahrten_1_0_0 = 0
 c118: Fahrten_1_1_1 = 0
 c119: Fahrten_1_2_2 = 0
 c120: Startzeit_3 = 0
 c121: Startzeit_4 = 0
 c122: Fahrten_0_0_0 <= 0
 c123: Fahrten_0_0_0 <= 2
 c124: Fahrten_0_0_1 <= 0
 c125: Fahrten_0_0_1 <= 2
 c126: Fahrten_0_0_2 <= 0
 c127: Fahrten_0_0_2 <= 2
 c128: Fahrten_0_0_3 <= 0
 c129: Fahrten_0_0_3 <= 2
 c130: Fahrten_0_0_4 <= 0
 c131: Fahrten_0_0_4 <= 2
 c132: Fahrten_0_1_0 <= 0
 c133: Fahrten_0_1_0 <= 2
 c134: Fahrten_0_1_1 <= 0
 c135: Fahrten_0_1_1 <= 2
 c136: Fahrten_0_1_2 <= 0
 c137: Fahrten_0_1_2 <= 2
 c138: Fahrten_0_1_3 <= 0
 c139: Fahrten_0_1_3 <= 2
 c140: Fahrten_0_1_4 <= 0
 c141: Fahrten_0_1_4 <= 2
 c142: Fahrten_0_2_0 <= 1
 c143: Fahrten_0_2_0 <= 1
 c144: Fahrten_0_2_1 <= 1
 c145: Fahrten_0_2_1 <= 1
 c146: Fahrten_0_2_2 <= 1
 c147: Fahrten_0_2_2 <= 1
 c148: Fahrten_0_2_3 <= 1
 c149: Fahrten_0_2_3 <= 1
 c150: Fahrten_0_2_4 <= 1
 c151: Fahrten_0_2_4 <= 1
 c152: Fahrten_1_0_0 <= 1
 c153: Fahrten_1_0_0 <= 1
 c154: Fahrten_1_0_1 <= 1
 c155: Fahrten_1_0_1 <= 1
 c156: Fahrten_1_0_2 <= 1
 c157: Fahrten_1_0_2 <= 1
 c158: Fahrten_1_0_3 <= 1
 c159: Fahrten_1_0_3 <= 1
 c160: Fahrten_1_0_4 <= 1
 c161: Fahrten_1_0_4 <= 1
 c162: Fahrten_1_1_0 <= 1
 c163: Fahrten_1_1_0 <= 1
 c164: Fahrten_1_1_1 <= 1
 c165: Fahrten_1_1_1 <= 1
 c166: Fahrten_1_1_2 <= 1
 c167: Fahrten_1_1_2 <= 1
 c168: Fahrten_1_1_3 <= 1
 c169: Fahrten_1_1_3 <= 1
 c170: Fahrten_1_1_4 <= 1
 c171: Fahrten_1_1_4 <= 1
 c172: Fahrten_1_2_0 <= 2
 c173: Fahrten_1_2_0 <= 0
 c174: Fahrten_1_2_1 <= 2
 c175: Fahrten_1_2_1 <= 0
 c176: Fahrten_1_2_2 <= 2
 c177: Fahrten_1_2_2 <= 0
 c178: Fahrten_1_2_3 <= 2
 c179: Fahrten_1_2_3 <= 0
 c180: Fahrten_1_2_4 <= 2
 c181: Fahrten_1_2_4 <= 0

Bounds
0 <= Fahrten_0_0_0 <= 1
0 <= Fahrten_0_0_1 <= 1
0 <= Fahrten_0_0_2 <= 1
0 <= Fahrten_0_0_3 <= 1
0 <= Fahrten_0_0_4 <= 1
0 <= Fahrten_0_1_0 <= 1
0 <= Fahrten_0_1_1 <= 1
0 <= Fahrten_0_1_2 <= 1
0 <= Fahrten_0_1_3 <= 1
0 <= Fahrten_0_1_4 <= 1
0 <= Fahrten_0_2_0 <= 1
0 <= Fahrten_0_2_1 <= 1
0 <= Fahrten_0_2_2 <= 1
0 <= Fahrten_0_2_3 <= 1
0 <= Fahrten_0_2_4 <= 1
0 <= Fahrten_0_3_0 <= 1
0 <= Fahrten_0_3_1 <= 1
0 <= Fahrten_0_3_2 <= 1
0 <= Fahrten_0_3_3 <= 1
0 <= Fahrten_0_3_4 <= 1
0 <= Fahrten_0_4_0 <= 1
0 <= Fahrten_0_4_1 <= 1
0 <= Fahrten_0_4_2 <= 1
0 <= Fahrten_0_4_3 <= 1
0 <= Fahrten_0_4_4 <= 1
0 <= Fahrten_1_0_0 <= 1
0 <= Fahrten_1_0_1 <= 1
0 <= Fahrten_1_0_2 <= 1
0 <= Fahrten_1_0_3 <= 1
0 <= Fahrten_1_0_4 <= 1
0 <= Fahrten_1_1_0 <= 1
0 <= Fahrten_1_1_1 <= 1
0 <= Fahrten_1_1_2 <= 1
0 <= Fahrten_1_1_3 <= 1
0 <= Fahrten_1_1_4 <= 1
0 <= Fahrten_1_2_0 <= 1
0 <= Fahrten_1_2_1 <= 1
0 <= Fahrten_1_2_2 <= 1
0 <= Fahrten_1_2_3 <= 1
0 <= Fahrten_1_2_4 <= 1
0 <= Fahrten_1_3_0 <= 1
0 <= Fahrten_1_3_1 <= 1
0 <= Fahrten_1_3_2 <= 1
0 <= Fahrten_1_3_3 <= 1
0 <= Fahrten_1_3_4 <= 1
0 <= Fahrten_1_4_0 <= 1
0 <= Fahrten_1_4_1 <= 1
0 <= Fahrten_1_4_2 <= 1
0 <= Fahrten_1_4_3 <= 1
0 <= Fahrten_1_4_4 <= 1

Binaries
 Fahrten_0_0_0 Fahrten_0_0_1 Fahrten_0_0_2 Fahrten_0_0_3 Fahrten_0_0_4
 Fahrten_0_1_0 Fahrten_0_1_1 Fahrten_0_1_2 Fahrten_0_1_3 Fahrten_0_1_4
 Fahrten_0_2_0 Fahrten_0_2_1 Fahrten_0_2_2 Fahrten_0_2_3 Fahrten_0_2_4
 Fahrten_0_3_0 Fahrten_0_3_1 Fahrten_0_3_2 Fahrten_0_3_3 Fahrten_0_3_4
 Fahrten_0_4_0 Fahrten_0_4_1 Fahrten_0_4_2 Fahrten_0_4_3 Fahrten_0_4_4
 Fahrten_1_0_0 Fahrten_1_0_1 Fahrten_1_0_2 Fahrten_1_0_3 Fahrten_1_0_4
 Fahrten_1_1_0 Fahrten_1_1_1 Fahrten_1_1_2 Fahrten_1_1_3 Fahrten_1_1_4
 Fahrten_1_2_0 Fahrten_1_2_1 Fahrten_1_2_2 Fahrten_1_2_3 Fahrten_1_2_4
 Fahrten_1_3_0 Fahrten_1_3_1 Fahrten_1_3_2 Fahrten_1_3_3 Fahrten_1_3_4
 Fahrten_1_4_0 Fahrten_1_4_1 Fahrten_1_4_2 Fahrten_1_4_3 Fahrten_1_4_4

Generals
 Startzeit_0 Startzeit_1 Startzeit_2 Startzeit_3 Startzeit_4
End