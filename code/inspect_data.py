"""Open supplied packets, report split support, and read one input/target. No fits."""
from pathlib import Path
import json
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from field_control import OperationalForecastTask

ROOT=Path(__file__).resolve().parents[1]

def main():
    specs=[('bpa','BPA',dict(season=s)) for s in ['winter','spring','summer']]
    specs += [('acn','ACN',dict(site=s)) for s in ['caltech','office001']]
    specs += [('epfl','EPFL',{})]
    specs += [(f'cu_bems/floor{f}','CU-BEMS',dict(site=f'floor{f}')) for f in range(1,8)]
    rows=[]
    for relative,source,kw in specs:
        task=OperationalForecastTask(ROOT/'data'/relative,source,**kw)
        condition='power' if kw.get('site')=='floor1' else 'full'
        task.inputs([0],condition=condition)
        target=task.targets([0])
        row=dict(source=source,**kw,cases=len(task),
            splits={str(k):int(v) for k,v in task.meta.split.value_counts().items()},
            target_bins=int(target.shape[1]))
        rows.append(row);print(json.dumps(row),flush=True)
        base=task.base
        if hasattr(base,'close'):base.close()
        del task
    print(json.dumps(dict(checked=len(rows),model_fits=0,new_forecasts=0)))

if __name__=='__main__':main()
