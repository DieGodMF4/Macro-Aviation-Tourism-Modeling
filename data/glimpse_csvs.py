import os
import glob
import pandas as pd
from pathlib import Path

def try_read_csv(path: str, nrows: int = 12000):
    """
    Try multiple common CSV formats (Eurostat comma CSV, semicolon CSV, Polish decimal comma).
    Returns (df, meta) or (None, meta) if failed.
    """
    attempts = [
        # Eurostat-style
        dict(sep=",", encoding="utf-8", decimal=".", engine="python"),
        dict(sep=",", encoding="utf-8-sig", decimal=".", engine="python"),
        dict(sep=",", encoding="latin-1", decimal=".", engine="python"),

        # Semicolon + decimal comma (common in PL datasets)
        dict(sep=";", encoding="utf-8", decimal=",", engine="python"),
        dict(sep=";", encoding="utf-8-sig", decimal=",", engine="python"),
        dict(sep=";", encoding="cp1250", decimal=",", engine="python"),
        dict(sep=";", encoding="latin-1", decimal=",", engine="python"),
    ]

    errors = []
    for kwargs in attempts:
        try:
            df = pd.read_csv(path, nrows=nrows, **kwargs)
            meta = {"read_kwargs": kwargs, "error": None}
            return df, meta
        except Exception as e:
            errors.append(f"{kwargs} -> {type(e).__name__}: {e}")
    return None, {"read_kwargs": None, "error": " | ".join(errors[:3]) + (" | ..." if len(errors) > 3 else "")}

def guess_time_col(df: pd.DataFrame):
    candidates = ["TIME_PERIOD", "time", "date", "Date", "DATE", "Period", "period"]
    for c in candidates:
        if c in df.columns:
            return c
    # heuristic: any column containing 'time' or 'date'
    for c in df.columns:
        cl = c.lower()
        if "time" in cl or "date" in cl or "period" in cl:
            return c
    return None

def parse_time_series_bounds(series: pd.Series):
    s = series.dropna().astype(str)
    if s.empty:
        return None, None, None

    # Try monthly YYYY-MM, YYYY-MM-DD
    dt = pd.to_datetime(s, errors="coerce")
    if dt.notna().mean() > 0.7:
        return dt.min(), dt.max(), "datetime"

    # Try Eurostat quarterly like 1995-Q1
    # Convert to quarter start timestamps
    q = s.str.extract(r"^(?P<y>\d{4})-Q(?P<q>[1-4])$")
    if q.notna().all(axis=1).mean() > 0.7:
        y = q["y"].astype(int)
        qq = q["q"].astype(int)
        # map quarter to month
        m = (qq - 1) * 3 + 1
        dtq = pd.to_datetime(y.astype(str) + "-" + m.astype(str).str.zfill(2) + "-01", errors="coerce")
        return dtq.min(), dtq.max(), "quarterly(YYYY-Q#)"

    # Try annual YYYY
    a = s.str.extract(r"^(?P<y>\d{4})$")
    if a["y"].notna().mean() > 0.7:
        ya = a["y"].astype(int)
        return int(ya.min()), int(ya.max()), "annual(YYYY)"

    return None, None, "unknown"

def dataset_card(path: str):
    df, meta = try_read_csv(path)
    print("\n" + "=" * 100)
    print(f"FILE: {path}")
    if df is None:
        print("!! Could not read. First errors:", meta["error"])
        return

    print("-- Read using:", meta["read_kwargs"])
    print(f"Shape (sampled): {df.shape}")

    # Columns and dtypes
    dtypes = df.dtypes.astype(str).to_dict()
    print("\nColumns:")
    for c in df.columns:
        print(f" - {c} ({dtypes.get(c)})")

    # Missingness
    miss = (df.isna().mean() * 100).sort_values(ascending=False)
    print("\nTop missingness (% of sampled rows):")
    print(miss.head(10).round(2).to_string())

    # Key categorical summaries (Eurostat-like)
    for c in ["geo", "unit", "freq", "s_adj", "na_item", "nace_r2", "c_resid"]:
        if c in df.columns:
            vc = df[c].astype(str).value_counts().head(10)
            print(f"\nTop values for '{c}':")
            print(vc.to_string())

    # Time coverage
    tcol = guess_time_col(df)
    if tcol:
        tmin, tmax, kind = parse_time_series_bounds(df[tcol])
        print(f"\nTime column: {tcol} | parsed as: {kind} | range: {tmin} -> {tmax}")
    else:
        print("\nTime column: not detected")

    # Numeric columns quick stats
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if num_cols:
        print("\nNumeric quick stats (sampled):")
        print(df[num_cols].describe().round(3).to_string())

    print("\nHead (first 5 rows):")
    print(df.head(5).to_string(index=False))

def main():
    raw_dir = Path("raw")
    if not raw_dir.exists():
        raw_dir = Path("raw")
    files = sorted(glob.glob(str(raw_dir / "**" / "*.csv"), recursive=True))

    if not files:
        print(f"No CSV files found under: {raw_dir.resolve()}")
        return

    print(f"Found {len(files)} CSV files under {raw_dir.resolve()}")
    for f in files:
        dataset_card(f)

if __name__ == "__main__":
    main()
