
from scipy.integrate import odeint as ode
import numpy as np

def wymiennik(y,t,params):
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
    value=params[10]
    dTpm=1/(Mm*Cw)*(value*Fzm*cw*ro*(Tzm-Tpm)-kw*(Tpm-Tzco))
    dTzco=1/(Mco*Cw)*(-Fzco*cw*ro*(Tzco-Tpco)+kw*(Tpm-Tzco))
    return [dTzco,dTpm]

def budynek(y,t,params):
    Tpco,Tr = y
    mh=3000
    ch=2700
    Fcob=0.01
    kh=12000
    ro=1000
    cw=4200
    mb=20000
    cb=1000
    ke=15000
    Tzco=params
    dTpco=1/(mh*ch)*(Fcob*ro*cw*(Tzco-Tpco)-kh*(Tpco-Tr))
    dTr=1/(mb*cb)*(kh*(Tpco-Tr)-ke*(Tr-5))
    return [dTpco,dTr]

def wymiennikz(y,t,params):
    Tzco,Tpm,Tpco,Tr = y
    mh=3000
    ch=2700
    Fcob=11
    kh=12000
    ke=15000
    cb=1000
    mb=20000
    Mm=params[0]
    Mco=params[1]
    Cw=params[2]
    ro=params[3]
    cw=params[4]
    kw=params[5]
    Fzco=params[6]
    Fzm=params[7]
    Tzm=params[8]
    value=params[10]
    dTpm=(1/(Mm*Cw))*(value*Fzm*cw*ro*(Tzm-Tpm)-kw*(Tpm-Tzco))
    dTzco=(1/(Mco*Cw))*(-Fzco*cw*ro*(Tzco-Tpco)+kw*(Tpm-Tzco))
    dTpco=(1/(mh*ch))*(Fcob*ro*cw*(Tzco-Tpco)-kh*(Tpco-Tr))
    dTr=(1/(mb*cb))*(kh*(Tpco-Tr)-ke*(Tr-8))
    return [dTzco,dTpm,dTpco,dTr]

def sim(y0,value,Tzm,Tpco,time):
    #params Mm Mco Cw ro cw kw Fzco Fzm Tzm Tpco value
    y0=np.array(y0)
    params=[3000,3000,2700,1000,4200,250000,23,42,Tzm,Tpco,value]
    t=np.arange(0., 1, 0.1)
    s=ode(wymiennik, y0, t,args=(params,))
    w=(s[-1]-y0)*time+y0
    return w

def sim2(y0,value,Tzm,Tpco,Tr,time):
    #params Mm Mco Cw ro cw kw Fzco Fzm Tzm Tpco value
    y0=[y0[0],y0[1],Tpco,Tr]
    y0=np.array(y0)
    params=[3000,3000,2700,1000,4200,250000,0.023,0.042,Tzm,Tpco,value]
    t=np.arange(0., time, 0.1)
    s=ode(wymiennikz, y0, t,args=(params,))
    return s[-1]

def simtest(y0,Tzco):
    t=np.arange(0., 1, 0.1)
    s=ode(budynek, y0, t,args=(Tzco,))
    return s[-1]