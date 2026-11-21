# Economic Lab

Infinite knowledge vault for **economic theory**.

Quarto essays, Jupyter notebooks, academic papers, model cards, data sources, and research projects. Scale by adding plugins. No hard limit.

Author: Le Tri Nhan  
Visibility: public (essays) / vault for research notes

## Mental model

```
POSTS (Quarto)     NOTEBOOKS     PAPERS        MODELS / DATA
public essays      theory .ipynb academic      cards and packs
```

## Quick start

```bash
make setup
cp docs/env.example .env
make doctor
make list
make preview
```

### Add an essay

```bash
make new-post NAME=solow-swan-extension DOMAIN=growth
# edit posts/<slug>/index.qmd → draft: false
make preview
make render
make publish   # GitHub Pages when ready
```

See [docs/quarto.md](docs/quarto.md).

### Featured essay

| Post | Topic |
| --- | --- |
| [solow-swan-tang-truong](posts/solow-swan-tang-truong/) | Solow–Swan from Harrod–Domar to convergence |

## Layout

```text
posts/       Quarto essays (index.qmd + figures/)
notebooks/   Theory Jupyter
papers/      Academic writing
projects/    Runnable research
data/        Data source manifests
datasets/    Curated packs
models/      Model cards
packages/    el-core, el-lab
_quarto.yml  Quarto website
_site/       Built site (gitignored)
```

## Related vaults

- [Quant Theory Lab](https://github.com/letrinhandn/quant-theory-lab)
- [Investment Research Lab](https://github.com/letrinhandn/investment-research-lab)

## License

MIT. Research and education only. Not investment advice.

> AI agents: read [AGENTS.md](AGENTS.md) first.
