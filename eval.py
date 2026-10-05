from src.recoup.core import normalize,match
def run():
    a=[normalize({"source":"bank","reference":"A1","amount_paise":50000,"timestamp":100})]
    b=[normalize({"source":"ledger","reference":"A1","amount_paise":50000,"timestamp":110})]
    m=match(a,b); return {"transactions":2,"matches":len(m),"precision":1.0 if m else 0.0}
if __name__=="__main__": print(run())
