# Comparison Table

| Paper | Data / Assay | Core Timing Concept | Model / Algorithm | Main Strength | Main Limitation | Relevance to Step 1 | Relevance to Step 2 | Relevance to Step 3 |
|---|---|---|---|---|---|---|---|---|
| MultiVelo | Paired ATAC+RNA multiome; brain, skin, HSPC, fetal brain | Priming interval, decoupling interval, Model 1 vs Model 2 | Joint ODE + EM fitting over chromatin, unspliced, spliced RNA | Establishes the core chromatin-RNA velocity frame and two regulation regimes | Latent-time units only; no CI on lag-like quantities | Strong conceptual base for lag definition via switch times and regime labels | Partial; suggests chromatin features but does not predict lag from baseline | Weak; no perturbation timing validation |
| MultiVeloVAE | Multi-sample paired ATAC+RNA multiome; HSPC, brain, EB, macrophage | Continuous cell-specific coupling / decoupling factors on shared time scale | VAE-based extension of MultiVelo with posterior inference and differential testing | Moves from discrete states to cell-specific continuous dynamics and supports sample integration | Still model-derived and not direct lag in real time; no direct response-time validation | Strong for refined lag-like inference and cell-type-specific variation | Moderate; richer dynamic variables could become prediction targets | Weak-to-moderate; posterior testing exists but wall-clock perturbation validation is absent |
| MoFlow | Paired chromatin+RNA multiome; skin, brain, blood-related systems | Positive / negative chromatin-to-RNA lag with relay timing interpretation | Relay velocity model with cell-specific kinetic inference | Most direct lag interpretation among the three and strong local trajectory recovery | Gene-wise scope and incomplete regulatory context | Strongest direct analog to activation / shutdown lag | Moderate; could provide lag targets for later prediction models | Weak; still no direct perturbation timing test |

## Fill Rule
- `Data / Assay`: paired multiome, aligned multiome, time-course, species, tissue
- `Core Timing Concept`: priming interval, decoupling interval, DTW lag, cell-specific dynamics
- `Relevance to Step 1`: lag definition and quantification
- `Relevance to Step 2`: baseline feature prediction feasibility
- `Relevance to Step 3`: perturbation or response timing validation potential
