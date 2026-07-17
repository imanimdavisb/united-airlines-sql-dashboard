import csv, random
from datetime import date, timedelta
from pathlib import Path

OUTPUT = Path(__file__).parent / 'data' / 'flight_operations.csv'
random.seed(42)
AIRLINES = {'United Airlines':1.00,'American Airlines':1.08,'Delta Air Lines':0.90,'Southwest Airlines':1.12,'JetBlue Airways':1.20}
AIRPORTS = {'ORD':1.28,'EWR':1.35,'DEN':1.05,'IAH':1.02,'SFO':1.22,'LAX':1.15,'ATL':0.92,'DFW':1.08,'JFK':1.30,'SEA':1.00,'BOS':1.12,'MCO':1.18,'LAS':1.10,'PHX':0.95,'CLT':0.98}

def delay_reason(delay, cancelled):
    if cancelled:
        return random.choices(['Weather','Air Carrier','National Airspace System','Security'],[45,30,22,3])[0]
    if delay <= 15:
        return 'No Significant Delay'
    return random.choices(['Weather','Air Carrier','Late Aircraft','National Airspace System','Security'],[26,25,29,18,2])[0]

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows=[]; current=date(2026,1,1); end=date(2026,12,31); fid=1; codes=list(AIRPORTS)
    while current <= end:
        seasonal = 1.18 if current.month in {6,7,8,11,12} else (1.10 if current.month in {1,2} else 1.0)
        for _ in range(random.randint(35,55)):
            airline=random.choice(list(AIRLINES)); origin=random.choice(codes); destination=random.choice([a for a in codes if a!=origin])
            delay=int(max(-12, random.gauss(8,18)*AIRLINES[airline]*AIRPORTS[origin]*seasonal))
            if random.random()<0.09: delay += random.randint(35,140)
            cancel_prob=.010+(.008 if current.month in {1,2,7,12} else 0)+(.006 if origin in {'ORD','EWR','JFK','SFO'} else 0)
            cancelled=1 if random.random()<cancel_prob else 0
            dep=arr=0 if cancelled else delay
            if not cancelled: arr=max(-15, delay+random.randint(-8,14))
            hour=random.randint(5,22); minute=random.choice([0,10,15,20,30,40,45,50])
            rows.append({'flight_id':fid,'flight_date':current.isoformat(),'month':current.strftime('%Y-%m'),'airline':airline,'origin_airport':origin,'destination_airport':destination,'scheduled_departure':f'{hour:02d}:{minute:02d}','departure_delay_minutes':dep,'arrival_delay_minutes':arr,'cancelled':cancelled,'delay_reason':delay_reason(arr,cancelled),'distance_miles':random.randint(250,2700)})
            fid += 1
        current += timedelta(days=1)
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f, fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)
    print(f'Created {len(rows):,} records')

if __name__ == '__main__': main()
