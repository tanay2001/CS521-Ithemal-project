# BHive: A Benchmark Suite and Measurement Framework for Validating x86-64 Basic Block Performance Models

More information about our tool/benchmark can be found in this paper.
* **BHive: A Benchmark Suite and Measurement Framework for Validating x86-64 Basic Block Performance Models**</br>
  Yishen Chen, Ajay Brahmakshatriya, Charith Mendis, Alex Renda, Eric Atkinson, Ondrej Sykora, Saman Amarasinghe, and Michael Carbin</br>
  2019 IEEE International Symposium on Workload Characterization</br>
  
```
@inproceedings{bhive,
  title={BHive: A Benchmark Suite and Measurement Framework for Validating x86-64 Basic Block Performance Models},
  author={Chen, Yishen and Brahmakshatriya, Ajay and Mendis,  Charith and Renda, Alex and Atkinson, Eric and Sykora, Ondrej and Amarasinghe, Saman and Carbin, Michael},
  booktitle={2019 IEEE international symposium on workload characterization (IISWC)},
  year={2019},
  organization={IEEE}
}
```


What's here?

Download the benchmark folder from here - https://github.com/ithemal/bhive and place it inside the bhive folder

# Benchmark
* `benchmark/categories.csv` lists all the basic blocks and their categories.
* `benchmark/throughput/` contains the measured throughput of basic blocks. The throughput of some basic blocks are missing because we can't get a clean measurement.
* `benchmark/sources/` lists the source applications of all the basic blocks. For each basic block, we additionally show the (static) frequency with which it shows up in an application.
* `benchmark/disasm` is a tool that disassembles hex representation of a basic block. Use it like this `./disasm 85c044897c2460`. It uses `llvm-mc` and assumes that you have `llvm` installed.

# Basic Block Profiler
`timing-harness/` is a profiler that allows you to profile arbitrary, memory accessing basic blocks such as those in `sources/`.

# Throughput Calculation
* The unit of the throughput numbers in the directory `benchmark/throughput*` is cycles per hundred-iterations. 
* The profiler in `timing-harness` only produces an unrolled basic block's latency---including measurement overhead.
To get the final throughput, numbers in `benchmark/throughput*` is calculated as `(L_a-L_b)/(a-b)`,
where `a` and `b` are two integer unroll factors (`a > b`) and `L_a`, `L_b` are the the latency of the basic block unrolled `a` and `b` times respectively.
* Measurements from the profiler can have noise.
The published paper uses the minimum of the measured latencies as the final latency of an unrolled basic block,
and the numbers in the master branch are produced using the same methodology.
* The profiler sometimes produces small, spurious latency. Using the median is more stable in this case, and the throughputs are retabulated in a separate [branch](https://github.com/ithemal/bhive/tree/fix).

# Page Aliasing
Our profiling methodology relies on mapping potentially large number of
virtual pages to a small set of physical pages.
This is problematic when two memory accesses access different virtual
addresses alised to the same physical ones, creating spurious memory dependence
and slow down the basic block unnecessarily.
We haven't been able to use hardware counters to detect page aliasing reliably,
so we tracked the trace of loads and stores occured during profiling
and conservatively mark basic blocks that *could* have been affected.
These basic blocks are listed in `benchmark/may-alias.csv`.

# Data Generation for Ithemal

To train and evaluate Ithemal on the BHive dataset, you first need to convert the raw CSVs and disassembled blocks into a PyTorch‐ready format.

### Environment Setup

Make sure you have Conda installed. Then create and activate the environment specified in `environment.yml`:

```
conda env create -f environment.yml
conda activate .env
```

### Generating the Dataset

From the repository root, run one of the following in the `bhive` directory:

```
cd bhive
python ./make_data.py
# or for much faster execution (multi-threaded disassembly & tokenization):
python ./make_data_parallel.py
```

* **Inputs**

  * `benchmark/throughput/<arch>.csv`
    – measured throughput (cycles per 100 iterations) for each architecture (`hsw`, `skl`, `ivb`)
  * `benchmark/disasm`
    – disassembler binary (requires `llvm-mc`)
  * `Ithemal/data_collection/build/bin/tokenizer`
    – instruction tokenizer

* **Outputs**

  * `bhive_ithemal_dataset.pt`
    – final dataset for training/testing: a serialized list of `(code_id, timing, intel_syntax, code_xml)` tuples
  * `bhive_ithemal_dataset_<N>.pt`
    – intermediate snapshots every 30k blocks

* **Performance Note**
  The parallel script uses Python’s `ThreadPoolExecutor` to disassemble and tokenize multiple blocks concurrently, typically reducing end-to-end runtime by 3–5x compared to the single-threaded version.
