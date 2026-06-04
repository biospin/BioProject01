# Comparison Table

| Paper | Data / Assay | Core Timing Concept | Model / Algorithm | Main Strength | Main Limitation | Relevance to Step 1 | Relevance to Step 2 | Relevance to Step 3 |
|---|---|---|---|---|---|---|---|---|
| MultiVelo | Paired ATAC+RNA multiome; brain, skin, HSPC, fetal brain | Priming interval, decoupling interval, Model 1 vs Model 2 | Joint ODE + EM fitting over chromatin, unspliced, spliced RNA | Establishes the core chromatin-RNA velocity frame | Latent-time units only; no CI on lag-like quantities | Strong conceptual base for lag definition | Partial; suggests baseline chromatin features but does not predict lag from them | Weak; no perturbation timing validation |
| MultiVeloVAE | Multi-sample paired ATAC+RNA multiome | Continuous cell-specific coupling / decoupling factors | VAE-based extension of MultiVelo with posterior inference | Moves from discrete states to cell-specific continuous dynamics | Still depends on strong model assumptions and lacks direct response-time validation | Strong for refined lag-like inference | Moderate; richer latent variables could feed feature prediction | Weak-to-moderate; more suggestive than validated |
| MoFlow | Paired chromatin+RNA multiome; skin and brain examples | Positive / negative chromatin-to-RNA lag with relay timing interpretation | Relay velocity model with cell-specific kinetic inference | Most direct lag interpretation among the three | Gene-wise scope and incomplete regulatory context | Strongest direct analog to activation / shutdown lag | Moderate; could produce lag targets for prediction | Weak; still no direct perturbation timing test |

## Fill Rule
- `Data / Assay`: paired multiome, aligned multiome, time-course, species, tissue
- `Core Timing Concept`: priming interval, decoupling interval, DTW lag, cell-specific dynamics
- `Relevance to Step 1`: lag definition and quantification
- `Relevance to Step 2`: baseline feature prediction feasibility
- `Relevance to Step 3`: perturbation or response timing validation potential
