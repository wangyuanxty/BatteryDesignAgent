import sys
sys.argv = ['bda', 'log-evaluate', '--case-dir', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo', '--round', '13', '--outputs', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run13_energy.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run13_4c.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run13_tr.json', '--candidate', 'OKane2022 High-t+ R13', '--note', 'High transference number (t+=0.9) solved plating while maintaining thermal control']
from bda.cli import main
main(sys.argv[1:])
