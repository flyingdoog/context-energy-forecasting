"""Draw manuscript displays from saved errors. No model imports, fits or inference."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT/'results'
FIG = ROOT/'paper/figures'
GEN = ROOT/'paper/generated'
MODELS = ['Ridge','LightGBM','N-HiTS']
CONDITIONS = ['power','power_state','full']

def device_table():
    data = pd.read_csv(RESULTS/'device_average.csv')
    cu = pd.read_json(RESULTS/'cu_common_scores.json')
    cu = cu[(cu.cohort=='thermal_five_floors') & (cu.scale=='device') &
            (cu.span_minutes==0) & cu.metric.isin(['mse','mae'])]
    context = [('BPA','Field study','spring','BPA','Spring'),
        ('BPA','Field study','summer','BPA','Summer'),
        ('ACN','Caltech','autumn','Caltech','Autumn'),
        ('ACN','Caltech','winter','Caltech','Winter'),
        ('ACN','Office','autumn','Office','Autumn'),
        ('ACN','Office','winter','Office','Winter'),
        ('EPFL','Fast charging','later','EPFL','Later'),
        ('CU-BEMS','','later_1','CU-BEMS','Sep.--Oct.'),
        ('CU-BEMS','','later_2','CU-BEMS','Nov.--Dec.')]
    out = [r'\begin{table*}[t]',
        r'\caption{Device forecasting with different information conditions. MSE (kW$^2$) and MAE (kW) average the three native spans with equal date weights. CU-BEMS additionally weights its five common floors equally; its state and all-telemetry columns are the same thermal arm. Neural errors average three seeds. Bold marks the lowest error across information conditions within each model and row, including ties at displayed precision.}',
        r'\label{tab:device}',r'\centering\small',r'\setlength{\tabcolsep}{6pt}',
        r'\begin{tabular}{@{}llrrrrrr@{}}',r'\toprule',
        r'\multirow{2}{*}{Source / period} & \multirow{2}{*}{Model} & \multicolumn{2}{c}{History} & \multicolumn{2}{c}{History + state} & \multicolumn{2}{c}{All telemetry}\\',
        r'\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(l){7-8}',
        r'& & MSE & MAE & MSE & MAE & MSE & MAE\\',r'\midrule']
    records = []
    for source, site, period, label, display_period in context:
        for m, model in enumerate(MODELS):
            values=[]
            for condition in CONDITIONS:
                if source=='CU-BEMS':
                    cm = ('Tree' if model=='LightGBM' else model)+': '+('power' if condition=='power' else 'thermal')
                    p=cu[(cu.split==period)&(cu.method==cm)].set_index('metric').value
                    pair=[p['mse'],p['mae']]
                else:
                    p=data[(data.source==source)&(data.site==site)&(data.period==period)&
                        (data.model==model)&(data.condition==condition)]
                    if len(p)!=1: raise ValueError((source,site,period,model,condition))
                    pair=[p.iloc[0].mse,p.iloc[0].mae]
                values.append(pair)
                records.append(dict(source=source,site=site,period=period,model=model,
                    condition=condition,mse=float(pair[0]),mae=float(pair[1])))
            v=np.round(values,3); best=v.min(axis=0)
            first=r'\multirow{3}{*}{\shortstack[l]{'+label+r'\\'+display_period+'}}' if m==0 else ''
            cells=[first,model]
            for pair in v:
                for j,value in enumerate(pair):
                    s=f'{value:.3f}'
                    cells.append(r'\textbf{'+s+'}' if value==best[j] else s)
            out.append(' & '.join(cells)+r' \\')
        if source!='CU-BEMS' or period!='later_2': out.append(r'\addlinespace[2pt]')
    out += [r'\bottomrule',r'\end{tabular}',r'\end{table*}']
    (GEN/'device_table.tex').write_text('\n'.join(out)+'\n')
    (RESULTS/'paper_device_cells.json').write_text(json.dumps(records,indent=2)+'\n')

def declaration_table():
    blocks=[]
    for filename,model,arms in [('declarations_tree.csv','LightGBM',['telemetry','declared']),
            ('declarations_nhits.csv','N-HiTS',['padded','raw'])]:
        d=pd.read_csv(RESULTS/filename)
        d=d[(d.site=='caltech')&(d.scale=='cohort_mean')&d.split.isin(['autumn','winter'])&d.method.isin(arms)]
        avg=d.groupby(['split','method'])[['mse','mae']].mean()
        for period in ['autumn','winter']:
            a,b=avg.loc[(period,arms[0])],avg.loc[(period,arms[1])]
            blocks.append(dict(model=model,period=period,telemetry_mse=a.mse,
                telemetry_mae=a.mae,declared_mse=b.mse,declared_mae=b.mae,
                mse_reduction_pct=100*(a.mse-b.mse)/a.mse))
    out=[r'\begin{table}[t]',
        r'\caption{Caltech group-mean forecasting with query-time demand declarations. MSE / MAE in kW$^2$ / kW; equal-span averages. The neural control has the same input width as the declaration arm.}',
        r'\label{tab:declarations}',r'\centering\small',r'\setlength{\tabcolsep}{3pt}',
        r'\begin{tabular}{@{}llll@{}}',r'\toprule',
        r'Model & Period & Telemetry & + declarations\\',
        r'& & MSE / MAE & MSE / MAE\\',r'\midrule']
    for i,r in enumerate(blocks):
        label=(r'\multirow{2}{*}{'+r['model']+'}') if i%2==0 else ''
        out.append(f"{label} & {r['period'].capitalize()} & {r['telemetry_mse']:.3f} / {r['telemetry_mae']:.3f} & {r['declared_mse']:.3f} / {r['declared_mae']:.3f}"+r' \\')
        if i==1:out.append(r'\addlinespace[2pt]')
    out += [r'\bottomrule',r'\end{tabular}',r'\end{table}']
    (GEN/'declaration_table.tex').write_text('\n'.join(out)+'\n')
    (RESULTS/'paper_declaration_cells.json').write_text(json.dumps(blocks,indent=2)+'\n')

def task_figure():
    fig,ax=plt.subplots(figsize=(3.5,2.0))
    ax.set(xlim=(0,10),ylim=(0,5.6)); ax.axis('off')
    def box(x,y,w,h,s,color='#edf3f7'):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.04,rounding_size=.10',
            facecolor=color,edgecolor='#3b626f',linewidth=.7))
        ax.text(x+w/2,y+h/2,s,ha='center',va='center',fontsize=8.2,linespacing=1.3)
    def arrow(a,b):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=8,lw=.8,color='#3b626f'))
    box(.15,3.8,4.1,1.25,'Power history\n+ calendar')
    box(5.65,3.8,4.1,1.25,'State / control / requests\n+ observation masks')
    box(2.9,1.85,4.2,1.05,'Device-level predictor','#f7efe4')
    box(.15,.05,4.1,1.0,'Device power\ntrajectories')
    box(5.65,.05,4.1,1.0,'Same-group\ntotal power')
    arrow((2.2,3.75),(4.15,2.95));arrow((7.7,3.75),(5.85,2.95))
    arrow((4.1,1.8),(2.5,1.1));arrow((5.9,1.8),(7.5,1.1))
    fig.subplots_adjust(left=0,right=1,bottom=.03,top=1)
    fig.savefig(FIG/'task.pdf',bbox_inches='tight',pad_inches=.01);plt.close(fig)

def reassignment_figure():
    d=pd.read_json(RESULTS/'reassignment_effects.json')
    d=d[(d.scale=='group_total')&(d.span_minutes==0)&(d.metric=='mse')]
    entries=[('Field study','spring','BPA spring'),('Caltech','autumn','Caltech autumn'),
        ('Office','autumn','Office autumn'),('Field study','summer','BPA summer'),
        ('Caltech','winter','Caltech winter'),('Office','winter','Office winter')]
    colors=['#909da5','#246a8b','#ca8746','#5b9c8e']
    fig,axes=plt.subplots(2,3,figsize=(7.1,3.2))
    for ax,(site,period,title) in zip(axes.flat,entries):
        r=d[(d.site==site)&(d.period==period)].iloc[0]
        vals=[r[k] for k in ['power_error','paired_error','frozen_error','retrained_error']]
        ax.bar(range(4),vals,width=.72,color=colors)
        for i,v in enumerate(vals):ax.text(i,v,f'{v:.2f}',ha='center',va='bottom',fontsize=8)
        ax.set_title(title,fontsize=9);ax.set_xticks([]);ax.set_ylabel('MSE (kW$^2$)',fontsize=8)
        ax.set_ylim(0,max(vals)*1.27);ax.tick_params(labelsize=8)
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.16)
    handles=[plt.Rectangle((0,0),1,1,color=c) for c in colors]
    fig.legend(handles,['History only','Paired records','Fixed-model reassignment','Retrained reassignment'],
        loc='lower center',ncol=2,frameon=False,fontsize=8.5)
    fig.tight_layout(rect=[0,.11,1,1],h_pad=.65,w_pad=1)
    fig.savefig(FIG/'reassignment.pdf',bbox_inches='tight',pad_inches=.025);plt.close(fig)

def main():
    FIG.mkdir(parents=True,exist_ok=True);GEN.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42})
    device_table();declaration_table();task_figure();reassignment_figure()
    print('Saved-score tables and figures generated; no training, inference or new experiments.')

if __name__=='__main__':main()
