import geopy
import snap
import pickle as pkl
import filterpy 
import numpy as np
from filterpy.monte_carlo import systematic_resample
from numpy.linalg import norm
from numpy.random import uniform 
from numpy.random import randn
import scipy.stats
import matplotlib.pyplot as plt

terrorism_dict = pkl.load(open('gtd_group_dict.pkl', 'rb'))
ISIS_dict = terrorism_dict["Irish Republican Army (IRA)"]
terror_raw = pkl.load(open('raw_gtd_data.pkl', 'rb'))
attack_event_ids = []
year = [y for y in range(1970, 2017)]
month = [m for m in range(1, 13)]
for y in year:
	if str(y) not in ISIS_dict:
		continue
	for m in month:
		if str(m) not in ISIS_dict[str(y)]:
			continue
		attack_event_ids += ISIS_dict[str(y)][str(m)]
attack_loactions = []
for i in attack_event_ids:
	try:
		attack_loactions += [np.array([float(terror_raw[i]['longitude']), float(terror_raw[i]['latitude'])])]	
	except:
		continue	

def create_uniform_particles(x_range, y_range, hdg_range, N):
    particles = np.empty((N, 3))
    particles[:, 0] = uniform(x_range[0], x_range[1], size=N)
    particles[:, 1] = uniform(y_range[0], y_range[1], size=N)
    particles[:, 2] = uniform(hdg_range[0], hdg_range[1], size=N)
    particles[:, 2] %= 2 * np.pi
    return particles

def create_gaussian_particles(mean, std, N):
    particles = np.empty((N, 3))
    particles[:, 0] = mean[0] + (randn(N) * std[0])
    particles[:, 1] = mean[1] + (randn(N) * std[1])
    particles[:, 2] = mean[2] + (randn(N) * std[2])
    particles[:, 2] %= 2 * np.pi
    return particles

def predict(particles, u, std, dt=1.):
    """ move according to control input u (heading change, velocity)
    with noise Q (std heading change, std velocity)`"""

    N = len(particles)
    # update heading
    particles[:, 2] += u[0] + (randn(N) * std[0])
    particles[:, 2] %= 2 * np.pi

    # move in the (noisy) commanded direction
    dist = (u[1] * dt) + (randn(N) * std[1])
    particles[:, 0] += np.cos(particles[:, 2]) * dist
    particles[:, 1] += np.sin(particles[:, 2]) * dist

def update(particles, weights, z, R, landmarks):
    weights.fill(1.)
    for i, landmark in enumerate(landmarks):
        distance = np.linalg.norm(particles[:, 0:2] - landmark, axis=1)
        weights *= scipy.stats.norm(distance, R).pdf(z[i])

    weights += 1.e-300      # avoid round-off to zero
    weights /= sum(weights) # normalize

def estimate(particles, weights):
    """returns mean and variance of the weighted particles"""

    pos = particles[:, 0:2]
    mean = np.average(pos, weights=weights, axis=0)
    var  = np.average((pos - mean)**2, weights=weights, axis=0)
    return mean, var

def neff(weights):
    return 1. / np.sum(np.square(weights))

def resample_from_index(particles, weights, indexes):
    particles[:] = particles[indexes]
    weights[:] = weights[indexes]
    weights.fill (1.0 / len(weights))

x_range = (-180, 181)
y_range = (-90, 91)
hdg_range = (0, 1)
n = 20000
landmarks = np.array([[i * 2, i] for i in range(-90, 91)])

def run_pf1(N, sensor_std_err=.1, 
            do_plot=True, plot_particles=False,
            xlim=(0, 20), ylim=(0, 20),
            initial_x=None, landmarks=None, positions=[]):
    NL = len(landmarks)
   

    plt.figure()
    plt.xlim(*xlim)
    plt.ylim(*ylim)
    # create particles and weights
    if initial_x is not None:
        particles = create_gaussian_particles(
            mean=initial_x, std=(5, 5, np.pi/4), N=N)
    else:
        particles = create_uniform_particles(xlim, ylim, (0, 1), N)
    weights = np.zeros(N)

    if plot_particles:
        alpha = .20
        if N > 5000:
            alpha *= np.sqrt(5000)/np.sqrt(N)           
        plt.scatter(particles[:, 0], particles[:, 1], 
                    alpha=alpha, color='g')
    
    xs = []
    for x in range(len(positions)):
        print x
        robot_pos = positions[x]

        # distance from robot to each landmark
        zs = (norm(landmarks - robot_pos, axis=1) + (randn(NL) * sensor_std_err))

        # move diagonally forward to (x+1, x+1)
        predict(particles, u=(0.00, 1.414), std=(.2, .05))
        
        # incorporate measurements
        update(particles, weights, z=zs, R=sensor_std_err, 
               landmarks=landmarks)
        
        # resample if too few effective particles
        if neff(weights) < N/2:
            indexes = systematic_resample(weights)
            resample_from_index(particles, weights, indexes)

        mu, var = estimate(particles, weights)
        xs.append(mu)

        if plot_particles:
            plt.scatter(particles[:, 0], particles[:, 1], 
                        color='k', marker=',', s=1)
        p1 = plt.scatter(robot_pos[0], robot_pos[1], marker='+',
                         color='k', s=180, lw=3)
        p2 = plt.scatter(mu[0], mu[1], marker='s', color='r')
    
    xs = np.array(xs)
    # plt.plot(xs[:, 0], xs[:, 1])
    print('final position error, variance:\n\t', mu - np.array([len(positions), len(positions)]), var)
    plt.legend([p1, p2], ['Actual', 'PF'], loc=4, numpoints=1)
    plt.title('Irish Republican Army (IRA)')
    plt.show()
    

run_pf1(N=n, plot_particles=False, xlim=x_range, ylim=y_range, landmarks=landmarks, positions=attack_loactions)


