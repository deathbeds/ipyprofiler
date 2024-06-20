---
name: Release
about: Prepare for a release
labels: maintenance
---

- [ ] merge all outstanding PRs
- [ ] ensure the versions have been bumped (check with `pixi lint`)
- [ ] ensure the CHANGELOG is up-to-date
- [ ] validate on ReadTheDocs
- [ ] wait for a successful build of `main`
- [ ] download the `dist` archive and unpack somewhere (maybe a fresh `dist`)
- [ ] create a new release through the GitHub UI
  - [ ] paste in the relevant CHANGELOG entries
  - [ ] upload the artifacts
- [ ] actually upload to pypi.org
  ```bash
  cd dist
  twine upload *.tar.gz *.whl
  ```
- [ ] postmortem
  - [ ] handle `conda-forge` feedstock tasks
  - [ ] validate on binder via simplest-possible gists
  - [ ] bump to next development version
  - [ ] bump the `CACHE_EPOCH`
  - [ ] rebuild `pixi.lock`
  - [ ] update release procedures with lessons learned
