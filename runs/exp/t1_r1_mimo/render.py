import sys
sys.argv = ['bda', 'render', '--case-dir', 'D:\\research\\degradation_prognostics\\Battery_Design_Agent\\runs\\exp\\t1_r1_mimo']
from bda.cli import main
main(sys.argv[1:])
