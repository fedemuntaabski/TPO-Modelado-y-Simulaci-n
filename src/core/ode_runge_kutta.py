from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional
import numpy as np, time

@dataclass
class ODEResult:
    t: np.ndarray
    y: np.ndarray
    method: str
    step: float
    steps_taken: int
    computation_time: float
    max_error_estimate: Optional[float] = None
    rejected_steps: int = 0
    message: str = ""

class RungeKuttaSolver:
    SUPPORTED = ("euler","heun","rk2","rk4","rk45")
    def __init__(self, method="rk4", step: Optional[float]=0.1, tol: float=1e-6, h_min: float=1e-6, h_max: Optional[float]=None, max_steps: int=1_000_000):
        if method.lower() not in self.SUPPORTED: raise ValueError("Método no soportado")
        self.method=method.lower(); self.step=step; self.tol=tol; self.h_min=h_min; self.h_max=h_max; self.max_steps=max_steps

    def _euler_step(self,f,t,y,h): return y + h*f(t,y)
    def _heun_step(self,f,t,y,h):
        k1=f(t,y); k2=f(t+h, y+h*k1); return y + (h/2.0)*(k1+k2)
    def _rk2_midpoint_step(self,f,t,y,h):
        k1=f(t,y); k2=f(t+0.5*h, y+0.5*h*k1); return y + h*k2
    def _rk4_step(self,f,t,y,h):
        k1=f(t,y); k2=f(t+0.5*h, y+0.5*h*k1); k3=f(t+0.5*h, y+0.5*h*k2); k4=f(t+h, y+h*k3)
        return y + (h/6.0)*(k1+2*k2+2*k3+k4)

    def _rk45_step(self,f,t,y,h):
        c2=1/5; c3=3/10; c4=4/5; c5=8/9; c6=1.0; c7=1.0
        a21=1/5
        a31=3/40; a32=9/40
        a41=44/45; a42=-56/15; a43=32/9
        a51=19372/6561; a52=-25360/2187; a53=64448/6561; a54=-212/729
        a61=9017/3168; a62=-355/33; a63=46732/5247; a64=49/176; a65=-5103/18656
        b1=35/384; b3=500/1113; b4=125/192; b5=-2187/6784; b6=11/84
        b1s=5179/57600; b3s=7571/16695; b4s=393/640; b5s=-92097/339200; b6s=187/2100; b7s=1/40

        k1=f(t,y)
        k2=f(t+c2*h, y+h*(a21*k1))
        k3=f(t+c3*h, y+h*(a31*k1+a32*k2))
        k4=f(t+c4*h, y+h*(a41*k1+a42*k2+a43*k3))
        k5=f(t+c5*h, y+h*(a51*k1+a52*k2+a53*k3+a54*k4))
        k6=f(t+c6*h, y+h*(a61*k1+a62*k2+a63*k3+a64*k4+a65*k5))
        y5 = y + h*( (35/384)*k1 + 0*k2 + (500/1113)*k3 + (125/192)*k4 + (-2187/6784)*k5 + (11/84)*k6 )
        k7=f(t+c7*h, y5)
        y4 = y + h*( b1s*k1 + 0*k2 + b3s*k3 + b4s*k4 + b5s*k5 + b6s*k6 + b7s*k7 )
        err = np.linalg.norm(y5-y4, ord=np.inf)
        return y5, y4, err

    def solve(self, f: Callable[[float, np.ndarray], np.ndarray], t0: float, tf: float, y0, step: Optional[float]=None)->ODEResult:
        import numpy as np
        t0=float(t0); tf=float(tf); tdir=1.0 if tf>=t0 else -1.0
        y0=np.array(y0, dtype=float, ndmin=1)
        h=float(step if step is not None else (self.step if self.step else 0.1))
        if self.h_max: h=min(h, self.h_max); h=abs(h)*tdir

        t_values=[t0]; y_values=[y0.copy()]; steps=0; rejected=0; start=time.time()

        if self.method in ("euler","heun","rk2","rk4"):
            while (tdir>0 and t_values[-1]<tf) or (tdir<0 and t_values[-1]>tf):
                if steps>=self.max_steps: break
                t=t_values[-1]; y=y_values[-1]
                if (tdir>0 and t+h>tf) or (tdir<0 and t+h<tf): h=tf-t
                if self.method=="euler": y_next=self._euler_step(f,t,y,h)
                elif self.method=="heun": y_next=self._heun_step(f,t,y,h)
                elif self.method=="rk2": y_next=self._rk2_midpoint_step(f,t,y,h)
                else: y_next=self._rk4_step(f,t,y,h)
                t_values.append(t+h); y_values.append(y_next); steps+=1
            elapsed=time.time()-start
            return ODEResult(np.array(t_values), np.vstack(y_values), self.method, abs(h), steps, elapsed, message=("OK" if steps<self.max_steps else "Max steps reached"))
        else:
            if step is not None: h=float(step)*tdir
            else: h=(tf-t0)/100.0
            max_err=0.0
            while (tdir>0 and t_values[-1]<tf) or (tdir<0 and t_values[-1]>tf):
                if steps>=self.max_steps: break
                t=t_values[-1]; y=y_values[-1]
                if (tdir>0 and t+h>tf) or (tdir<0 and t+h<tf): h=tf-t
                y5,y4,err=self._rk45_step(f,t,y,h)
                s = 2.0 if err==0 else 0.9*(self.tol/err)**0.2
                if err<=self.tol or abs(h)<=self.h_min:
                    t_values.append(t+h); y_values.append(y5); steps+=1; max_err=max(max_err,float(err))
                    h = max(self.h_min*tdir, s*h)
                else:
                    rejected+=1; h = max(self.h_min*tdir, s*h)
            elapsed=time.time()-start
            return ODEResult(np.array(t_values), np.vstack(y_values), self.method, abs(h), steps, elapsed, max_err, rejected, message=("OK" if steps<self.max_steps else "Max steps reached"))
