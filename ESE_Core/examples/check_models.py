"""Independent arithmetic checks for original ESE teaching examples.
No RTOS, network, RTL, analog, or hardware simulation is claimed.
Run from any working directory: python3 path/to/check_models.py
"""
from math import ceil, isclose, sqrt
from fractions import Fraction as F

def response_times(tasks):
    # tasks: (C,T,D), in descending priority. B=J=0, single CPU.
    answers = []
    for i, (c, t, d) in enumerate(tasks):
        r = c
        for _ in range(10000):
            nr = c + sum(ceil(F(r, tj)) * cj for cj, tj, _ in tasks[:i])
            if nr > d:
                answers.append(None)
                break
            if nr == r:
                answers.append(r)
                break
            r = nr
        else:
            raise AssertionError('no convergence')
    return answers

def check():
    assert 100 + 8 + 3 + 2 + 1 == 114
    assert ((0xFFFF & ~(7 << 4)) | (5 << 4)) == 0xFFDF
    assert 32 - (8 + 3*2 + 6 + 4) == 8
    assert isclose(40*10/115200*1000, 3.4722222222222223)
    assert 48_000_000 // ((47+1)*(999+1)) == 1000
    assert sum((F(1,4), F(1,5), F(2,10))) == F(65,100)
    assert response_times([(1,4,4),(1,5,5),(2,10,10)]) == [1,2,4]
    assert response_times([(1,2,2),(2,4,4)]) == [1,4]
    assert response_times([(1,5,5),(2,10,10)]) == [1,3]
    assert response_times([(3,4,4),(3,5,5)]) == [3,None]
    assert int.from_bytes(bytes([0xE6,0x09]),'little',signed=True)==2534
    assert int.from_bytes(bytes([0x0C,0xFE]),'little',signed=True)==-500
    assert 120*86400 == 10_368_000
    avg = 5*.010 + 8*.005 + 15*.004 + .010*.981
    assert isclose(avg,.15981)
    assert isclose(700/avg/24,182.50839538535343)
    assert isclose(20e-6/.0009,.022222222222222223)
    assert isclose(100*(.3+.02),32)
    assert isclose(10*.3+100*.02,5)
    assert isclose(.02*.002/.1,400e-6)
    assert isclose((5-3.3)*.1*60,10.2)
    assert isclose((1600-100)/30,50)
    assert isclose(3.3/4096*1000,.8056640625)
    assert isclose((256/1024)/.05*60,300)
    assert isclose(.01/(1*.1+.01*.01),.0999000999000999)
    assert sqrt(.2**2+.3**2) > .3
    assert 8*4095 == 32760 and (8*4095).bit_length()==15
    assert 384*(-64) == -24576
    # Exhaustive saturating-adder reference comparison to carry-based identity.
    for a in range(256):
        for b in range(256):
            wide = a+b
            carry_impl = 255 if wide & 256 else wide & 255
            assert carry_impl == min(a+b,255)
    print('PASS: ESE arithmetic, RTA pass/fail cases, 65536 adder inputs')

if __name__ == '__main__':
    check()
