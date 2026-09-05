import sys
sys.argv = ['bda', 'calc-energy', '--sim', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run5_4c.json', '--params', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\params_round5.json', '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run5_energy_v3.json']
from bda.cli import main
main(sys.argv[1:])
