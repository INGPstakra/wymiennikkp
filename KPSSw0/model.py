
from scipy.integrate import odeint as ode
import numpy as np

def wymiennik(t,y,params):
    Tzco,Tpm = y
    Mm=params[0]
    Mco=params[1]
    Cw=params[2]
    ro=params[3]
    cw=params[4]
    kw=params[5]
    Fzco=params[6]
    Fzm=params[7]
    Tzm=params[8]
    Tpco=params[9]
    dTpm=1/(Mm*Cw)*(Fzm*cw*ro*(Tzm-Tpm)-kw*(Tpm-Tzco))
    dTzco=1/(Mco*Cw)*(-Fzco*cw*ro*(Tzco-Tpco)+kw*(Tpm-Tzco))
    return [dTpm,dTzco]

param=[3000,3000,2700,1000,4200,250000,150000,80000,100,20]
t=np.arange(0., 1, 0.01)
ode(wymiennik, [0.,0.], t,args=(param,))