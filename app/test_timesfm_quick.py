"""Test TimesFM via pipeline."""
import sys, os, warnings
sys.path.insert(0, r"d:\BCIE\Datos-Abiertos-BCIE\app")
os.chdir(r"d:\BCIE\Datos-Abiertos-BCIE\app")
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import torch
import traceback
from core.config import load_config

config = load_config()
fmt = config["paths"].get("format", "parquet")
silver = config["paths"]["silver"]
df = pd.read_parquet(os.path.join(silver, "aprobaciones_forecasting." + fmt))
df["ds"] = pd.to_datetime(df["ds"])

import timesfm
print("Loading model...")
tfm = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
fc_config = timesfm.ForecastConfig(max_context=512, max_horizon=20)
tfm.compile(fc_config)
print("Loaded on GPU:", torch.cuda.get_device_name(0))

for country in df["Pais"].unique():
    cdata = df[df["Pais"] == country].sort_values("ds")
    if len(cdata) < 3:
        print(f"  {country}: SKIP ({len(cdata)} pts)")
        continue
    try:
        history = cdata["y"].values.astype(np.float64)
        with torch.no_grad():
            pf, q = tfm.forecast(horizon=5, inputs=[history])
        vals = pf[0][:3]
        print(f"  {country}: OK ({len(history)} pts) -> {vals}")
    except Exception as e:
        print(f"  {country}: ERROR - {type(e).__name__}: {e}")
        traceback.print_exc()
