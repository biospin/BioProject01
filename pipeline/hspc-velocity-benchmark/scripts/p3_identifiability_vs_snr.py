import pandas as pd, numpy as np
from scipy import stats
R="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark/results/"
ident=pd.read_csv(R+"profile_likelihood_identifiability.csv")
mv=pd.read_csv(R+"multivelo_genes.csv"); mf=pd.read_csv(R+"moflow_genes.csv"); vae=pd.read_csv(R+"multivelovae_genes.csv")
mv["mv_lag"]=mv["fit_t_sw2"]-mv["fit_t_sw1"]; mv=mv[["gene","mv_lag","fit_alpha"]].rename(columns={"fit_alpha":"mv_alpha"})
mf=mf[["gene","cs_lag_median"]].rename(columns={"cs_lag_median":"mf_lag"}); vae=vae[["gene","vae_alpha"]]
d=ident.merge(mv,on="gene").merge(mf,on="gene").merge(vae,on="gene")
print(f"[N] 4-method 공통: {len(d)}",flush=True)
for c in ["mv_lag","mf_lag","mv_alpha","vae_alpha"]: d[c+"_r"]=d[c].rank(pct=True)
d["lag_disagree"]=(d["mv_lag_r"]-d["mf_lag_r"]).abs()
d["alpha_disagree"]=(d["mv_alpha_r"]-d["vae_alpha_r"]).abs()
print(f"[재현] lag불일치 med={d.lag_disagree.median():.3f} alpha불일치 med={d.alpha_disagree.median():.3f}",flush=True)
for cur in ["kappa_lag","kappa_alpha","ratio"]:
    m=d[[cur,"lag_disagree"]].replace([np.inf,-np.inf],np.nan).dropna()
    print(f"  rho({cur},lag_disagree)={stats.spearmanr(m[cur],m.lag_disagree)[0]:+.3f} p={stats.spearmanr(m[cur],m.lag_disagree)[1]:.1e}",flush=True)
m=d[["kappa_lag","lag_disagree","nkeep"]].replace([np.inf,-np.inf],np.nan).dropna()
def partial(x,y,z,df):
    rxy=stats.spearmanr(df[x],df[y])[0]; rxz=stats.spearmanr(df[x],df[z])[0]; ryz=stats.spearmanr(df[y],df[z])[0]
    return (rxy-rxz*ryz)/np.sqrt((1-rxz**2)*(1-ryz**2))
print("[SNR분리]",flush=True)
print(f"  단순 rho(kappa_lag,disagree)={stats.spearmanr(m.kappa_lag,m.lag_disagree)[0]:+.3f}",flush=True)
print(f"  nkeep통제 편상관={partial('kappa_lag','lag_disagree','nkeep',m):+.3f}",flush=True)
print(f"  rho(nkeep,disagree)={stats.spearmanr(m.nkeep,m.lag_disagree)[0]:+.3f}  rho(kappa_lag,nkeep)={stats.spearmanr(m.kappa_lag,m.nkeep)[0]:+.3f}",flush=True)
print("DONE",flush=True)
