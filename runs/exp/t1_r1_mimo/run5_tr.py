import json
import sys
import os
sys.path.append('D:\\research\\degradation_prognostics\\Battery_Design_Agent\\scripts')
from bda.cli import main

# Assume mass from run4_energy.json for R4, but R5 has different thickness.
# Ideally calculate mass for R5, but using R4 as proxy for now or just run bda run-tr
# Mass for R5: L_n=88um, L_p=60um.
# M_n = 0.105 * (88/100) = 0.0924
# M_p = 0.164 * (60/77) = 0.1278
# M_cc = 0.1507
# M_sep = 0.0025
# Total M = 0.3734 g/cell -> 0.0373 kg
mass = 0.03734

args = ['run-tr', '--sim', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run5_overcharge.json', '--mass', str(mass), '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run5_tr.json']
main(args)
