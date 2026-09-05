import sys
sys.argv = ['bda', 'run-tr', '--sim', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\sim_oc.json', '--mass-kg', '0.04345', '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run3_tr_oc.json']
from bda.cli import main
main(sys.argv[1:])
