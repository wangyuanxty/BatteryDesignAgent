while (-not (Test-Path "D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_flash\df_endorse_md_out.json")) {
    Add-Content -Path "D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_flash\md_run.log" -Value "=== attempt $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" -Encoding utf8
    & "D:\anaconda\envs\py312\python.exe" -u -m bda run-md --box runs/exp/t5_r1_flash/md_box.json --engine mace --t-ns 1.0 --out runs/exp/t5_r1_flash/df_endorse_md_out.json >> "D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_flash\md_run.log" 2>&1
    Start-Sleep -Seconds 10
}
