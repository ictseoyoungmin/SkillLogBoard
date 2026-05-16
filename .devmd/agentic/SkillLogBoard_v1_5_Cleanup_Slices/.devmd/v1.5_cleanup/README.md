# v1.5 Cleanup

## Goal

Close the v1.5 Performance, Retention, and Operational Rules milestone cleanly.

## Cleanup Theme

v1.5 already has the correct functional pillars. This cleanup focuses on:

- safer CLI wording
- metric-mode-aware retention policy
- lighter index rebuild behavior
- explicit CI/release-candidate evidence

## Expected Final State

```text
skilllog prune remains non-destructive by default
--execute wording cannot be mistaken for deletion
retention best protection understands max/min metric direction
project index does not enumerate huge artifact lists unnecessarily
v1.5 release candidate note records local and CI verification status
```
