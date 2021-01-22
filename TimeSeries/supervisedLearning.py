import pandas as pd
import numpy as np
import forecasting

def transform_series(series,n_input_steps,n_output_steps, df):
    for k in range(n_input_steps):
        df["X" + str(k)] = ""
    for j in range(n_output_steps):
        df["y" + str(j)] = ""
    for i in range(len(series)):
        sample_size = i + n_input_steps
        output_size = sample_size + n_output_steps
        if (output_size > len(series)-1):
            return df
        else:
            features, target = series.values[i:sample_size], series.values[sample_size:output_size]
            matrix = np.concatenate([features, target])
            matrix = matrix.reshape(-1)
            df.loc[i] = matrix
    return df
