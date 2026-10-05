from dataclasses import dataclass
@dataclass(frozen=True)
class Txn:
    source:str; reference:str; amount_paise:int; timestamp:int
@dataclass(frozen=True)
class Match:
    left:str; right:str; score:float
def normalize(row:dict)->Txn:
    amount=int(row["amount_paise"])
    if amount<0: raise ValueError("negative amount")
    return Txn(str(row["source"]),str(row["reference"]).strip(),amount,int(row["timestamp"]))
def match(left:list[Txn],right:list[Txn],window:int=300):
    candidates=[]
    for a in left:
        best=None
        for b in right:
            if abs(a.timestamp-b.timestamp)>window or a.amount_paise!=b.amount_paise: continue
            score=1.0 if a.reference and a.reference==b.reference else 0.5
            if best is None or score>best[2]: best=(a,b,score)
        if best: candidates.append(best)
    used=set(); out=[]
    for a,b,score in sorted(candidates,key=lambda x:x[2],reverse=True):
        if b.reference in used: continue
        used.add(b.reference); out.append(Match(a.reference,b.reference,score))
    return out
def recovery_allowed(reason:str,amount_paise:int)->bool:
    return reason=="amount_mismatch" and 10_000<=amount_paise<=1_000_000
