---
status: active
phase: v1.0.2 · Publish
next: push v1.0.2, then Needs you
tests: local macOS 109/109 on 3.13.0 and 3.9.6 at 4498884 (2026-11-21); CI pending for v1.0.2
live: https://github.com/CTO-Side-com/tenant-guardian
updated: 2026-11-21 00:33 +0400
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
- v1.0.1 pushed 2026-11-20 18:31: `main` fast-forwarded from `b4ace73` to `c61a552`, CI run 44753789907 green on
  all 4 jobs. Commits: `aa07683` output guard (TG-6),
  `3af727c` recheck `**` (TG-7), `7fe564c` redaction (TG-8), `1386ba1` CI (TG-9), `4fa3f0a` docs
  and manifests (TG-10), TG-11 fixes `4b7bea3`, `6940508`, `4697b2c` (docs) and `e5b6d7b`, then
  `c61a552` (docs). Manifests read 1.0.1. `20da0e4` (this HANDOFF's release notes) followed; CI run
  44754209342 green on all 4 jobs. Last commit before this update: `20da0e4`.

## What's working

- 36 objectives in 8 areas (CTX 5, API 6, DB 6, CACHE 4, STORE 4, JOB 4, AI 4, LIFE 3), each ending
  in one of five conclusions that `guardian.py validate` enforces.
- `scripts/guardian.py`: init, scan (10 rules, file and line only), plan, validate, report (Markdown,
  PDF, risk register, redacted assessment, hashed manifest), tasks (Jira, Notion, Slack Lists, Slack
  text, Markdown), recheck.
- `scripts/probe.py`: two synthetic tenants, own-tenant positive controls first, then
  `leak_observed` / `denied` / `inconclusive`; dry run; `--allow-network`, `--synthetic-only` and an
  exact `--allow-origin` required; HTTPS unless loopback.
- Tests: 109 in `skills/tenant-guardian/tests` (82 in v1.0.0), including a loopback run of both
  fixture modes, 12 output-guard tests, 8 recheck pattern tests, a CSV tab/CR test and 6 redaction
  tests (secret shapes, ordinary text kept, no secret in any output file including PDF streams,
  linear time under 1 s). 109/109 on macOS with Python 3.13.0 and 3.9.6 (2026-11-21 00:22).
  `docs/build_example.py` rebuilt the example on a scratch copy with the v1.0.2 code: dates differ,
  every CSV is byte-identical.
- CI (`.github/workflows/tests.yml`): ubuntu-24.04 × Python 3.9/3.11/3.13 plus macos-latest × 3.13,
  `fail-fast: false`, checkout/setup-python v7, unit tests and example build. Green on `main` since
  `6943002`; v1.0.1 run 44753789907 green on all 4 jobs.
- Docs: README with ASCII banner, badges, five infographics (`outputs`, `workflow`, `boundary-map`,
  `evidence-model`, `probe-oracle`) and `report-preview.png`; a scratch link check resolved 38/38
  local links and anchors after the review fixes and caught both planted breaks.

## Known problems

- **Redaction is pattern-based.** v1.0.1 masks what SOC 2 v1.1 masks (README, Task exports, lists
  it). Verified by TG-11: names where the label is not last (`SECRET_KEY=`, `PASSWORD_HASH=`), a URL
  password containing `/` (or partly `@`) and other providers' keys pass through; `pwd: /path`,
  `Token: x`, `git@github.com:…` and `logo@2x.png` are over-masked. Same as SOC 2; README says so.
- **A watched path starting with `/` matches nothing (since v1.0.0).** `validate` accepts `/backend`,
  `//backend` and `/**`, but changed paths are always relative, so `watched()` never matches them and
  the recheck fails open for anyone writing the root anchor as `.gitignore` and CODEOWNERS do (TG-15
  finding 4). README now says so. Fix waits on Needs you: treat a leading `/` as rooted, or reject it.
- **Folder patterns widen by suffix too (v1.0.2, by design).** `migrations` covers
  `apps/x/migrations/0001.py`, and `api` covers `services/api/handlers.py`, because the end-anchored
  rule that already let `api` match a file `services/api` now also accepts that folder. More
  invalidation, never less; README says so.
- **Output guard covers the repository only from its root.** From a subfolder, a link planted
  elsewhere in the repository is outside the working directory and is followed. README tells users
  to run from the root.
- **Scanner skip list is exact-name only.** `SKIP` in `scripts/guardian.py:132` is case-sensitive
  folder names, so `fixture/`, `vendor/` or a dump in `db/` is read (TG-3 confirmed; file and line
  only are recorded). `.rs`, `.kt`, `.mjs` and `.vue` are not scanned. README lists the exact names.
- **`session-tenant-context` over-matches.** It also flags ordinary SQL such as
  `UPDATE invoices SET tenant_id = 5` (verified 2026-11-20). README says so.
- `validate` checks structure only: a `confirmed_gap` linked to one `code` item with any non-empty
  `ref` passes. By design (the CLI says "Evidence truth and scope sufficiency require review"); the
  README now says "checks evidence structure", not "validates against evidence".
- CI rebuilds the example without diffing it against `docs/example/`.
- **The loopback probe test is slow on the macOS runner.** `test_real_loopback_secure_and_vulnerable`
  took 36 s of the macOS job's 37 s (run 44753789907) against ~1 s locally and on Ubuntu. Cause not
  investigated (present since v1.0.0's test; not a v1.0.1 change).
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
- Fixed in v1.0.2, each with tests watched red first:
  - TG-12 (`1968ccc`, since v1.0.0): a folder name in `watched_paths` (`backend`, `backend/`,
    `services/*`) matched only that path, so a recheck failed open on `backend/app.py`; `.` and `./`
    exited 1 with "empty pattern". Every rule now also accepts a match on a folder above the changed
    path, and `.` names the root. Red: 7 failures and 2 `ValueError: empty pattern` errors.
    `test_recheck_folder_name_ignores_lookalike_paths` passes before and after (a guard, not red).
  - TG-13 (`e8431f8`, since v1.0.0): `cell()` did not prefix a cell starting with a tab or CR
    (CR was flattened to a space first). Now checked before flattening, as SOC 2's `csv_safe` does.
    Red: 4 failures. The shipped example CSVs are unchanged by it.
  - TG-15 review (verdict ship; gate 109/109 on 3.13.0 and 3.9.6; plants 2 of 3 caught): over
    661,752 pattern/path pairs, 0 matches lost against `main` and 0 new exceptions (bound 0 each);
    `cell()` agrees with SOC 2's `csv_safe` on every generated input. P1 (string-prefix folder
    compare) failed the lookalike guard test on its own assertion. Findings, all minor:
    - 1: P3 (prefix any cell with leading whitespace) passed all 109. The CSV test now also
      requires `' team a'` and `'  note'` to stay unprefixed (`1fd54d5`). Re-check at `4498884`:
      P3 now fails it on its own assertions (`AssertionError: True is not false`, failures=2).
    - 2, 3: README's CSV sentence (a `\n` before a tab skips the prefix, as in SOC 2) and its
      contradictory `*.sql` sentence reworded.
    - 4: absolute watched paths, filed under Known problems and Needs you.

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
- [x] 2026-11-21 · Build v1.0.2 (answered 00:19 "folder name shall be adaptive .csv yes, make the
      changes and push"). "Adaptive" read as: a pattern names a file or a folder, and a folder covers
      every file under it, with `.` as the root. In-session on branch `v1.0.2`, final review by the
      `reviewer` agent (standard risk), then merge to `main` and push. Manifests at 1.0.2;
      `references/checks.json` stays at 1.0.0 for the same reason as in v1.0.1.

## Needs you

- [ ] 2026-11-20 · Tag and publish a GitHub release `v1.0.1`? (recommend yes; not done unasked)
- [ ] 2026-11-21 · Treat a watched path starting with `/` (`/backend`, `/**`) as anchored at the
      repository root, as `.gitignore` and CODEOWNERS do, instead of matching nothing? It only adds
      invalidations. The alternative is to reject it in `validate`, which breaks assessments that
      have one. (recommend rooted)

- [x] 2026-11-20 · v1.0.2: make a bare folder in `watched_paths` (`backend`, `backend/`) match the files
      under it, so a recheck no longer fails open there? It only adds invalidations. (recommend yes;
      answered 2026-11-21 00:19: "folder name shall be adaptive", make the changes and push)
- [x] 2026-11-20 · v1.0.2: prefix CSV cells that start with a bare tab or CR, as SOC 2's `csv_safe` does?
      (recommend yes; answered 2026-11-21 00:19: ".csv yes", make the changes and push)

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
| TG-12 | Recheck: a pattern naming a folder covers the files under it | done | 2026-11-21 00:20 | 2026-11-21 00:21 |
| TG-13 | CSV: prefix cells starting with a tab or CR | done | 2026-11-21 00:21 | 2026-11-21 00:22 |
| TG-14 | README, HANDOFF, manifests 1.0.2 | done | 2026-11-21 00:22 | 2026-11-21 00:23 |
| TG-15 | Final review of v1.0.2 | done | 2026-11-21 00:23 | 2026-11-21 00:33 |

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

1. If `main` on GitHub is not yet at this commit: `git switch main`, `git merge --ff-only v1.0.2`,
   list the files in `origin/main..main`, `git push origin main` (authorized 2026-11-21 00:19).
2. Watch the CI run for that push; record its ID and result here.
3. Still open in Needs you: the GitHub release tag and rooted `/` watched paths. Optional: why the
   loopback probe test takes 36 s on the macOS runner.

## In flight

- v1.0.2 merge and push: `v1.0.2` fast-forwards into `main`, then `git push origin main`. TG-15
  review and re-check are done (report `<session scratchpad>/tg15-review.md`,
  verdict ship; its worktree is removed).
- Local branch `v1.0.1` is fully merged into `main` (kept).
