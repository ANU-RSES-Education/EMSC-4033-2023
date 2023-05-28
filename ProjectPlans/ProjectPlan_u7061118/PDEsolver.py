'''
This module is designed to solve any one-dimensional first-order Partial Differential Equations (PDEs). This package uses the pseudo-spectral method to solve PDEs, based on the Fourier basis. Functions in this module include:

time_domain(tmax,dt)
create_grid(length,num_of_points)
derivative(grid,f,order)
adv_diff_eq(u,t,grid,D,v)
burger_eq(u,t,grid,D,v)
plot_anim(t,grid,u0,u)
'''

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
from matplotlib import cm

# Temporal Domain
def time_domain(tmax,dt):
    '''
    This is the function used to define the time domain.
    tmax is the total time.
    dt is the time step.
    '''
    t = np.arange(0,tmax,dt)
    return t

# Spatial Domain
class create_grid:
    '''
    This is a class that creates the spatial grid of the PDE.
    This class will store two numpy arrays: the physical grid `x` and the Fourier grid `wavenumber`. 
    The two grids will be calculated once the class is called, and there will be no repeated calculation in later computations.
    '''
    def __init__(self, length, num_of_points):
        self.length = length
        self.num_of_points = num_of_points
    
        def create_x(self):
            '''
            This is the function to find the physical domain x.
            The input is the length of the physical domain and the number of discretisation points.
            the physical domain is centred at 0.
            '''
            dx = self.length/self.num_of_points             # step in the physical domain x
            x = np.arange(-self.length/2,self.length/2,dx)  # x is the numpy array that begin at -Length/2 and end at Length/2 - dx
            return x

        def create_wavenum(self):
            '''
            This is the function to find the Fourier domain, discrete wavenumber domain, of a given physical domain x.
            The output is the Fourier wavenumber domain, a numpy array, kappa.
            '''
            dx = self.length/self.num_of_points             # step in the physical domain x
            kappa = 2*np.pi*np.fft.fftfreq(self.num_of_points,d=dx)
            return kappa

        self.x = create_x(self)
        self.wavenum = create_wavenum(self)
        return

# Derivative calculation using the pseudo-spectral method
def derivative(grid, f, order):
    '''
    This is the function for finding the derivative of a function f with domain x, using the pseudo-spectral method. 
    The function f is being transformed to the Fourier basis and then calculate the derivative by multiplying i*wave number.
    The order of derivative can be defined at the beginning as an input.
    The output is the given order derivative in the physical domain.
    '''
    κ = grid.wavenum                          # wavenumber domain for the function f
    fhat = np.fft.fft(f)                      # Fourier tranform of f
    d_ord_fhat = ((1j*κ)**order)*fhat         # the 'order'th derivative of fhat 
    d_ord_f = np.fft.ifft(d_ord_fhat).real    # the 'order'th derivative of f
      
    return d_ord_f

# Advection-Diffusion equation
def adv_diff_eq(t,u,grid,D,v):
    '''
    This function is for deriving the advection diffusion equation with RHS fully solved.
    This function will be implemented in the below integration function.
    t is the temporal domain, which should take the form t = time_domain(tmax,dt).
    grid is the grid of spatial domain, containing the physical domain and fourier domain.
    D is the diffusion coefficient.
    v is the advection velocity.
    '''
    d_u = derivative(grid,u,1)
    dd_u = derivative(grid,u,2)
    
    du_dt = D*dd_u - v*d_u
    return du_dt

def burger_eq(t,u,grid,D):
    '''
    This function is for deriving the burger's equation with rhs fully solved.
    t is the temporal domain, which should take the form t = time_domain(tmax,dt).
    grid is the grid of spatial domain, containing the physical domain and fourier domain.
    D is the diffusion coefficient.
    '''
    d_u = derivative(grid,u,1)
    dd_u = derivative(grid,u,2)
    
    du_dt = D*dd_u - u*d_u
    return du_dt

# Set up animated plot
def plot_anim(t,grid,u0,u):
    '''
    This function is used to plot the stationary plot and animation of the wave.
    The first subplot shows the initial state and the final state of the function.
    The second subplot shows the movement of the wave with time. 
    '''
    x = grid.x
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
    
    ax1.plot(x,u0,label='u at t = 0')
    ax1.plot(x,u.y[:,-1],label='u at t = $t_{final}$')
    ax1.set_title('Stationary plot for $u(x,t)$')
    ax1.set_xlabel('x')
    ax1.set_ylabel('u')
    ax1.legend(fontsize=12)

    line, = ax2.plot([],[],lw=3)
    ax2.set_xlim((x[0],x[-1]))
    ax2.set_ylim((np.min(u.y),np.max(u.y)))
    ax2.set_title('t = {:.3f}'.format(t[0])) 

    def plot_frame(i):
        line.set_data(x,u.y[:,i])
        ax2.set_title('t = {:.3f}'.format(t[i]))
        fig.canvas.draw()
        return line,

    # Animate the solution
    anim = animation.FuncAnimation(fig, plot_frame,frames=len(t),interval=80,repeat=False,blit=True)
    plt.close()
    
    return HTML(anim.to_jshtml())