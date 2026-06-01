from datetime import datetime

def csv_bytes(df):
    return df.to_csv(index=False).encode('utf-8')

def timestamped_filename(prefix):
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
