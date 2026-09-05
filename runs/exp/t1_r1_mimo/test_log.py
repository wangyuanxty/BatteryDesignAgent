import sys
sys.argv = ['bda', 'log-evaluate', '--case-dir', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo', '--round', '3', '--batch-file', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo\\batch.json']
from bda.cli import main
main(sys.argv[1:])
