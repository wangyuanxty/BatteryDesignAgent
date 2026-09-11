# OPLS-AA topology template directory (bda/simulators/data/opls/)

The deterministic box builder `_build_box` in `bda/simulators/md_runner.py` copies the
required `.itp` templates from this directory into the run working directory and
`#include`s them in `topol.top`.

> **This directory does not ship `.itp` files with the code** (they must be generated
> once by hand: LigParGen is an interactive web page, and the ilff parameters need manual
> curation). Behavioral contract:
>
> - GROMACS not installed: the slow test skips right at the `shutil.which("gmx")` check,
>   entirely unaffected;
> - GROMACS installed but templates missing: `_build_box` fast-fails with a `RuntimeError`
>   pointing at this document;
> - Templates complete: `_build_box` copies the .itp files into the run directory and
>   includes them correctly.

## File names and moleculetype names the code expects

| Species | Expected file | Expected `[moleculetype]` name | Generation tool |
|---------|---------------|--------------------------------|-----------------|
| EC      | `ec.itp`      | `EC`                           | LigParGen       |
| EMC     | `emc.itp`     | `EMC`                          | LigParGen       |
| PF6⁻    | `pf6.itp`     | `PF6`                          | ilff repo       |
| Li⁺     | `li.itp`      | `Li`                           | ilff repo       |

The `[molecules]` section written by `_build_box` uses the names from the table above
(`EC`/`EMC`/`PF6`/`Li`); after generating them, check that the `[moleculetype]` names
inside the .itp files match (if they do not, simply rename them by hand).

## EC / EMC: LigParGen generation steps

1. Open <https://zarbi.chem.yale.edu/ligpargen/> (interactive form, no API — do not try
   to script it).
2. Submit the SMILES separately:
   - EC: `C1COC(=O)O1`
   - EMC: `CCOC(=O)OC`
3. Choose **1.14*CM1A-LBCC** as the charge model (the recommended OPLS-AA default); choose
   **GROMACS** as the output format.
4. Download the products (the `.itp` and the optional `.prm`/`.gro`).
5. **Use the standalone form** of the .itp (with `[atomtypes]` and `[nonbond_params]`
   embedded): `topol.top` includes only the four .itp files from this directory and no
   longer includes `oplsaa.ff/forcefield.itp`. If the .itp from LigParGen starts with
   `#include "oplsaa.ff/..."`, either merge the parameters into a standalone .itp or
   place that force-field directory next to the run directory yourself.
6. Rename the `[moleculetype]` to `EC` / `EMC` and save the files in this directory as
   `ec.itp` / `emc.itp`.

## PF6 / Li: ilff repository parameters

1. Clone <https://github.com/agiliopadua/ilff>.
2. Locate the PF6 and Li⁺ parameters inside the repository (ilff organizes them as
   `.zmat`/`.ff` text; see its README). If only DL_POLY/LAMMPS formats are provided,
   convert them following the repository instructions, or assemble them from the
   supplementary tables of the IL/CL&P literature.
3. Assemble them into standalone GROMACS `.itp` files (with atomtypes/nonbond_params and
   `[moleculetype]` embedded), name the moleculetypes `PF6` and `Li`, and save them as
   `pf6.itp` / `li.itp`.

## Note on the 0.8 charge scaling

The common practice for mixed OPLS-AA and ilff systems is to scale the partial charges of
ions and solvent uniformly (to model polarization effects and avoid overly strong
electrostatics that slow diffusion or cause abnormal aggregation):

- Scale every PF6⁻ atomic charge × 0.8 (the ion's net charge goes from −1e to **−0.8e**);
- Li⁺ charge +1e → **+0.8e**;
- If the LigParGen atom types do not match ilff, use the same 0.8 scaling to unify them:
  scale the EC/EMC atomic charges by 0.8 as well.

The scaling must be done by hand in the .itp files, and the total system charge must be
re-checked as 0: `N_PF6 × (−0.8) + N_Li × (+0.8) = 0` (the solvent molecules are
electrically neutral).

## Verification

- No GROMACS environment: `pytest tests/test_md_runner.py` runs only the deterministic
  unit tests, slow ones are skipped;
- After installing GROMACS (`winget install GROMACS.GROMACS` or
  `conda install -c conda-forge gromacs`):
  `pytest tests/test_md_runner.py -m slow` runs a 0.1 ns short trajectory (about
  10~20 minutes) and asserts the returned `D_Li_m2_s`.
