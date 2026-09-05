import sys
sys.argv = ['bda', 'log-evaluate', '--case-dir', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo', '--round', '19', '--outputs', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run19_energy.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run19_4c.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run19_tr.json', '--candidate', 'OKane2022 High-t+ R19 (Best)', '--note', 'Best performance but still fails strict plating criterion']
from bda.cli import main
main(sys.argv[1:])
