import json
import sys
import os
sys.path.append('D:\\research\\degradation_prognostics\\Battery_Design_Agent\\scripts')
from bda.cli import main

# Assume mass from run4_energy.json for R4, but R5 has different thickness.
# R13 uses base params (L_n=100um, L_p=77um).
m_total = 0.444843
m_kg = m_total / 1000.0

args = ['run-tr', '--sim', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run13_overcharge.json', '--mass-kg', str(m_kg), '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run13_tr.json']
main(args)
