import sys
sys.argv = ['bda', 'run-pyamm', '--base', 'OKane2022', '--params', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\params_round15.json', '--protocol', '4C_charge_45C', '--mode', 'dfn', '--thermal', 'lumped', '--plating', '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run15_4c.json']
from bda.cli import main
main(sys.argv[1:])
