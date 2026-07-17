import csv, sqlite3
from pathlib import Path
ROOT=Path(__file__).parent
DB=ROOT/'airline_operations.db'; CSV=ROOT/'data'/'flight_operations.csv'; SCHEMA=ROOT/'sql'/'schema.sql'

def main():
    if not CSV.exists():
        raise FileNotFoundError('Sample data was not found. Run: python generate_data.py')

    con=sqlite3.connect(DB)
    con.executescript(SCHEMA.read_text())
    with CSV.open(encoding='utf-8') as f:
        rows=[]
        for r in csv.DictReader(f):
            rows.append((int(r['flight_id']),r['flight_date'],r['month'],r['airline'],r['origin_airport'],r['destination_airport'],r['scheduled_departure'],int(r['departure_delay_minutes']),int(r['arrival_delay_minutes']),int(r['cancelled']),r['delay_reason'],int(r['distance_miles'])))
    con.executemany('INSERT INTO flight_operations VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', rows)
    con.commit(); con.close()
    print(f'Loaded {len(rows):,} rows')

if __name__ == '__main__': main()
