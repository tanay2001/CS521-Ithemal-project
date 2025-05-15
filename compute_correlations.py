import pandas as pd
from scipy.stats import spearmanr, pearsonr, kendalltau
import numpy as np

def compute_correlations_and_error(file_path):
    # Read the file, skipping the last two lines
    data = pd.read_csv(file_path, header=None, names=["X", "Y"], skipfooter=2, engine='python')
    # Compute Spearman correlation
    spearman_corr, spearman_p = spearmanr(data["X"], data["Y"])

    # Compute Pearson correlation
    pearson_corr, pearson_p = pearsonr(data["X"], data["Y"])

    # Compute Kendall's tau correlation
    kendall_corr, kendall_p = kendalltau(data["X"], data["Y"])

    # Compute average absolute error (MAE)
    mae = np.mean(np.abs(data["X"] - data["Y"])/data["Y"])

    print(f"Spearman Correlation: {spearman_corr:.4f} (p={spearman_p:.4g})")
    print(f"Pearson Correlation:  {pearson_corr:.4f} (p={pearson_p:.4g})")
    print(f"Kendall's Tau:       {kendall_corr:.4f} (p={kendall_p:.4g})")
    print(f"Average Absolute Error (MAE): {mae:.4f}")

# ablations study
print('HSW RNN')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/hsw/1/validation_results.txt")
print('HSW LSTM')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/hsw/lstm_2/validation_results.txt")
print('HSW LSTM with Dense')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/hsw/lstm_model_with_dense/validation_results.txt")
print('HSW LSTM with Linear')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/hsw/lstm_linear/validation_results.txt")
print('HSW LSTM with 512')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/hsw/lstm_embed_512/validation_results.txt")


# final Table 1 results
print('HSW LSTM')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/hsw/lstm_2/validation_results.txt")

print('SKL LSTM')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/skl/lstm_2/validation_results.txt")

print('IVB LSTM')
compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/ivb/lstm_2/validation_results.txt")


# addiitonal results
# print('IVB RNN')
# compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/ivb/1/validation_results.txt")
# print('IVB RNN upsampled')
# compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/ivb/upsampled_rnn/validation_results.txt")
# print('IVB LSTM upsampled')
# compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/ivb/upsampled_lstm/validation_results.txt")
# print('IVB LSTM upsampled 512 ')
# compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/ivb/upsampled_lstm_hidden512_embed512/validation_results.txt")
# print('SKL RNN')
# compute_correlations_and_error("/shared/data/tanayd2/CS521/Ithemal/learning/pytorch/saved/skl/1/validation_results.txt")