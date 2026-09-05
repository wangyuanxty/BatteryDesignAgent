import json
import os
import sys
sys.path.append('D:\\research\\degradation_prognostics\\Battery_Design_Agent\\scripts')
from bda.cli import main

# Manually calculate mass for R5
m_n = 0.105882 * (88/100)
m_p = 0.16399 * (60/77)
m_cc = 0.04319 + 0.10752
m_sep = 0.00252
m_total = m_n + m_p + m_cc + m_sep
m_kg = m_total / 1000.0

args = ['calc-energy', '--sim', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run5_4c.json', '--mass', str(m_kg), '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run5_energy_v2.json']
main(args)
