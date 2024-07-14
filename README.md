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

## Screenshots

| note                                                                |           screenshot            |
| ------------------------------------------------------------------- | :-----------------------------: |
| viewing `pyinstrument` profile data with `speedscope` and `mermaid` | [![screenshot-1]][screenshot-1] |

[screenshot-1]:
  https://private-user-images.githubusercontent.com/45380/348560542-ea0f7649-e35e-482b-971b-80d54ec2678d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjA5Nzg2MTcsIm5iZiI6MTcyMDk3ODMxNywicGF0aCI6Ii80NTM4MC8zNDg1NjA1NDItZWEwZjc2NDktZTM1ZS00ODJiLTk3MWItODBkNTRlYzI2NzhkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA3MTQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNzE0VDE3MzE1N1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWY5YTI5MTY1ODdkMDk2ODVhYzc1ZTQ5ZDNmYjAzZmI5ZjlmMzE2YmMyYTE2NDQ2NGM4YmQzMjY5YTg5NGEzYWYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.28eNu41jxBbyNIJB-KxQHFqBJJGa2MLOXbdNkjI1V00
