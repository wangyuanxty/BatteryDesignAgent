import sys
sys.argv = ['bda', 'run-pyamm', '--base', 'OKane2022', '--params', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\params_round13.json', '--protocol', 'overcharge', '--mode', 'dfn', '--thermal', 'lumped', '--plating', '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run13_overcharge.json']
from bda.cli import main
main(sys.argv[1:])
