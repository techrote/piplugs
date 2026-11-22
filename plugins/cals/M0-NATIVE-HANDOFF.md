# CALS M0 — Source-exact CyberSand native qualification handoff

**Status:** Source-verified procedure; **not executed** against a Godot/native binary by CALS.  
**Last source inspection:** 2026-11-22. **Target repo:** [techrote/cybersand](https://github.com/techrote/cybersand).  
**Baseline inspected:** `00cdb02f103265b6dc5224c68283e9a0c8cb449f` (refresh on execution).  
**Purpose:** Use *existing* CyberSand native tests and controlled user-data isolation to qualify CALS's future real generated-start path, without introducing a second World, network interface or engine change.

## 1. What already exists

Two different existing tests serve different purposes and **must not be conflated**:

| Existing code | What it actually exercises | What it does not prove |
|---|---|---|
| [`godot/tests/test_workbench_generator_installed.gd`](https://github.com/techrote/cybersand/blob/main/godot/tests/test_workbench_generator_installed.gd) | Full Shared Workbench; discovers a real packaged `gen007-deepworks` profile; generates a 512×512 native final play plane; installs it; paints Wall/Metal; saves; on second process regenerates/reopens and continues painting. Emits `WB_GENERATOR_INSTALLED checks=N failures=0`. | It does **not** import arbitrary CALS region proposals, or establish 2048×1024 gameplay route correctness |
| [`tools/qualify_workbench_landscapes.py`](https://github.com/techrote/cybersand/blob/main/tools/qualify_workbench_landscapes.py) | Source/runtime-binary identity gates; verifies exact Godot 4.7 pin and Rapier/native provenance; isolates each landscape's user data; source-pinned real Workbench install/reopen; records process logs, fixtures, SHA-256s and evidence. | These landscape fixtures are prepared Setup-v2 maps (e.g. SANDMAPS), **not** GEN-007 recipes or CALS's authored World Bible |

The second runner already imports [`case_environment`](https://github.com/techrote/cybersand/blob/main/tools/ci/stress_physical_godot.py), which isolates `XDG_DATA_HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, and on Windows `APPDATA` and `LOCALAPPDATA`, plus `TMP/TEMP/TMPDIR`. **Reuse it rather than write a new process manager.**

The actual `world_art_capture.gd` + `world_design_pack_adapter.gd` path renders **presentation-only, synthetic-condition materials** and does not perform native simulation or Workbench import. A PNG from this route is not a native World acceptance result.

## 2. Preconditions before launching

- Work in a **disposable, full clone** of CyberSand at an **explicit HEAD SHA**; do not use an unreviewed Draft branch or a valued owner Workbench user directory. Run `git status --porcelain`, `git rev-parse HEAD`, `git lfs ls-files`, confirm required native/Rapier DLLs are materialized rather than Git LFS pointers.
- Use the source-pinned **Godot 4.7** executable and **matching GDExtension/DLL**. `tools/ci/check_repository.py` validates relevant recorded source/runtime provenance. A successful JSON parse is not a native binary verification.
- On Windows, choose the **console** binary for preserving actual process logs; the launcher is separate. Verify `<godot> --version` matches the expected `4.7.stable.official.5b4e0cb0f` where the qualified runner requires it.
- Pick an absolute, **new** evidence output directory; the official landscape runner refuses to reuse one. Do not send private content or credentials to models.
- Run no paid inference and make no GitHub merge/publication. All code below assumes a valid local CyberSand checkout and a source-matched binary; those are unavailable in the CALS implementation CI environment.

## 3. Recommended first real qualification: existing source-pinned runner

Run **from the CyberSand checkout root**, with PowerShell quoting corrected for your local locations:

```powershell
# Example paths only. Replace with the actual source clone and pinned console executable.
Set-Location 'C:\work\cybersand'
$Godot = 'C:\Godot_v4.7-stable_win64_console.exe'
$Evidence = 'C:\work\cals-evidence\landscape-001' # MUST NOT exist

git rev-parse HEAD
git status --porcelain
git lfs ls-files
& $Godot --version

# The runner validates native/Rapier/source identity BEFORE installing maps.
# --map is an optional bounded subset; 'graven-keel' exists in the inspected manifest.
python tools/qualify_workbench_landscapes.py `
  --godot $Godot `
  --output $Evidence `
  --map graven-keel `
  --process-timeout 240 `
  --campaign-timeout 900
if ($LASTEXITCODE -ne 0) { throw 'CALS native landscape qualification failed: inspect logs' }
```

Inspect `$Evidence/qualification.json`, `landscape-manifest.json`, each `*/process.log` and `*/process.json`, the generated source grids and saved-start hashes. The runner itself checks that install/reopen happened in **different process IDs**, retained exact source/native identities, compared independently replayed source material and confirmed saved-start identity. The runner has network-dependent fixture download unless a verified local `--fixture-dir` is supplied; a missing source URL or timeout is a **failed/blocked test**, never a reason to substitute content.

This test is valuable as a **baseline of the engine and Workbench persistence** for CALS, but **does not** validate GEN-007 generation.

## 4. Required GEN-007 authoring qualification (separate test)

The existing `test_workbench_generator_installed.gd` has no separate orchestration wrapper in CALS yet. It requires a **disposable Godot user-data root shared only by its import, install and reopen processes**, not your normal `%APPDATA%/Godot/app_userdata` directory.

Suggested *operator script outline* (not run or qualified by CALS):

```powershell
Set-Location 'C:\work\cybersand'
$Godot   = 'C:\Godot_v4.7-stable_win64_console.exe'
$Project = (Resolve-Path '.\godot').Path
$Case    = 'C:\work\cals-evidence\gen007-001'   # new, disposable, not existing
New-Item -ItemType Directory -Force -Path $Case | Out-Null
foreach ($name in @('APPDATA','LOCALAPPDATA','TEMP','TMP','TMPDIR','XDG_DATA_HOME','XDG_CONFIG_HOME','XDG_CACHE_HOME')) {
    $location = Join-Path $Case $name.ToLowerInvariant()
    New-Item -ItemType Directory -Force -Path $location | Out-Null
    Set-Item -Path ("Env:" + $name) -Value $location
}
# Use a NEW PowerShell process for this isolated environment:
$env:WB_GENERATOR_SCREENSHOTS = Join-Path $Case 'screenshots'
$env:WB_GENERATOR_REQUIRE_GRAPHICS = '0'
$env:WB_GENERATOR_REOPEN = '0'

# Imports project resources; then first fresh native install+paint+Save.
& $Godot --headless --path $Project --editor --quit 2>&1 |
  Tee-Object -FilePath (Join-Path $Case 'import.log')
if ($LASTEXITCODE -ne 0) { throw 'Godot project import failed' }
& $Godot --headless --path $Project --script 'res://tests/test_workbench_generator_installed.gd' 2>&1 |
  Tee-Object -FilePath (Join-Path $Case 'install.log')
if ($LASTEXITCODE -ne 0) { throw 'GEN-007 install/save failed' }

# Different process, same isolated user:// tree.
$env:WB_GENERATOR_REOPEN = '1'
& $Godot --headless --path $Project --script 'res://tests/test_workbench_generator_installed.gd' 2>&1 |
  Tee-Object -FilePath (Join-Path $Case 'reopen.log')
if ($LASTEXITCODE -ne 0) { throw 'GEN-007 fresh-process reopen failed' }
```

**Caution:** This is a handoff outline, not a shipped/hardened test runner. PowerShell environment changes persist within that PowerShell session; **launch it from a fresh dedicated terminal**, or manage environment via a child process helper. Verify both `install.log` and `reopen.log` show exactly one positive `WB_GENERATOR_INSTALLED checks=N failures=0` and **no Godot `ERROR:`/script parse failures**, and retain actual two-process PID/executable/hash evidence for acceptance. If the test runs in a truly headless display, screenshots will be absent; graphical evidence needs a separately validated graphical run. The named test save is fixed (`wb-generator-installed-regression`), so do **not** run it in your ordinary profile.

To prevent accidental profile contamination, the preferred follow-up is a narrowly scoped external **safe launch wrapper** that uses CyberSand's existing `case_environment()` and process runner, hashes source and results, and refuses non-disposable output directories. Do not implement a new Godot/GDExtension API to make this test run.

## 5. CALS mapping and remaining gates

Once the existing tests pass with fresh evidence:

| CALS capability | Existing source evidence required | Status at plan time |
|---|---|---|
| `validateProposal` | CALS offline bounds and joints validator + native GEN-007 recipe acceptance | Offline 32 tests pass; native untested |
| `generatePreview` | `test_workbench_generator_installed.gd` native preview + copied material source receipt | Existing test **identified**, not run by CALS |
| `installApproved` | Existing Workbench generated installation in same native World, exact source receipt | Existing test **identified**, not run by CALS |
| `readback` | Actual native stored material/renderer result | Only source-defined test assertions so far |
| `saveAndReopen` | Two-process GEN-007 test with identical isolated user-data and exact recipe/edits readback | Existing test **identified**, not run by CALS |
| Large landscaped start | `qualify_workbench_landscapes.py` source/runtime+install/reopen campaign | Existing runner **identified**, not run by CALS |

**CALS does not yet support importing an arbitrary multi-agent proposal** through the existing generator dialog. Passing the built-in 512² GEN-007 test only establishes that a known recipe works. M3 still needs to verify whether a standard external recipe/profile selection is sufficient for the team's output without engine modifications.

There are three levels of evidence: (1) source inspection (this document); (2) actual pinned Windows/native runner + install/reopen receipts; (3) owner playability and artistic evaluation. Do not promote one into the next.

**Next engineering gate:** [CALS-M0-NATIVE-001, issue #3](https://github.com/techrote/piplugs/issues/3). The OMP host/permissions gate is [issue #2](https://github.com/techrote/piplugs/issues/2).
