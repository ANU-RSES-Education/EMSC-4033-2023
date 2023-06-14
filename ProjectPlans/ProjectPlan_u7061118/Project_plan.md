# Pseudo-spectral Method for Solving one-dimensional first-order PDEs

## Executive summary

Earth’s ocean circulation is a complex system that is driven by large-scale surface wind patterns and internal density variations. Commonly, sophisticated mathematical models are used to simulate ocean circulation based on geophysical fluid dynamic theories. In this project, I plan to build a set of functions to solve geophysics-related partial differential equations (PDEs) that are usually associated with climate models, for example, the advection-diffusion equation. Specifically, I will use the **pseudo-spectral method**, and focus on solving **one-dimentional first-order PDEs**. The set of functions will be compacted into a package and then uploaded to GitHub, with tests and validation of PDE initial conditions, parameters, and resultant plots. The repository will also include a notebook to show how a user could use the new package to solve PDEs. 

## Goals

The goal of this project is to establish a package that solves one-dimentional first-order PDEs using the pseudo-spectral method. The detailed goals are as below:

- Build a set of mathematical functions for solving essential components in a PDE  
    - Define the function that creates the time domain
    - Define the function that creates the domain in both the physical space and the wavenumber space using a periodic Boundary Condition (BC)
    - Define the function for computing derivatives using the pseudo-spectral method
    - Find the time-stepping (time-integral) using the `scipy.integrate.solve_ivp()` function and all written functions (above)
    - Define the function for visualising PDE solutions
- Ensure the correctness and accuracy of the new package by writing up test functions and validations for exception handling
- Demonstrate the usage of the new package by using it to solve PDEs as a user
- Compare and evaluate the performance of this new package with currently existing package of `py-pde`


## Background and Innovation  

This project aims to develop a framework for solving PDEs in the periodic domain using the pseudo-spectral method. The pseudo-spectral method is a numerical technique used for solving PDEs in many fields, including fluid dynamics, quantum mechanics, and weather forecasting. The pseudo-spectral method works by transforming the PDE into an algebraic equation in the Fourier space, as chosen in this project. The algebraic equation can then be solved using standard linear algebra techniques, which involves computing the Fourier derivatives and the forcing terms in the PDE. These functions have the property that they can represent any periodic function to arbitrary accuracy, and they are efficient to compute using fast Fourier transforms (FFT). Overall, the pseudo-spectral method is a powerful and widely used technique for solving PDEs, and it continues to be an active area of research in numerical analysis and scientific computing.

The developed functions for solving PDEs will be then applied to solve one-dimensional first-order PDEs, for example the **Advection-Diffusion equation**:

<p style="text-align: center;"><font size= "4">$\frac{\partial u}{\partial t} = D\frac{\partial^2 u}{\partial x^2} - v\frac{\partial u}{\partial x}$</font></p> 

where $u(x,t)$ is the quantity being transported, $t$ is time, $x$ is the spatial coordinate along the one-dimensional domain, $D$ is the diffusion coefficient, and $v$ is the velocity of the flow. 

## Review of existing code

Currently, the common method for solving PDEs in Python is to use the `py-pde` package. The `py-pde` package could be used to solve PDEs to multiple dimensions and high orders, such as the Laplace equation, diffusion equation, and more. However, the `py-pde` package solves PDEs using **finite differences method** that is more flexible with BCs but with lower accuracy. Generally, the **pseudo-spectral method** has a higher accuracy than the finite differences method (used by `py-pde`) due to the better performance of approximating functions using the Fourier transform. This project could provide a more general set of functions that could potentially solve PDEs with higher accuracy. 


## Resources & Timeline
This project will be supervised by Dr Navid Constantinou 
- Step 1: Write the functions for defining time and spatial domains, and then the function for calculating the spatial derivatives
- Step 2: Write the functions for solving one-dimensional first-order PDEs and plotting PDE solutions
- Step 3: Define test functions and validation commands to ensure the correctness of functions
- Step 4: Use various examples to test and demonstrate the usage of the new package. This includes different parameter choices, initial condition choices, and temporal integration method choices.
- Step 5: Analyse the convergence, error, and operation speed of the new package. Then, compare with `py-pde` in terms of these properties.

Main packages required for the project
- `numpy` and `scipy` are the main packages to use for solving PDEs using the pseudo-spectral methods. Specifically, `numpy.fft` will be used to calculate the spatial derivatives and `scipy.integrate.solve_ivp()` will be used to calculate the final PDE solution after transforming a PDE into an ODE using the pseudo-spectral method.
-	The solutions will also be plotted using the `matplotlib` package for visualisation.


## Testing, validation, documentation

### Testing
The main method will be to compare the results between numerical solutions and analytical solutions. Test functions will be written for all necessary functions to ensure the correctness of the returned outputs. The Advection-Diffusion equation is a common equation with a known solution when initial condition is the Gaussian equation. Therefore, the error of numerical solution is easy to calculate. It is also possible to use a specific PDE that could be solved by using the `py-pde` package to test the correctness of the solution. Solutions computed by the `py-pde` package and the self-developed package can be compared to validate the results. 

### Validation
Input validation will be done by adding `try` and `except` commands to ensure the input of all functions are numerical values or functions, not strings or other data type. Certain possible errors would be handled to tell what specific parameters or conditions needed to be changed. 

### Documentation
Comments and docstring will be added consistently throughout the coding part of the project. The `Project_report.md` file will have the documentation of the project. It will contain the structure as:
- **Introduction**: description of the project background
- **Instruction**: the user manual and samples for using the new package
- **Dependencies**: all necessary external packages required by this project
- **Test and Validation**: details about the test functions and validation steps
- **Error evaluation**: detailed analysis about the performance of the new package
- **Limitation**: flaws or insufficient part of the package
- **Further improvement**: possible routes for improving the package
