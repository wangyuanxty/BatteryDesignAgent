import json
import sys
sys.path.append('D:\\research\\degradation_prognostics\\Battery_Design_Agent\\scripts')
from bda.cli import main

args = ['run-pyamm', '--base', 'OKane2022', '--params', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\params_round5.json', '--protocol', 'overcharge', '--mode', 'dfn', '--thermal', 'lumped', '--plating', '--out', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\run5_overcharge.json']
main(args)
