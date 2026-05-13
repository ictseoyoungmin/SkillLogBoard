# SkillLogBoard v1.0 Cleanup

## Purpose

Resolve post-review cleanup items before release-candidate packaging or TestPyPI work.

## Cleanup Items

1. Align `--poll-interval` with server health/config and browser refresh behavior.
2. Improve project watch discovery performance for larger run directories.
3. Restore at least one real HTTP smoke test for the Live Board server.
4. Make GPU monitor empty parse behavior explicit and visible.
5. Synchronize docs/status/changelog and run final verification.

## Rule

Do not start v1.1 UI polish or release packaging until this cleanup is completed or explicitly deferred.
