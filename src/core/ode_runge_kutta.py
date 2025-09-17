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
    k1_values: Optional[np.ndarray] = None
    k2_values: Optional[np.ndarray] = None
    k3_values: Optional[np.ndarray] = None
    k4_values: Optional[np.ndarray] = None
    y_next_values: Optional[np.ndarray] = None

class RungeKuttaSolver:
    SUPPORTED = ("euler","heun","rk4")
    def __init__(self, method="rk4", step: Optional[float]=0.1, tol: float=1e-6, h_min: float=1e-6, h_max: Optional[float]=None, max_steps: int=1_000_000):
        if method.lower() not in self.SUPPORTED: raise ValueError("Método no soportado")
        self.method=method.lower(); self.step=step; self.tol=tol; self.h_min=h_min; self.h_max=h_max; self.max_steps=max_steps

    def _euler_step(self,f,t,y,h): 
        y_next = y + h*f(t,y)
        return y_next, y_next  # Retorna y_next dos veces para mantener consistencia con RK4
    def _heun_step(self,f,t,y,h):
        k1=f(t,y); k2=f(t+h, y+h*k1); return y + (h/2.0)*(k1+k2)
    def _rk4_step(self,f,t,y,h):
        k1=f(t,y); k2=f(t+0.5*h, y+0.5*h*k1); k3=f(t+0.5*h, y+0.5*h*k2); k4=f(t+h, y+h*k3)
        y_next = y + (h/6.0)*(k1+2*k2+2*k3+k4)
        return y_next, k1, k2, k3, k4

    def solve(self, f: Callable[[float, np.ndarray], np.ndarray], t0: float, tf: float, y0, step: Optional[float]=None)->ODEResult:
        import numpy as np
        t0=float(t0); tf=float(tf); tdir=1.0 if tf>=t0 else -1.0
        y0=np.array(y0, dtype=float, ndmin=1)
        h=float(step if step is not None else (self.step if self.step else 0.1))
        if self.h_max: h=min(h, self.h_max); h=abs(h)*tdir

        t_values=[t0]; y_values=[y0.copy()]; steps=0; start=time.time()
        k1_values=[]; k2_values=[]; k3_values=[]; k4_values=[]; y_next_values=[]

        while (tdir>0 and t_values[-1]<tf) or (tdir<0 and t_values[-1]>tf):
            if steps>=self.max_steps: break
            t=t_values[-1]; y=y_values[-1]
            if (tdir>0 and t+h>tf) or (tdir<0 and t+h<tf): h=tf-t
            if self.method=="euler": 
                y_next, y_next_calc = self._euler_step(f,t,y,h)
                k1_values.append(None); k2_values.append(None); k3_values.append(None); k4_values.append(None); y_next_values.append(y_next_calc.copy())
            elif self.method=="heun": 
                y_next=self._heun_step(f,t,y,h)
                k1_values.append(None); k2_values.append(None); k3_values.append(None); k4_values.append(None); y_next_values.append(None)
            else: 
                y_next, k1, k2, k3, k4 = self._rk4_step(f,t,y,h)
                k1_values.append(k1.copy()); k2_values.append(k2.copy()); k3_values.append(k3.copy()); k4_values.append(k4.copy()); y_next_values.append(y_next.copy())
            t_values.append(t+h); y_values.append(y_next); steps+=1
        elapsed=time.time()-start
        
        # Convert lists to arrays for methods that support it
        if self.method == "rk4":
            k1_array = np.vstack(k1_values) if k1_values else None
            k2_array = np.vstack(k2_values) if k2_values else None
            k3_array = np.vstack(k3_values) if k3_values else None
            k4_array = np.vstack(k4_values) if k4_values else None
            y_next_array = np.vstack(y_next_values) if y_next_values else None
        elif self.method == "euler":
            k1_array = k2_array = k3_array = k4_array = None
            y_next_array = np.vstack(y_next_values) if y_next_values else None
        else:
            k1_array = k2_array = k3_array = k4_array = y_next_array = None
            
        return ODEResult(np.array(t_values), np.vstack(y_values), self.method, abs(h), steps, elapsed, 
                        message=("OK" if steps<self.max_steps else "Max steps reached"),
                        k1_values=k1_array, k2_values=k2_array, k3_values=k3_array, k4_values=k4_array, y_next_values=y_next_array)
