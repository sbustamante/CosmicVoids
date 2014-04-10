#voids_density_histogram.py
#
#This code calculates histograms of mean density for void regions according to Lambda_thr values
#Usage: voids_density_histogram.py <Compute histograms(0), Only quartiles(1)>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Number of sections
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Web Scheme
webs = ['Vweb', 'Tweb']
#Styles
color = ['blue','green']

#N Lambda
N_l = 100
#Lambdas extremes values
L_min = 0
L_max = 1
#Lambda array
Lambda = np.linspace(L_min, L_max, N_l+1)

#N delta
N_d = 2000
#Delta extremes values
D_min = -1
D_max = 1

#Uncertain of quartiles
Delta_Q = 0.005

#==================================================================================================
#			CONSTRUCTING HISTOGRAMS
#==================================================================================================
N_sim = len(folds)

i_web = 0
for web in webs:
    i_fold = 0
    #Quartiles array
    Quart = np.zeros( (N_l-1,4) )
    for fold in folds:
	print fold, web
	
	if sys.argv[1] == "0":
	    #Loading eigenvalues
	    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
	    #Loading density
	    delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
	    #Calculating mean densities associated to differents kind of regions
	    Voids_Histograms( eigV_filename, delta_filename, L_min, L_max, N_l, D_min, D_max, \
	    N_d, '%svoids_delta_hist/%s'%(data_figures_fold,web) )
	    print 'Histogram of mean density for voids, %s scheme: done!'%(web)
	
	for i_l in xrange( N_l-1 ):
	    lamb = Lambda[i_l]
	    hist_void = np.loadtxt( '%svoids_delta_hist/%s/delta_voids_hist_%1.2f.dat'%(data_figures_fold,web,lamb) )
	    for i_d in range( N_d-1 ):
		Quart[i_l,0] = lamb
		#Q1
		if 0.25 - Delta_Q <= hist_void[i_d,2]/hist_void[-1,2] <= 0.25 + Delta_Q:
		    Quart[i_l,1] = hist_void[i_d,0]
		#Median
		elif 0.50 - Delta_Q <= hist_void[i_d,2]/hist_void[-1,2] <= 0.50 + Delta_Q:
		    Quart[i_l,2] = hist_void[i_d,0]
		#Q3
		elif 0.70 - Delta_Q <= hist_void[i_d,2]/hist_void[-1,2] <= 0.70 + Delta_Q:
		    Quart[i_l,3] = hist_void[i_d,0]
		    
	np.savetxt( '%svoids_delta_hist/%s/quartiles.dat'%(data_figures_fold,web), Quart )
	
	i_fold += 1
    i_web += 1