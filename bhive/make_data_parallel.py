
####### parallel version #######
#!/usr/bin/env python3
import os
import csv
import subprocess
import torch
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Configuration ---
BHIVE_ROOT   = "./bhive"
THP_FILE     = os.path.join(BHIVE_ROOT, "benchmark/throughput/skl.csv")
DISASM_BIN   = os.path.join(BHIVE_ROOT, "benchmark/disasm")
# TOKENIZER    = "./Ithemal/data_collection/tokenizer/tokenizer"
TOKENIZER    = "./Ithemal/data_collection/build/bin/tokenizer"
OUTPUT_ROOT = os.path.join(BHIVE_ROOT, THP_FILE.split("/")[-1].split(".")[0])
os.makedirs(OUTPUT_ROOT, exist_ok=True)
OUTPUT_PT    = os.path.join(OUTPUT_ROOT, "bhive_ithemal_dataset.pt")

def process_row(row):
    hex_code, throughput_str = row
    timing = float(throughput_str)
    try:
        proc_intel = subprocess.run(
            [TOKENIZER, hex_code, "--intel"],
            capture_output=True, text=True, check=True
        )
        intel = proc_intel.stdout.strip()
        proc_xml = subprocess.run(
            [TOKENIZER, hex_code, "--token"],
            capture_output=True, text=True, check=True
        )
        code_xml = proc_xml.stdout.strip()
        code_id = hex_code
        return (code_id, timing, intel, code_xml)
    except Exception as e:
        print(f"Error processing {hex_code}: {e}")
        return None

dataset = []
with open(THP_FILE, newline='') as f:
    reader = list(csv.reader(f))
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_row, row) for row in reader]
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Processing", unit="inst"):
            result = fut.result()
            if result is not None:
                dataset.append(result)
            # print after every 10k records
            if len(dataset) % 10000 == 0:
                print(f"Processed {len(dataset)} records")
            # save after every 30k records
            if len(dataset) % 30000 == 0:
                save_name = OUTPUT_PT.replace(".pt", f"_{len(dataset)}.pt")
                torch.save(dataset, save_name)
                print(f"Saved {len(dataset)} records to {save_name}")

torch.save(dataset, OUTPUT_PT)
print(f"Saved {len(dataset)} records to {OUTPUT_PT}")
