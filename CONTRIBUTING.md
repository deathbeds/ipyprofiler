# Contributing

## Local Development

### Set up

This project is developed locally and in CI with [pixi], a relatively new approach to
`conda` package management and task running.

> ** Note **
>
> Refer to `pixi.toml#/$schema` for the current development version

[pixi]: https://pixi.sh/latest/#installation

If using `mamba` or `conda` (or some other `$CONDA_EXE`):

```bash
# replace `mamba` with your CONDA_EXE
mamba install -c conda-forge pixi==0.24.2
```

<details><summary><i>Why <code>pixi</code>?</i></summary>

`pixi` provides the necessary primitives to:

- capture complex environments, with python and other runtimes
- install environments quickly, and cache well, but only when needed
- run tasks, in the right environment, in the right order
- skip tasks that have already run, and dependencies have not changed

</details>

<br />

### Tasks and Environments

See all the project info:

```bash
pixi info
```

See just the available top-level `pixi` tasks:

```bash
pixi task list
```
