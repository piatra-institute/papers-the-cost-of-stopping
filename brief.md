# Brief

Written before research begins.

## Question

Why did Europe's retreat from nuclear power cost so much more than the electricity it forwent, and when did the retreat actually begin? The paper treats the retreat as an industrial-capability event rather than a technology choice: what was lost was the ability to build reactors economically, and the loss preceded Chernobyl, outlasted every policy reversal, and ended by supplying the evidence used to justify it.

## Claim

Europe's nuclear discontinuity was a dynamic industrial-policy failure with four parts, each carrying different evidentiary weight:

1. **The retreat predates Chernobyl.** Western European construction starts collapsed between 1979 and 1983; the pipeline was nearly empty before April 1986. Chernobyl was a ratchet that converted a heterogeneous slowdown into durable political lock-in. It accelerated and legitimized the retreat; it did not originate it.
2. **Stopping is five processes, not one event.** Order stop, construction stop, capability stop, asset stop, output decline. They run on different clocks, and the operating fleet (the stock) concealed the death of the order pipeline (the flow) for over a decade: EU nuclear output peaked in 2004, some two decades after Western orders had effectively ceased. This stock-flow illusion is why the interruption was politically invisible while it was happening.
3. **Capability hysteresis.** Industrial delivery capability decays when construction stops (teams disperse, suppliers requalify out, regulators forget new-build licensing) and rebuilding it requires building through the penalty the decay created. Reversing the policy does not reverse the effect: the first post-hiatus projects (Olkiluoto 3, Flamanville 3) arrived at roughly four times their estimated cost, and those costs were then read as properties of the technology rather than of the interruption. Stopping makes restarting expensive; expensive restarting appears to prove that stopping was correct. The trap is self-validating.
4. **A coordination failure sat underneath.** Reactor construction anywhere in Europe maintained suppliers, skills, and regulatory competence everywhere, but build decisions were national while the capability was continental. Each cancellation was individually small and collectively fatal. Euratom socialized nuclear risk without socializing continuity.

The counterfactual defended is minimum continuity: retain reactors independent regulators judge safe while fossil generation remains, and maintain a slow standardized replacement sequence, one or two units per year continent-wide, alongside the observed renewable expansion. The counterfactual explicitly rejected is the all-nuclear Europe, the displacement of renewable investment, and the claim that nuclear power would have prevented the 2022 crisis.

## Kind

**formal-model** wrapped around a genealogy — ships a simulation. `has_simulation: true`, `claims_target: results.json`.

The simulation is a stylized capability-hysteresis model of a reactor-building system: a capability stock with organizational forgetting, unit cost and duration as decreasing functions of capability (anchored to the documented 4x first-of-a-kind overruns and to the NEA's series-savings estimates), a fleet stock with construction lags and retirements, and a policymaker who decides whether to keep ordering by looking at the last realized unit cost. Results the model must produce or refute:

- **The stock-flow lag**: generation peaks long after orders stop; measure the lag.
- **The ratchet**: under a myopic cost-reading policymaker there is a critical freeze duration; below it the system returns to the build equilibrium, above it the trap closes and never reopens. 1986's role is a parameter, and its value can be computed.
- **Hysteresis asymmetry**: capability lost in G years takes much longer than G to rebuild, because rebuilding means buying units at the penalty the loss created.
- **The coordination wedge**: with capability spillovers across countries, nationally chosen construction falls short of the continental optimum; measure the wedge as a function of the spillover share.
- **The counterfactual table**: observed vs retention-only vs minimum-continuity vs high-nuclear, on cumulative fossil generation, gas-shock exposure, restart cost, and programme cost.
- **Where the thesis fails**: a regime grid (forgetting rate x crisis probability, or renewable learning rate x capital cost) with cells where continuity does not pay. The 2022 French fleet's correlated outages enter as a vintage-concentration experiment, so the paper's own caveat is also a number.

Calibration is anchoring, and the paper says so plainly: the numbers are facts about the model's geometry, disciplined by documented magnitudes, and none is an econometric estimate.

## Constraint

The historical record enters through verified sources; the model's numbers enter through results.json; the two are never blended in one sentence without attribution. The paper stands alone and cites no PIATRA paper.

## Cornerstone literature

Must engage, each with one job and one stated limit:

- **Jarvis, Deschênes and Jha** (2022), the German phase-out costs — the strongest causal evidence that closing nuclear before coal raised emissions, pollution, and social cost. Limit: model-based counterfactual, one country, 2012–2019.
- **Lovering, Yip and Nordhaus** (2016), historical construction costs across countries — no single universal cost escalation; outcomes vary by regime. Limit: cost-data coverage and comparability were disputed in published comments.
- **Grubler** (2010), the French scale-up as negative learning — cost escalation inside the most standardized programme. Limit: contested data provenance; Rangel and Lévêque's reanalysis softens the slope.
- **Berthélemy and Escobar Rangel** (2015), lead-time and standardization econometrics — the closest thing to a direct test of the continuity mechanism.
- **Benkard** (2000) and **Argote and Epple** (1990), organizational forgetting — the microfoundation for the capability-decay term. Limit: aircraft and manufacturing, not reactors.
- **Arrow** (1962), learning by doing — the classical origin of the learning term.
- **Dixit** (1992) and **Blanchard and Summers** (1986), hysteresis in economics — investment under sunk costs and the unemployment case; the concept the model transplants. Limit: neither is about industrial capability stocks.
- **Davis** (2012), prospects for nuclear power — the sober economic baseline against triumphalism.
- **OECD NEA** (2020), reducing construction costs — the series-savings anchor. Limit: conditional engineering estimates, not observed outcomes.
- **STUK/Finnish national report** on Olkiluoto 3 — the regulator's own finding that the European hiatus destroyed the supplier base the project needed.
- **Cour des comptes** (2020/2025) on Flamanville and the EPR programme; **NAO** on Hinkley Point C — the restart-penalty record.
- **IPCC AR6 WGIII** (2022), renewable cost declines — the fact that forbids the nuclear-instead-of-renewables counterfactual.
- **Eurostat / IAEA PRIS** — the output and construction-start chronology the periodization rests on.
- **Euratom Supply Agency** (2022) and **RTE** (2023) — the two 2022 caveats: residual Russian fuel dependence, and the French fleet's correlated outages.
- **Müller and Thurner** (2017), the politics of nuclear energy in Western Europe — the comparative political record for the referenda and moratoria. Limit: political science of decisions, silent on industrial capability.

Not to be cited: any paper of this institute's.
