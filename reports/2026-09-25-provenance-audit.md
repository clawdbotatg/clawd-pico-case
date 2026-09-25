# Development-history and licensing evidence audit

Date: 2026-09-25. Design/dispatch baseline: 6869bed. Photo archive: a82aed5.
Assessment by Codex, not a lawyer or independent forensic examiner.

## Bottom line

The repository contains substantial evidence of iterative, hardware-led,
AI-assisted development. It is **not a complete evidentiary archive**, a
comparative originality study, or legal clearance. Keep MIT for material the
project has rights to license; do not describe MIT as proof of noninfringement.
No competing cases were opened or compared in this audit.

## Evidence actually inspected

- 54 commits through 6869bed; photo archive makes 55. History starts with
  setup, then measurements/scans, then CAD, failed trials, fixes and dispatches.
- LICENSE names Austin Griffith and contains the standard MIT grant/disclaimer.
- CLAUDE.md, SOURCES.md, PROCESS.md and PROVENANCE.md document source restrictions.
- Measurements include raw board scan and caliper photographs, row identifiers,
  derived coordinates, and separately identified design choices/assumptions.
- Source, meshes, STEP files, validation reports, viewers, print logs and feedback
  remain in Git. Failed experiments were retained, not erased.
- Both current S1 manifests checked: **28 source/output hash entries match**.
  This checks consistency of recorded bytes, not independent reproduction of
  every historical revision or actual print settings.
- Current CAD/tool source search found no STEP/STL/BREP import calls. Current
  shapes are built from primitives and repository code. This is not proof that
  every line in all history has no outside influence.
- Original setup commit 887ba7b contains documents, not CAD geometry. First
  CAD commit 30ecec9 follows measurement commits, including scan 2c4e363.
- Redacted Gitleaks scan of all 55 reachable commits reported no detected
  secrets. This is not a guarantee about all personal data or image metadata.

## Traceable human decisions and physical iteration

| Evidence | Decision or result |
|---|---|
| 904556b / V1 photos | Captive joystick, pry access and physical feedback |
| f278436, 50630f3 | V2 rectangular buttons/reset access; documented failures |
| 145e386 | Austin insists on flat face-down lid, no support layer |
| 53632f9, 8b0fc03, afbbed9 | Socket trials; saved pre-dispatch CAD correction |
| c7a0315, L2 print log | Lower lid tried despite warning; physical closure failed |
| e082ac8, 53ec430 | Hole alignment corrected from Austin's photos/feedback |
| 5c6f7ab | Austin requests lower seam, stronger walls, hidden catches, one notch |
| d57302f, 6869bed | Approved seven-part plate and hash-linked dispatch |
| a82aed5 / IMG_0839 | User-supplied photo consistent with that production layout |

These records support a development explanation. The current 2:1 visible
shell split, internal detents, supporting rails, stepped cap socket and
corrected opening have recorded reasons. They are **not asserted to be unique
to this product** or verified differences from any competitor.

## Gaps and qualifications

1. **Prior exposure is disclosed.** Phase 0's setup agent had seen prior case
   materials; Austin had handled earlier cases. The log says subsequent geometry
   sessions were isolated and used hardware inputs. Keep this disclosure and
   supporting records. Do not claim nobody ever saw another case.
2. **Some inputs are not archived in Git.** Recent alignment/fit photos are
   named in provenance but only some are committed. Full prompt/tool transcripts
   were not found among tracked files. Preserve originals privately; publish
   redacted, dated excerpts rather than raw chats with credentials/private data.
3. **Print chain is incomplete.** Several dispatch logs lack operator start/end
   records or exact sliced-job files. V1's exact physical source is unresolved.
   IMG_0839 supports production, not successful fit or an exact completion time.
4. **Navigation is stale.** README calls old V3 files current and its build
   section points to historical stl/print. PROCESS retains superseded target
   hardware/methods with later corrections. S1 review artifacts correctly
   preserve pre-approval state, but need to be read with the later dispatch log.
5. **Hashes are not independent timestamps.** All 55 inspected commits are
   unsigned. Git preserves content relationships, not independently verified
   authorship/capture dates. Keep hosted releases/backups and original records;
   consider signed release tags going forward without rewriting old history.
6. **Reproducibility and rights inventory are partial.** Top-level Python
   dependencies are pinned, but no complete transitive environment lock or
   full contributor/provider-terms review was performed. Tool dependencies
   are distinct from imported design geometry. Do not blanket-relicense any
   future third-party assets just because this repo has MIT at its root.

## Legal boundaries — general U.S. guidance, not a clearance opinion

MIT permits copying, modification and commercial distribution subject to its
notice condition. It also disclaims warranties, including noninfringement.
The license cannot grant rights the licensor does not hold; adding it does
not cure unauthorized third-party copying. [OSI MIT text](https://opensource.org/license/mit).

Ideas and methods are not copyrightable; their original written or graphic
expression can be. Functional similarity does not by itself establish copying,
but hardware compatibility is not a blanket defense for copying expressive
CAD/code. [Copyright Office Circular 33](https://www.copyright.gov/circs/circ33.pdf).

For useful articles, mechanical/utilitarian aspects are distinguished from
separable artistic authorship. The README's broad statement that hardware-driven
shape is nobody's property is too categorical across all kinds of IP.
[Copyright Office: useful articles](https://www.copyright.gov/register/va-useful.html).

AI assistance is not a legal shield. Copyrightability depends on human
authorship; purely AI-generated expression is not protected under the Office's
analysis, and prompts alone generally do not establish sufficient control.
Record Austin's decisions, selection, revisions and physical work accurately,
without claiming this audit establishes ownership of every generated element.
[Copyright Office AI report, Part 2](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf).

Patents can cover functional inventions or ornamental product designs; a patent
grants exclusion rights, not general permission to practice an invention. This
audit includes no patent, trademark, trade-dress or international design-rights
clearance. Obtain jurisdiction-specific IP advice before relying on commercial
clearance. [USPTO patent essentials](https://www.uspto.gov/patents/basics/essentials).

## Recommended next steps

1. Fix current-version navigation; add a concise revision → source → print →
   feedback index without deleting failed history.
2. Archive missing user photos with hashes/privacy review; link each to a
   revision. Preserve original uploads and relevant transcripts privately.
3. Record actual slice profiles/job hashes and physical fit results as received.
4. Prepare a release rights/attribution inventory and reproducible build record.
5. If selling against a concern about a specific similar case, have independent
   IP counsel perform the comparison/clearance outside this design clean room.

No geometry or historical records were rewritten for this audit. The photo
was saved with unchanged decoded pixels and removed metadata; original and
public hashes are in prints/s1-photos/IMG_0839.json.
