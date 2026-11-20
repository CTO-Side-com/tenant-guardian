---
status: active
phase: v1.0.0 · Docs refresh
next: Your calls under Needs you (git, marketplace name, v1.0.1, publish)
tests: unit 82/82 with TMPDIR inside the project (3.9.6 and 3.13.0); 75/82 under the macOS default TMPDIR (7 symlink-guard errors); example build green (2026-11-20)
updated: 2026-11-20 17:48 +0400
---
# Tenant Guardian: handoff

## Current state

- v1.0.0 as received: an extracted ZIP dated 2026-11-20 00:13, manifests at 1.0.0. **Not a git
  repository and not published**: `CTO-Side-com/tenant-guardian` does not exist yet, so there is no
  last commit.
- Siblings in the same CTOside family: SOC 2 Engineering Guardian (v1.1, public,
  https://github.com/CTO-Side-com/soc2-engineering-guardian) and HIPAA Guardian (public). The new
  README follows the SOC 2 README's layout.
- Marketplace renamed `ctoside` → `ctoside-tenant` (TG-4), so it no longer collides with
  hipaa-guardian's `ctoside`; install is `/plugin install tenant-guardian@ctoside-tenant`.
- 2026-11-20 session: README rewritten; five SVG infographics and a PDF preview added under
  `docs/images/`; this HANDOFF added. No code, manifest, test or example output changed. Final
  review (TG-3) found 4 overclaims and 9 minor gaps, all applied 17:47.

## What's working

- 36 objectives in 8 areas (CTX 5, API 6, DB 6, CACHE 4, STORE 4, JOB 4, AI 4, LIFE 3), each ending
  in one of five conclusions that `guardian.py validate` enforces.
- `scripts/guardian.py`: init, scan (10 rules, file and line only), plan, validate, report (Markdown,
  PDF, risk register, redacted assessment, hashed manifest), tasks (Jira, Notion, Slack Lists, Slack
  text, Markdown), recheck.
- `scripts/probe.py`: two synthetic tenants, own-tenant positive controls first, then
  `leak_observed` / `denied` / `inconclusive`; dry run; `--allow-network`, `--synthetic-only` and an
  exact `--allow-origin` required; HTTPS unless loopback.
- Tests: 82 in `skills/tenant-guardian/tests`, including a loopback run of both fixture modes.
  `docs/build_example.py` rebuilt the example on a scratch copy: vulnerable 2/2 `leak_observed`,
  isolated 2/2 `denied`; the rebuilt `TENANT-ISOLATION.md` matches the shipped one apart from dates
  and hashes.
- CI (`.github/workflows/tests.yml`): ubuntu-latest, Python 3.9/3.11/3.13, unit tests and example
  build. It has never run: there is no remote yet.
- Docs: README with ASCII banner, badges, five infographics (`outputs`, `workflow`, `boundary-map`,
  `evidence-model`, `probe-oracle`) and `report-preview.png`; a scratch link check resolved 38/38
  local links and anchors after the review fixes and caught both planted breaks.

## Known problems

- **Symlink guard too strict on macOS.** `output()` in `scripts/guardian.py:24` refuses a path when
  any folder above it is a symlink. `/var` and `/tmp` are symlinks on macOS, so 7 tests error under
  the default TMPDIR and `--out /tmp/...` is refused. CI is Ubuntu-only and never shows it. SOC 2 v1.1
  fixed the same guard (SG-1: check the file, its folder, and folders inside the working directory).
  Verified 2026-11-20; README documents the TMPDIR workaround.
- **Recheck fails open on nested changes.** `PurePosixPath.match` never crosses a folder, so
  `watched_paths: ["backend/**"]` keeps an objective's conclusion when `backend/sub/x.py` changes.
  Verified 2026-11-20 (same bug as SOC 2's correction prompt 2). README documents the behaviour.
- **Redaction is narrower than SOC 2 v1.1's.** `clean()` masks emails, SSN-format numbers, `Bearer`
  tokens and values after a standalone `password`/`secret`/`token`/`api_key` label. Verified to miss
  `DB_PASSWORD=`, `access_token=`, `api-key=` and `sk-…` (2026-11-20); has no pattern for `AKIA…`,
  `ghp_…`, bare JWTs or PEM blocks. Quoted JSON keys (`"password": "x"`) also pass through, since
  the quote sits between label and colon (verified 2026-11-20). README lists exactly what is masked.
- **Scanner skip list is exact-name only.** `SKIP` in `scripts/guardian.py:132` is case-sensitive
  folder names, so `fixture/`, `vendor/` or a dump in `db/` is read (TG-3 confirmed; file and line
  only are recorded). `.rs`, `.kt`, `.mjs` and `.vue` are not scanned. README lists the exact names.
- **`session-tenant-context` over-matches.** It also flags ordinary SQL such as
  `UPDATE invoices SET tenant_id = 5` (verified 2026-11-20). README says so.
- `validate` checks structure only: a `confirmed_gap` linked to one `code` item with any non-empty
  `ref` passes. By design (the CLI says "Evidence truth and scope sufficiency require review"); the
  README now says "checks evidence structure", not "validates against evidence".
- README's tests badge and remote install commands (`/plugin marketplace add`, `gh skill install`,
  git clone) work only once `CTO-Side-com/tenant-guardian` exists.
- CI rebuilds the example without diffing it against `docs/example/`.

## Decisions

- [x] 2026-11-20 · Rewrite the README after SOC 2 Engineering Guardian's (sections, ASCII banner,
      infographics) and add HANDOFF.md (your request, 17:27).
- [x] 2026-11-20 · README targets the planned public home `CTO-Side-com/tenant-guardian` and the
      current manifest name `ctoside`; manifests left untouched (assumption stated in session).
- [x] 2026-11-20 · Report preview built with Pillow in a scratch script only; no dependency added.
- [x] 2026-11-20 · Apply all 13 TG-3 findings, including the section reorder (Install, Use it and
      Example now follow "How an assessment runs"). The review report stayed in the session
      scratchpad; its findings are folded into Known problems.
- [x] 2026-11-20 · Publish now as v1.0.0 (answered 17:50, "publish"): `git init`, import v1.0.0 as
      received as the first commit, then the docs commit, then the marketplace rename; create public
      `CTO-Side-com/tenant-guardian` with the siblings' homepage and topic style, push `main`.
      v1.0.1 hardening stays open.
- [x] 2026-11-20 · Marketplace name `ctoside-tenant` (answered 17:51).

## Needs you

- [x] 2026-11-20 · Marketplace name: rename `ctoside` to `ctoside-tenant` in both manifests and the
      README install line, as SOC 2 did with `ctoside-soc2`? (recommend rename; answered: rename)
- [x] 2026-11-20 · `git init` with v1.0.0 as received as the initial commit, then this docs change as
      a second commit? (recommended; answered by "publish")
- [ ] 2026-11-20 · v1.0.1 hardening from SOC 2 v1.1: narrowed symlink guard, nested-folder recheck,
      wider redaction, `macos-latest` in the CI matrix? (recommend yes)
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
| TG-5 | Publish: git init, commits, public repo, push, CI | active | 2026-11-20 17:51 | |

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

1. Answer Needs you.
2. If yes to git: `git init`, commit v1.0.0 as received (`chore: import tenant guardian v1.0.0`),
   then `docs: rewrite readme with infographics and add handoff` with a `Task: TG-1` trailer.
3. v1.0.1 hardening per Needs you, each fix with a red-then-green test; update the README lines that
   describe today's behaviour (macOS TMPDIR note, recheck patterns, redaction list, skip list).
4. Publish when you say "push".

## In flight

- TG-5 publish in progress (2026-11-20 17:51). Order: `git init -b main`; commit 1 imports v1.0.0 as
  received (original README restored for it); commit 2 the docs; commit 3 the marketplace rename;
  `gh repo create CTO-Side-com/tenant-guardian --public`; push `main`; watch the CI run. If the
  session ends mid-way, check `git log`, `git remote -v` and `gh run list` and carry on from there.
