# Append: (1) three-strike plan-update entry, (2) propose r4 entry.
import sys
sys.path.insert(0, r".claude/skills/virtual-battery-factory/scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1_noceiling", "runs")

plan_update = {
    "action": "plan",
    "update": True,
    "reason": "three-strike: 4C plating and SEI500 fail for 3 consecutive rounds with the same cause. R3 dose-response (anode 85->110->130 um) scales BOTH metrics monotonically negative (anode min -0.4385->-0.4643->-0.5027; SEI500 777.9->865.6->979.9; H also fails SEI100) - N/P-up rejected; separator lever neutral (F: -0.4348, 787.9). All rounds: the 4C metric is pinned by the protocol start state (1C discharge to v_min leaves the anode deeply lithiated) + SPMe surface response + Chen2020 transport; the SEI500 is pinned by the 4.2 V charge-end depth per cycle. Levers that would move them (solid-phase diffusivity, initial lithiation, SEI kinetics, charge cut-off, electrode modification, electrode system) are all outside the admissible set (locked / excluded / escalation OFF).",
    "candidate_strategy": "final evidence round R4 (declared expected-negative): last qualitatively distinct admissible levers - (I) thermal cooling h 10->100 W/m2/K (4C kinetics cooler -> shallower abort; collateral on lowT retention, measured); (J) cathode particle radius 5.22->12.5 um (cathode surface depletes faster at 4C -> earlier abort -> less anode excursion; also shortens aging charge step); (K) electrolyte transport DOWN (sigma 0.95->0.475 S/m const, D 1.76e-10->9e-11, t+ 0.26->0.2) mirror of B (B's transport-up hurt both criteria); (L) anode porosity 0.25->0.35 (anode-side electrolyte-potential relief - the mechanism R3's phi_e-drop evidence points at). All on A's thin-CC base (ED bank). If negative (predicted): conclude infeasible-within-admissible-space, select best-effort candidate, close with honest negative result.",
    "budget_allocation": "one final round (4 candidates x full protocol set), then closing deliverables",
}
append_entry(ws, plan_update)

propose_r4 = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Total heat transfer coefficient [W.m-2.K-1]": 100.0},
         "name": "I Cool",
         "role": "thermal-management lever: 10x cooling keeps the 4C charge closer to the 45C ambient (slower kinetics -> shallower abort -> less anode excursion; R2/R3 correlation: T_max 329-340 K vs anode min -0.41..-0.50, hotter=worse). Collateral: lowT retention measured mechanically."},
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Positive particle radius [m]": 1.25e-05},
         "name": "J CathPartUp",
         "role": "cathode particle radius 5.22->12.5 um: lower cathode surface area -> surface lithium depletes faster at 4C -> 4.2 V abort earlier -> anode excursion cut short; also shortens the 1C aging charge step (SEI time integral)."},
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Electrolyte conductivity [S.m-1]": 0.475,
                    "Electrolyte diffusivity [m2.s-1]": 9e-11,
                    "Cation transference number": 0.2},
         "name": "K TransDown",
         "role": "mirror of B (B transport-up worsened anode min -0.4494 and SEI500 829.8): transport-down should abort the 4C charge shallower and shorten the aging charge step; risks a larger electrolyte potential drop - net sign measured."},
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Negative electrode porosity": 0.35},
         "name": "L AnPorUp",
         "role": "anode porosity 0.25->0.35: R3's dose-response showed the anode-internal electrolyte potential drop scales with anode thickness (E/G/H worse) - porosity attacks the same physics in the favorable direction (lower tortuosity); effective N/P drops (-13% active mass), which per the R3 dose-response also points favorable for plating."},
    ],
    "llm_reason": "R3 evaluated (4/4 fail, log-evaluate round 3): N/P-up rejected (monotonic negative dose-response on plating AND SEI, H fails SEI100 at 540.0); separator lever neutral. Three-strike reached on both hard criteria (see plan update entry). R4 is the declared final evidence sweep of the last distinct admissible levers: thermal management (untested axis, the only lever that acts on the 4C test kinetics without touching the isothermal aging), cathode particle size (architecture DoF, abort-race timing), electrolyte-down (mirror of the rejected B direction), anode porosity (anode-side electrolyte-potential relief). Nominal bookkeeping per established convention (measure 1C at 5 A per candidate, set nominal, re-run 1C ref). Expected outcome negative -> close with honest negative result. Sources: R2/R3 tool outputs (this case), pybamm_runner PROTOCOLS (lowT T_amb 253.15, 4C T_amb 318.15), Chen2020 dump (h=10, R_pos=5.22e-6, eps_neg=0.25).",
}
append_entry(ws, propose_r4)
print("plan-update + propose r4 appended")
