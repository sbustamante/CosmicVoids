#halos_velocity_environment.py
#
#This code calculates the median peculiar velocity of dark matter halos embedded into each one of 
#the defined type of environments and for several lambda_th values
#Usage: halos_velocity_environment.py <Tweb or Vweb> <BDM or FOF>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Number of sections
N_sec = 256
#Smooth parameter
smooth = '_s1'
#Halo Scheme
catalog = sys.argv[2]
#Web Scheme
web = sys.argv[1]


#N Lambda
N_l = 100
#Lambdas extremes values
L_min = 0
L_max = 1
#Lambda array
Lambda = np.linspace(L_min, L_max, N_l)

#==================================================================================================
#			CONSTRUCTING HISTOGRAMS
#==================================================================================================
#Meadian mass and Q1 and Q3 quartiles
Quartiles = np.zeros( (N_l, 13) )
print simulation, web

#Loading general catalog of halos
GH = np.loadtxt('%s%sC_GH_%s.dat'%(foldglobal,simulation,catalog))

#Loading eigenvalues
eigV = np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,simulation,web,N_sec,smooth,catalog))

for i_l in xrange( N_l ):
    lamb = Lambda[i_l]
    #Storing lambda value
    Quartiles[i_l,0] = lamb
    #Halos in Voids
    bool_v = (eigV[:,1] <= lamb)*(eigV[:,2] <= lamb)*(eigV[:,3] <= lamb)
    Vel = np.sort( np.sqrt( GH[bool_v,4]**2 + GH[bool_v,5]**2 + GH[bool_v,6]**2 ) )
    Quartiles[i_l,1] = Vel[ int(len(Vel)*0.25) ]
    Quartiles[i_l,2] = Vel[ int(len(Vel)*0.5) ]
    Quartiles[i_l,3] = Vel[ int(len(Vel)*0.75) ]
    
    #Halos in Sheets
    bool_s = (eigV[:,1] > lamb)*(eigV[:,2] <= lamb)*(eigV[:,3] <= lamb)
    Vel = np.sort( np.sqrt( GH[bool_s,4]**2 + GH[bool_s,5]**2 + GH[bool_s,6]**2 ) )
    Quartiles[i_l,4] = Vel[ int(len(Vel)*0.25) ]
    Quartiles[i_l,5] = Vel[ int(len(Vel)*0.5) ]
    Quartiles[i_l,6] = Vel[ int(len(Vel)*0.75) ]
    
    #Halos in Filaments
    bool_f = (eigV[:,1] > lamb)*(eigV[:,2] > lamb)*(eigV[:,3] <= lamb)
    Vel = np.sort( np.sqrt( GH[bool_f,4]**2 + GH[bool_f,5]**2 + GH[bool_f,6]**2 ) )
    Quartiles[i_l,7] = Vel[ int(len(Vel)*0.25) ]
    Quartiles[i_l,8] = Vel[ int(len(Vel)*0.5) ]
    Quartiles[i_l,9] = Vel[ int(len(Vel)*0.75) ]
    
    #Halos in Knots
    bool_k = (eigV[:,1] > lamb)*(eigV[:,2] > lamb)*(eigV[:,3] > lamb)
    Vel = np.sort( np.sqrt( GH[bool_k,4]**2 + GH[bool_k,5]**2 + GH[bool_k,6]**2 ) )
    Quartiles[i_l,10] = Vel[ int(len(Vel)*0.25) ]
    Quartiles[i_l,11] = Vel[ int(len(Vel)*0.5) ]
    Quartiles[i_l,12] = Vel[ int(len(Vel)*0.75) ]
	    
np.savetxt( '%shalos_velocities_%s_%s.dat'%(data_figures_fold,catalog,web),\
Quartiles, fmt="%1.5e\t\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e\t%1.5e" )