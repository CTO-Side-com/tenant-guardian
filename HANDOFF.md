---
status: active
phase: v1.0.1 · Hardening (local branch v1.0.1)
next: Merge v1.0.1 to main, push, watch CI
tests: unit 104/104 on macOS, Python 3.13.0 and 3.9.6, default TMPDIR (2026-11-20 18:28); CI last green on v1.0.0 (82/82, run 44748481642)
live: https://github.com/CTO-Side-com/tenant-guardian
updated: 2026-11-20 18:28 +0400
---
# Tenant Guardian: handoff

## Current state

- Published 2026-11-20 17:53: public https://github.com/CTO-Side-com/tenant-guardian (`origin`,
  branch `main`), homepage ctoside.com, topics agent-skills, claude-code, claude-code-plugin, cursor,
  github-copilot, security-audit, multi-tenancy, tenant-isolation, saas, bola, row-level-security.
- History: `af57cf4` imports v1.0.0 exactly as received (extracted ZIP dated 2026-11-20 00:13, the
  original README restored byte for byte); `2f18599` docs; `d9ac458` marketplace rename; `6943002`
  CI runner pin (pushed; CI run 44748481642 green). Last commit before this update: `6943002`.
- `gh skill install CTO-Side-com/tenant-guardian tenant-guardian` from the public repo installs the
  skill folder (checked into a scratch `--dir`); the README tests badge reads "passing".
- Siblings in the same CTOside family: SOC 2 Engineering Guardian (v1.1, public,
  https://github.com/CTO-Side-com/soc2-engineering-guardian) and HIPAA Guardian (public). The new
  README follows the SOC 2 README's layout.
- Marketplace renamed `ctoside` → `ctoside-tenant` (TG-4), so it no longer collides with
  hipaa-guardian's `ctoside`; install is `/plugin install tenant-guardian@ctoside-tenant`.
- 2026-11-20 session: README rewritten; five SVG infographics and a PDF preview added under
  `docs/images/`; this HANDOFF added. No code, manifest, test or example output changed. Final
  review (TG-3) found 4 overclaims and 9 minor gaps, all applied 17:47.
- v1.0.1 on local branch `v1.0.1` (not yet merged or pushed): `aa07683` output guard (TG-6),
  `3af727c` recheck `**` (TG-7), `7fe564c` redaction (TG-8), `1386ba1` CI (TG-9), `4fa3f0a` docs
  and manifests (TG-10), TG-11 fixes `4b7bea3`, `6940508`, `4697b2c` (docs) and `e5b6d7b`, then a
  docs commit. Manifests read 1.0.1.

## What's working

- 36 objectives in 8 areas (CTX 5, API 6, DB 6, CACHE 4, STORE 4, JOB 4, AI 4, LIFE 3), each ending
  in one of five conclusions that `guardian.py validate` enforces.
- `scripts/guardian.py`: init, scan (10 rules, file and line only), plan, validate, report (Markdown,
  PDF, risk register, redacted assessment, hashed manifest), tasks (Jira, Notion, Slack Lists, Slack
  text, Markdown), recheck.
- `scripts/probe.py`: two synthetic tenants, own-tenant positive controls first, then
  `leak_observed` / `denied` / `inconclusive`; dry run; `--allow-network`, `--synthetic-only` and an
  exact `--allow-origin` required; HTTPS unless loopback.
- Tests: 104 in `skills/tenant-guardian/tests` (82 in v1.0.0), including a loopback run of both
  fixture modes, 12 output-guard tests, 4 recheck pattern tests and 6 redaction tests (secret shapes,
  ordinary text kept, no secret in any output file including PDF streams, linear time under 1 s).
  All pass on macOS under the default TMPDIR. `docs/build_example.py` rebuilt the example on a scratch
  copy with the v1.0.1 code: it differs from the shipped one in dates and port-derived hashes only.
- CI (`.github/workflows/tests.yml`): ubuntu-24.04 × Python 3.9/3.11/3.13 plus macos-latest × 3.13,
  `fail-fast: false`, checkout/setup-python v7, unit tests and example build. Green on `main` since
  `6943002`; the v1.0.1 workflow has not run yet.
- Docs: README with ASCII banner, badges, five infographics (`outputs`, `workflow`, `boundary-map`,
  `evidence-model`, `probe-oracle`) and `report-preview.png`; a scratch link check resolved 38/38
  local links and anchors after the review fixes and caught both planted breaks.

## Known problems

- **Redaction is pattern-based.** v1.0.1 masks what SOC 2 v1.1 masks (README, Task exports, lists
  it). Verified by TG-11: names where the label is not last (`SECRET_KEY=`, `PASSWORD_HASH=`), a URL
  password containing `/` (or partly `@`) and other providers' keys pass through; `pwd: /path`,
  `Token: x`, `git@github.com:…` and `logo@2x.png` are over-masked. Same as SOC 2; README says so.
- **A folder name as a watched path matches nothing below it.** `backend` or `backend/` invalidates
  only on that exact path, so the recheck fails open for `backend/app.py`; `backend/**` works.
  Present since v1.0.0; README now says so. Widening `watched()` to treat a bare folder as a prefix
  would fix it: a behaviour change to agree first. A watched path of `.` or `./` passes `validate`,
  then `recheck` exits 1 with "empty pattern" (no traceback; also since v1.0.0).
- **Output guard covers the repository only from its root.** From a subfolder, a link planted
  elsewhere in the repository is outside the working directory and is followed. README tells users
  to run from the root.
- **CSV cells starting with a bare tab or CR are not prefixed.** `cell()` prefixes `=`, `+`, `-`, `@`
  (after leading whitespace), but not a leading tab or CR on its own, which SOC 2's `csv_safe`
  also neutralizes. Out of v1.0.1's scope; a candidate for the next patch.
- **Scanner skip list is exact-name only.** `SKIP` in `scripts/guardian.py:132` is case-sensitive
  folder names, so `fixture/`, `vendor/` or a dump in `db/` is read (TG-3 confirmed; file and line
  only are recorded). `.rs`, `.kt`, `.mjs` and `.vue` are not scanned. README lists the exact names.
- **`session-tenant-context` over-matches.** It also flags ordinary SQL such as
  `UPDATE invoices SET tenant_id = 5` (verified 2026-11-20). README says so.
- `validate` checks structure only: a `confirmed_gap` linked to one `code` item with any non-empty
  `ref` passes. By design (the CLI says "Evidence truth and scope sufficiency require review"); the
  README now says "checks evidence structure", not "validates against evidence".
- CI rebuilds the example without diffing it against `docs/example/`.
- Fixed in TG-5: the first CI run (44748304856) failed before any test ran, because `ubuntu-latest`
  is now Ubuntu 26.04 and setup-python has no 3.9 build for it. Runner pinned to `ubuntu-24.04`, as
  SOC 2 did.
- Fixed in v1.0.1, each with tests watched red first:
  - TG-6: `output()` refused any symlinked folder above the path, so macOS `/var` and `/tmp` broke
    7 tests and `--out /tmp/<folder>/...` (`--out /tmp/x.json` stays refused: `/tmp` is then the
    file's own folder). It now refuses the file, its folder and symlinks inside the
    working directory only (SOC 2 SG-1). Red: 8 errors and 1 failure under the default TMPDIR.
  - TG-7: recheck's `PurePosixPath.match` never let `**` cross a folder, so `backend/**` failed
    open on `backend/api/x.py`. A root-anchored match where `**` spans folders is added.
  - TG-8: `clean()` missed joined labels, quoted JSON keys, provider keys, URL passwords, PEM
    blocks and phones, and its email pattern was quadratic (30 s on 100k chars of `a.`). Ported
    SOC 2 v1.1's patterns: 0.07 s on the same input.
  - TG-9: CI gained a macOS job, `fail-fast: false` and v7 actions.
  - TG-11 review (no blocker; gate 100/100 on both Pythons, plants 2 of 3 caught):
    - S1 (`4b7bea3`): TG-6 collapsed `..` in `output()` only, so `report --out out/link/..`
      hashed decoy files and replaced an `assessment-redacted.json` source in `out/`. Red: both new
      tests failed on their assertions.
    - M1 (`6940508`): no test covered `realpath` in `inside()` (the reviewer's plant P1 passed all
      100). New test added; the reviewer re-runs P1 against it.
    - M2 to M6: README and this file corrected (Safe writes, `/tmp` wording, joined-name redaction
      limits, folder-name watch paths).
    - Re-check of `4697b2c`: gate 103/103 on both Pythons; P1 now fails the new alias test on its
      own assertion (`AssertionError: ValueError not raised`); S1 closed for report and tasks.
    - R1 (`e5b6d7b`, since v1.0.0): on macOS `report --out OUT` passed the "would replace the
      source assessment" check (`resolve()` does not fold case) and overwrote
      `out/assessment-redacted.json`. Now compared with `os.path.samefile`. Red: the CLI exited 0.
      The test skips on case-sensitive filesystems; the macOS CI job runs it.

## Decisions

- [x] 2026-11-20 · Rewrite the README after SOC 2 Engineering Guardian's (sections, ASCII banner,
      infographics) and add HANDOFF.md (your request, 17:27).
- [x] 2026-11-20 · README targets the planned public home `CTO-Side-com/tenant-guardian` and the
      current manifest name `ctoside`; manifests left untouched (assumption stated in session).
- [x] 2026-11-20 · Report preview built with Pillow in a scratch script only; no dependency added.
- [x] 2026-11-20 · Apply all 13 TG-3 findings, including the section reorder (Install, Use it and
      Example now follow "How an assessment runs"). The review report stayed in the session
      scratchpad; its findings are folded into Known problems.
- [x] 2026-11-20 · v1.0.1 bumps the plugin manifests only. `references/checks.json` stays at 1.0.0:
      it is the catalog version that `validate` matches against `catalog_version`, and the catalog
      did not change, so existing assessments stay valid.
- [x] 2026-11-20 · Publish now as v1.0.0 (answered 17:50, "publish"): `git init`, import v1.0.0 as
      received as the first commit, then the docs commit, then the marketplace rename; create public
      `CTO-Side-com/tenant-guardian` with the siblings' homepage and topic style, push `main`.
      v1.0.1 hardening stays open.
- [x] 2026-11-20 · Marketplace name `ctoside-tenant` (answered 17:51).
- [x] 2026-11-20 · Build v1.0.1 (answered 18:02 "yes"): narrowed output symlink guard, `**` that
      crosses folders in recheck, redaction widened toward SOC 2 v1.1, CI with a macOS job,
      `fail-fast: false` and v7 actions; README, HANDOFF and manifests at 1.0.1. In-session on branch
      `v1.0.1`, one commit per change, final review by general-purpose (strongest model, high effort:
      redaction and the output guard are security-critical), then merge to `main` and push.

## Needs you

- [x] 2026-11-20 · Marketplace name: rename `ctoside` to `ctoside-tenant` in both manifests and the
      README install line, as SOC 2 did with `ctoside-soc2`? (recommend rename; answered: rename)
- [x] 2026-11-20 · `git init` with v1.0.0 as received as the initial commit, then this docs change as
      a second commit? (recommended; answered by "publish")
- [x] 2026-11-20 · v1.0.1 hardening from SOC 2 v1.1: narrowed symlink guard, nested-folder recheck,
      wider redaction, `macos-latest` in the CI matrix? (recommend yes; answered 18:02 "yes", push
      when done)
- [x] 2026-11-20 · Publish to public `CTO-Side-com/tenant-guardian` with the siblings' homepage and
      topics? (answered 17:50: "publish", before v1.0.1)

## Tasks

**Code:** TG

| ID | Task | Status | Started | Finished |
|---|---|---|---|---|
| TG-1 | README after SOC 2 Guardian: banner, badges, five infographics, preview | done | 2026-11-20 17:27 | 2026-11-20 17:38 |
| TG-2 | HANDOFF.md | done | 2026-11-20 17:38 | 2026-11-20 17:38 |
| TG-3 | Final review of README and images against the code | done | 2026-11-20 17:38 | 2026-11-20 17:47 |
| TG-4 | Rename marketplace to `ctoside-tenant` | done | 2026-11-20 17:51 | 2026-11-20 17:55 |
| TG-5 | Publish: git init, commits, public repo, push, CI | done | 2026-11-20 17:51 | 2026-11-20 17:58 |
| TG-6 | Narrow the output symlink guard (security-critical) | done | 2026-11-20 18:03 | 2026-11-20 18:06 |
| TG-7 | Recheck: `**` crosses folders | done | 2026-11-20 18:06 | 2026-11-20 18:07 |
| TG-8 | Widen redaction (security-critical) | done | 2026-11-20 18:07 | 2026-11-20 18:09 |
| TG-9 | CI: macOS job, fail-fast off, v7 actions | done | 2026-11-20 18:09 | 2026-11-20 18:10 |
| TG-10 | README, HANDOFF, manifests 1.0.1 | done | 2026-11-20 18:10 | 2026-11-20 18:11 |
| TG-11 | Final review of v1.0.1 (security-critical) | done | 2026-11-20 18:12 | 2026-11-20 18:28 |

## Regenerate the README preview

`docs/images/report-preview.png` is pages 1, 2 and 9 of `docs/example/TENANT-ISOLATION.pdf`. Pillow
is used only here, in a scratch script, never in committed code. With `$S` a scratch folder:

```bash
for p in 1 2 9; do pdftoppm -r 110 -png -f $p -l $p -singlefile docs/example/TENANT-ISOLATION.pdf "$S/page-$p"; done
python3 "$S/compose_preview.py" "$S" docs/images/report-preview.png   # keep it under 400 KB (116 KB today)
```

`$S/compose_preview.py`:

```python
import sys
from PIL import Image, ImageDraw, ImageFilter
scratch, out = sys.argv[1], sys.argv[2]
pages = [scratch + '/page-%s.png' % n for n in ('1', '2', '9')]
PW, PAD, GAP, BG = 470, 32, 26, (244, 243, 239)
ims = []
for p in pages:
    im = Image.open(p).convert('RGB')
    ims.append(im.resize((PW, round(im.height * PW / im.width)), Image.LANCZOS))
H = max(i.height for i in ims) + 2 * PAD
W = 2 * PAD + 3 * PW + 2 * GAP
shadow = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(shadow)
x = PAD
for im in ims:
    d.rectangle([x + 3, PAD + 5, x + im.width + 3, PAD + im.height + 5], fill=(214, 212, 204))
    x += PW + GAP
canvas = shadow.filter(ImageFilter.GaussianBlur(5))
x = PAD
d = ImageDraw.Draw(canvas)
for im in ims:
    canvas.paste(im, (x, PAD))
    d.rectangle([x, PAD, x + im.width - 1, PAD + im.height - 1], outline=(225, 224, 217))
    x += PW + GAP
canvas = canvas.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
canvas.save(out, optimize=True)
```

The infographics are hand-written SVG in the SOC 2 README's visual system (`#101827` ink, `#39B9D0`
accent, `#fcfcfb` card, system font stack, 960 px wide). Check a change with
`rsvg-convert -w 1200 docs/images/<name>.svg -o "$S/<name>.png"` and look at the PNG; any count in
them (36 objectives, 10 rules, per-area counts) must change with `checks.json` or the scanner.

## Next steps

1. Fast-forward `main` to `v1.0.1`, list the files, push, watch CI (Ubuntu 3.9/3.11/3.13 and the
   macOS job).
2. Update this file: front matter (phase v1.0.1 · Published, CI run and counts).

## In flight

- Since 2026-11-20 18:28: fast-forward `main` to `v1.0.1`, push `main`, watch CI (4 jobs). Nothing uncommitted.
