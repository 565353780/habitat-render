# Learn Habitat

## Install

```bash
sudo apt install libassimp5 libassimp-dev libassimp-doc
conda create -n habitat python=3.8
conda activate habitat
conda install habitat-sim -c conda-forge -c aihabitat
pip install numpy, matplotlib, pyyaml, rospkg
```

## Prepare Scene

```bash
assimp export <PLY FILE> <GLB PATH>
```

## Run

```bash
conda activate habitat
python demo.py
```

## Enjoy it~

