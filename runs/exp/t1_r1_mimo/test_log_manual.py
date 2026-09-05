import sys
sys.argv = ['bda', 'log-evaluate', '--case-dir', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo', '--round', '3', '--outputs', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run3_4c.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run3_tr.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run1_energy.json', '--candidate', 'OKane2022 High Cooling (Re-Eval)', '--note', 'Checking if log-evaluate correctly detects plating from anode potential']
from bda.cli import main
main(sys.argv[1:])
