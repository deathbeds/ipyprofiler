# `ipyprofiler`

> Jupyter Widgets for visualizing profiler data.

## Features

| feature                              | featuring                      |
| ------------------------------------ | ------------------------------ |
| view interactive flamge graphs       | [`speedscope`][speedscope]     |
| view call graphs (JupyterLab >=4.1+) | [`mermaid`][mermaid]           |
| customizable python profiling        | [`pyinstrument`][pyinstrument] |

[speedscope]: https://github.com/jlfwong/speedscope
[pyinstrument]: https://github.com/joerick/pyinstrument
[mermaid]: https://github.com/mermaid-js/mermaid

## Screenshots

| note                                                                |    screenshot     |
| ------------------------------------------------------------------- | :---------------: |
| viewing `pyinstrument` profile data with `speedscope` and `mermaid` | [![img01]][img01] |

[img01]: https://github.com/user-attachments/assets/ea0f7649-e35e-482b-971b-80d54ec2678d

## Install

### From PyPI

> **This package is not yet released.**
>
> ```bash
> pip install ipyprofiler
> ```
>
> To also install optional python-specific integration:
>
> ```bash
> pip install ipyprofiler[pyinstrument]
> ```
