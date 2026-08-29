from bda.store import CaseWorkspace, append_entry
ws=CaseWorkspace('exp/t3_r1_luna',root='runs')
append_entry(ws,{'action':'propose','round':0,'candidates':[{'name':'baseline','role':'Chen2020 default cell baseline'}],'llm_reason':'Deterministic Chen2020 baseline because electrode system unspecified; characterize ceiling and limiting metrics.'})
append_entry(ws,{'action':'propose','round':1,'candidates':[{'name':'V1_high_transport','role':'Higher electrolyte conductivity/diffusivity, smaller particles, thinner inactive layers, improved cooling'}],'llm_reason':'Architecture and transport fallback targets rate polarization, plating, thermal rise, and inactive mass.'})
append_entry(ws,{'action':'propose','round':2,'candidates':[{'name':'V2_high_rate','role':'Aggressive high-transport, 2 um particles, thin separator/current collectors, stronger cooling'}],'llm_reason':'Second fallback increases rate margin after V1 still failed 5C retention and temperature.'})
