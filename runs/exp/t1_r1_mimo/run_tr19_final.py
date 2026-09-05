import sys
sys.argv = ['bda', 'run-tr', '--sim', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run19_overcharge.json', '--mass-kg', '0.0434545275216', '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run19_tr.json']
from bda.cli import main
main(sys.argv[1:])
