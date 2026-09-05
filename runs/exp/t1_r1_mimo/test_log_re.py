import sys
sys.argv = ['bda', 'log-evaluate', '--case-dir', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo', '--round', '1', '--outputs', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run1_energy.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run1_4c.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run1_tr.json', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run1_overcharge.json', '--candidate', 'OKane2022 Baseline (R1 Re-Eval v2)', '--note', 'Re-evaluating R1 with run1_tr.json LAST to fix T_max_K']
from bda.cli import main
main(sys.argv[1:])
