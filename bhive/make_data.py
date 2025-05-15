
#!/usr/bin/env python3
import os
import csv
import subprocess
import torch
from tqdm import tqdm

# --- Configuration ---
BHIVE_ROOT   = "./bhive"
THP_FILE     = os.path.join(BHIVE_ROOT, "benchmark/throughput/hsw.csv")
DISASM_BIN   = os.path.join(BHIVE_ROOT, "benchmark/disasm")
# TOKENIZER    = "./Ithemal/data_collection/tokenizer/tokenizer"
TOKENIZER    = "./Ithemal/data_collection/build/bin/tokenizer"
OUTPUT_PT    = os.path.join(BHIVE_ROOT, "bhive_ithemal_dataset.pt")

dataset = []

with open(THP_FILE, newline='') as f:
    reader = list(csv.reader(f))
    for idx, (hex_code, throughput_str) in tqdm(enumerate(reader), total=len(reader), desc="Processing", unit="inst"):
        timing = float(throughput_str)

        # print(hex_code, throughput_str)

        # Disassemble for human-readable Intel syntax
        # intel = subprocess.check_output(
        #     [DISASM_BIN, hex_code],
        #     text=True
        # ).strip()
        # print(intel)
        
        proc = subprocess.run(
            [TOKENIZER, hex_code, "--intel"],
            capture_output=True, text=True, check=True
        )
        intel = proc.stdout.strip()
        # print(intel)

        # Tokenize to Ithemal's XML format
        proc = subprocess.run(
            [TOKENIZER, hex_code, "--token"],
            capture_output=True, text=True, check=True
        )
        code_xml = proc.stdout.strip()
        # print(code_xml)

        code_id = hex_code
        
        # check that timing and code_xml are not empty
        if not timing or not code_xml:
            print(f"Error: empty timing or code_xml for {code_id}")
            continue

        dataset.append((code_id, timing, intel, code_xml))

        # save after every 50k records 
        if idx % 30000 == 0 and idx > 0:
            save_name = OUTPUT_PT.replace(".pt", f"_{idx}.pt")
            torch.save(dataset, save_name)
            print(f"Saved {len(dataset)} records to {save_name}")



# Serialize for Ithemal's run_ithemal.py
torch.save(dataset, OUTPUT_PT)
print(f"Saved {len(dataset)} records to {OUTPUT_PT}")
