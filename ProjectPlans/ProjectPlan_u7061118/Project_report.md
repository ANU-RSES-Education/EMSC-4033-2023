# EMSC4033 - Project Report
## Title: Use the pseudo-spectral method to solve one-dimensional first-order PDEs
Ashley Huang u7061118


---
### Introduction
The [PDEsolver](PDEsolver.py) module aims to use the **pseudo-spectral method** to solve **one-dimensional first-order Partial Differential Equations (PDEs)** with periodic boundary conditions. For example the one-dimensional **Advection-Diffusion equation**:

<font size= "3">$$\frac{\partial u}{\partial t} = D\frac{\partial^2 u}{\partial x^2} - v\frac{\partial u}{\partial x}$$</font>

where $u(x,t)$ is the quantity being transported, $t$ is time, $x$ is the spatial coordinate along the one-dimensional domain, $D$ is the diffusion coefficient, and $v$ is the velocity of the flow. 


---
### Instructions

In order to use this package and solve the PDE, the user needs to import `PDEsolver` package, as well as `numpy` and `scipy.integrate.solve_ivp`.  

`PDEsolver` contains five functions and one class:  
1) `time_domain(tmax,dt)`: function for defining a time domain of the PDE.
2) `create_grid(length,num_of_points)`: class for defining a spatial domain of the PDE, including the physical domain **x** and Fourier domain **wavenum**.
3) `derivative(grid,f,order)`: function for calculating the 'order'th derivative of f(x) using the pseudo-spectral method.
4) `adv_diff_eq(u,t,grid,D,v)`: function for defining the Advection-Diffusion equation as an ODE returning $\frac{du}{dt} = $ RHS, where RHS is simplified using the `derivative()` function.
5) `burger_eq(u,t,grid,D,v)`: function for defining the Burger's equation as an ODE returning $\frac{du}{dt} = $ RHS, where RHS is simplified using the `derivative()` function.
6) `plot_anim(t,grid,u0,u)`: function for plotting the solution at $t_0$ and $t_{final}$ and the animation of the solution.  

These provide all necessary inputs for transforming a PDE into an Ordinary Differential Equation (ODE) and then solve it using an ODE solver function: `scipy.integrate.solve_ivp(fun,t_span,y0,method='RK45',t_eval=None,args=None,...)`. 

Here is a demonstration of using `PDEsolver` to solve the 1d first-order advection-diffusion equation:
```Python
# Step 1: Import all necessary modules 
# (There is no need to import plotting modules as they will be automatically imported from `PDEsolver`)
import PDEsolver
import numpy as np
from scipy.integrate import solve_ivp

# Step 2: Define temporal and spatial domains
t = PDEsolver.time_domain(tmax,dt)
grid = PDEsolver.create_grid(length, num_of_points)
x = grid.x

# Step 3: Define necessary parameters (depending on the equation aiming to solve)
D = 1.0 # diffusivity rate
v = 1.0 # advection velocity

# Step 4: Define the initial condition
u0 = 1/np.cosh(x)**2

# Step 5: Solution of the advection-diffusion equation
u = solve_ivp(PDEsolver.adv_diff_eq, [t[0],t[-1]], u0, method='RK45', t_eval=t, args=(grid,D,v))

# Step 6: Plot the solution
PDEsolver.plot_anim(t,grid,u0,u)
```
Please refer to [Project_user.ipynb](Project_user.ipynb) for examples of user applying `PDEsolver` module when finding PDE solutions.

<!-- #region -->
---
### List of dependencies + short description

- **numpy**: a package to efficiently manipulate multi-dimensional arrays.   
    *In `PDEsolver`, the main usage of `numpy` is to transform functions between the physical basis and the Fourier basis using the `numpy.fft.fft()` and `numpy.fft.ifft()` functions.*

- **scipy**: a collection of useful mathematical algorithms.  
    *After providing all necessary input parameters by the `PDEsolver`, the `scipy.integrate.solve_ivp()` function can solve ODEs transformed from PDEs. Generally, integration method of `method = 'DOP853'` is recommanded as it is fast in computation while maintaining good accuracy of results. However, other methods could provide better solutions in some circumstances.* 

- **matplotlib**: a comprehensive library for creating static, animated, and interactive visualizations.  
    *In `PDEsolver`, `matplotlib` are used to plot the stationary and animated plots of the evolution of functions.*

- **IPython**: a tool for interactive and parallel computing in Python.  
    *In `PDEsolver`, `IPython.display.HTML()` is used to create the interactive animation of changing functions.*

The `requirements.txt` contains all the listed dependencies as above. The user could use the `requirements.txt` to install all the dependencies by executing the following command in the terminal:

```bash
pip install -r requirements.txt
```
If the packages are already installed, the user could use the following command to update these packages:
```bash
pip install -r requirements.txt --upgrade
```
<!-- #endregion -->

---
### Test and Validation

**Test** functions are written in the notebook [Project_test.ipynb](Project_test.ipynb) for testing most functions that include computations.
1) `test_grid(tol)` aims to ensure the **class** `create_grid()` returns the correct physical and Fourier domains. This function uses $x = [-\frac{2}{\pi},\frac{-3\pi}{2},-\pi,-\frac{\pi}{2},0,\frac{\pi}{2},\pi,\frac{3\pi}{2}]$ as an example. The absolute mean error of both domains are calculated, and `assert` function is used to ensure the error is smaller than the chosen tolerance of $10^{-12}$. 

2) `test_derivative(tol)` aims to ensure the **function** `derivative()` returns the correct spatial derivative of u(x). This function uses $f = sin(2x)$ as an example to find the second derivative of f, which the true answer is $-4sin(2x)$. The absolute mean error of the result is calculated, and `assert` function is used to ensure the error is smaller than the chosen tolerance of $10^{-12}$.

3) `test_solve_dudt(D,v,tol)` aims to ensure the **function** `adv_diff_eq()` works well in solving the *advection-diffusion equation* when using the `scipy.intergrate.solve_ivp`. This function uses Gaussian initial condition to test the PDE solution under *advection only* case and *diffusion only* case. The absolute mean error of the result is calculated between the numerical solution and the analytical solution. The analytical solution is $u_{final} = u_0(x - vt)$ using the defined function `gaussian_solution` (this accounts for the advection over time), and the function already contains diffusion as an input parameter. `assert` function is used to ensure the error is smaller than the chosen tolerance of $10^{-6}$.

4) Stationary and animated plots are tested interdependently as the stationary plots consist both the initial and final states of the function, and the animated plots show the evolution of the function over time. Both plots should be consistent and this could be ensured by visuallisation directly.

**Validation** of input for each function is done by ensuring all inputs are numerical values and meeting certain conditions. The exception handling of each function has been done using the `try` and `except` commands. The `plot_anim()` function has also added the validation of input for animation making for handling 'IndexError'. Animation cannot be formed when the size of domain 'x' and the solution 'u' does not match with each other. Details can be found in the `PDEsolver.py` and examples are shown in the `Project_test.ipynb` file. 

---
### Error Evaluation
Error evaluation in terms of PDE solution absolute mean error, convergence, run-time, and comparison with `py-pde` solutions are done in addition to above testing and validation. Please refer to [Project_error_evaluation.ipynb](Project_error_evaluation.ipynb) for analysis and discussion.



---
### Limitations
- The `PDEsolver` package only works for one-dimensional and first-order PDEs, which is a very strict rule for solving PDEs. When people actually solve PDE in climate models, generally PDEs are at least two-dimentsional (dim = lat and lon) and to multiple orders. Therefore, this package is only a beginning of solving PDEs using the pseudo-spectral methods. 
- With certain initial conditions, the PDE could not be solved or is easy to break. Typically, trigonometry functions are not suitable to become the initial condition of a PDE when using the pseudo-spectral method to solve for PDEs unless some specific spatial domain is matched with it. For example, the -sin(x) function travelling with the Burger's equation. This is because of the Fourier transform calculations involved in the pseudo-spectral method. Therefore, the `PDEsolver` package requires careful choice of initial conditions. 
- With certain extreme choice of parameters in the PDE, for example the D and v in the advection-diffusion equation, the PDE solution would be easy to break. Noise may be introduced into the solution when the parameters are some unwise choices. Therefore, careful selection of parameter values is needed.
- The temporal integration method in `scipy.integrate.solve_ivp` could affect the PDE solution smoothness. Therefore, wise choise of integration method is recommanded.
- The error of the calculations is generally at $10^{-5}$ to $10^{-8}$, which is relatively good but not accurate enough for more sophisticated calculations. This needs to be improved for more general implementation of the package.




---
### Future Improvements	
- The package could be improved by adding more built-in one-dimentional first-order PDEs to become more useful for users.
- The package could be then improved by extending the application into higher-dimensional and multi-order PDEs.
    - Multi-dimensional PDEs: include another function for solving the derivatives in the **y** dimension, and more other dimensions.
    - Multi-order PDEs: include another function for transforming multi-order PDEs into a system of first-order PDEs, and then implement the `PDEsolver` package.
- The package could  introduce better error handling methods to improve noise/error caused by Fourier transform and inverse Fourier transform calculations.
