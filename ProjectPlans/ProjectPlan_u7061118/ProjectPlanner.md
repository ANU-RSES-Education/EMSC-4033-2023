# Pseudo-spectral Method for Solving Advection-Diffusion Equation

## Executive summary

Earth’s ocean circulation is a complex system that is driven by large-scale surface wind patterns and internal density variations. Commonly, sophisticated mathematical models are used to simulate ocean circulation based on geophysical fluid dynamic theories. In this project, I plan to build a set of functions to solve geophysics-related partial differential equations (PDEs) that are usually associated with climate models, for example, the advection-diffusion equation. Specifically, I will use the pseudo-spectral method as the main method for solving PDEs. The set of functions (ideally will be compacted into a package) will be uploaded to GitHub, with the testing boundary conditions, initial conditions, parameters and the resultant plots. 

## Goals

The goal of this project is to establish a package that solves 1D PDEs using the pseudo-spectral method, specifically the Advection-Diffusion Equation. The pseudo-spectral method has high accuracy than the finite differences method (used by `py-pde`). The project will be divided into two parts, which the first part is to build the functions for solving PDEs with tests and the second part is to apply the functions to solve the PDEs. 

**First part**: Build a set of mathematical functions for solving several essential components in a PDE. 
-	Create the domain in both the physical space and the wavenumber space using a periodic Boundary Condition (BC)
-	Write the functions for computing derivatives using the pseudo-spectral method
-	Write the functions for time-stepping (time-integral) using the Gaussian Quadrature method, or possibly another better quadrature method

**Second part**: Use these functions to solve PDE(s) as a user, possibly anyone who wants to solve 1D PDEs more efficiently
-	Use the built functions to find the solutions of PDE(s), for instance, the advection-diffusion equation
-	Plot to visualise the PDE solutions using the `matplotlib` package


## Background and Innovation  

This project aims to develop a framework for solving PDEs in the periodic domain using the pseudo-spectral method. The pseudo-spectral method is a numerical technique used for solving PDEs in many fields, including fluid dynamics, quantum mechanics, and weather forecasting. The pseudo-spectral method works by transforming the PDE into an algebraic equation in the Fourier space, as chosen in this project. The algebraic equation can then be solved using standard linear algebra techniques, which involves computing the Fourier of the derivatives and the forcing terms in the PDE. These functions have the property that they can represent any periodic function to arbitrary accuracy, and they are efficient to compute using fast Fourier transforms (FFT). Overall, the pseudo-spectral method is a powerful and widely used technique for solving PDEs, and it continues to be an active area of research in numerical analysis and scientific computing.

The developed functions for solving PDEs will be then applied to solve the 1-dimensional **Advection-Diffusion equation**:

<p style="text-align: center;"><font size= "4">$\frac{\partial u}{\partial t} = D\frac{\partial^2 u}{\partial x^2} - v\frac{\partial u}{\partial x}$</font></p> 

where $u(x,t)$ is the quantity being transported, $t$ is time, $x$ is the spatial coordinate along the one-dimensional domain, $D$ is the diffusion coefficient, and $v$ is the velocity of the flow. This project could eventually contribute to my own research having a part in investigating the Quasi-geostrophic (QG) equations, a set of multi-dimensional PDEs that simulates the surface ocean flow.

Currently, the common method for solving PDEs in Python is to use the `py-pde` package, or the combination of `numpy` and `scipy` packages that have FFT and quadrature functions separately. The `py-pde` package could be used to solve specific PDEs, such as the Laplace equation, diffusion equation, and more. However, the `py-pde` package solves PDEs using finite differences that is more flexible with BCs but with lower accuracy. This project could provide a more general set of functions that could potentially solve more PDEs with higher accuracy that do not follow the fundamental forms of these classical PDEs. 


## Resources & Timeline

-	This project will be supervised by Dr Navid Constantinou 
-	I will be writing up the code for solving PDEs with periodic domains using the pseudo-spectral method, specifically using the existing `numpy.fft` and `scipy.integrate` packages (and possibly more other packages)
-	The solutions for the Advection-Diffusion equation will then be computed using the written functions
-	The solutions will also be plotted using `matplotlib.pyplot` for visualisation


## Testing, validation, documentation

Since the Advection-Diffusion equation is a common equation with a known solution, it is not difficult to check the correctness of the solution. It is also possible to use a specific PDE that could be solved by using the `py-pde` package to test the correctness of the solution. Solutions computed by the `py-pde` package and the self-developed package can be compared to validate the results. 

Comments and Documentation will be recorded consistently throughout the coding part of the project. 
