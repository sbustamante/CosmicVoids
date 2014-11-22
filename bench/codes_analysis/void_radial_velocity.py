#void_radial_velocity.py
#
#This code computes radial histograms of the velocity profile of voids as computed by the three 
#defined schemes
#
#Usage: run void_radial_velocity.py <Vweb or Tweb> <FAG or DLT> <Nth MF and BR>
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
#Box lenght [Mpc]
L_box = 250.
#Smooth parameter
smooth = '_s1'
#Web Scheme
web = sys.argv[1]
#Config
config = sys.argv[3]
#Void finder scheme (FAG or DLG)
void_scheme = sys.argv[2]
#Cutt of respect to the number of cells
N_cut = 2

#Bins of histogram
bins = 80
#Number of times the effective radius of the void
Nreff = 8


###################################################################################################
#DIRECT METHOD USING PYTHON
###################################################################################################

##==================================================================================================
##			COMPUTING GEOMETRIC CENTER OF VOIDS
##==================================================================================================

#print simulation

#def Reff(X):
    #return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

##Loading the file with all the information about each region
#voids = np.transpose( np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
#(foldglobal, simulation, web, N_sec, void_scheme, config )))

##Loading centres of each void
#GC = np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/GC.dat"%\
#(foldglobal, simulation, web, N_sec, void_scheme, config ))

##Sweeping throughout all regions
#for i_void in xrange(4690, len(voids[0])):
    #sys.stdout.write( " In region:\t%d\r" %(int(i_void)) )
    #sys.stdout.flush()
    
    ##Number of cells
    #N_data = int(voids[1, i_void -1 ])
    ##Effective radius
    #reff = Reff( np.log10(N_data) )
    ##Geometric center
    #cgc = GC[ i_void-1, 4: ]

    ##Loading cells of the current void
    #Rdis, rvel = Void_Velocity( "%s/%s/%s/%d/M"%\
    #(foldglobal, simulation, "Vweb", N_sec), "%s/%s/%s/%d/P"%\
    #(foldglobal, simulation, "Vweb", N_sec), cgc[0], cgc[1], cgc[2], int(Nreff*reff) )
    
    ##Radial Histogram
    #vel_rad = np.zeros( bins )
    ##rbins = np.linspace( 0.99, Nreff*reff, bins+1 )
    #rbins = 10**np.linspace( np.log10(0.99), np.log10(Nreff*reff), bins+1 )

    ##print i_void, reff
    #for i in xrange( bins ):
	#vel_rad[i] = np.mean( rvel[ (Rdis>rbins[i])*(Rdis<=rbins[i+1]) ] )
    
    #radius = rbins[:-1]
    #np.savetxt( '%svoids_density_%s/%s/void_%d_VR.dat'%\
    #(data_figures_fold,void_scheme,web,i_void-1), \
    #np.transpose([radius[np.isnan(vel_rad)==False], \
    #vel_rad[np.isnan(vel_rad)==False]]), fmt = "%1.5e" )
    
###################################################################################################
#DIRECT METHOD USING C
###################################################################################################
filename_m = "%s/%s/%s/%d/M"%(foldglobal, simulation, "Vweb", N_sec)
filename_p = "%s/%s/%s/%d/P"%(foldglobal, simulation, "Vweb", N_sec)
out_folder = "%svoids_density_%s/%s"%(data_figures_fold,void_scheme,web)
indexes = "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%(foldglobal, simulation, web, N_sec, void_scheme, config )
CM = "%s/%s/%s/%d/voids%s/voids_%s/DC.dat"%(foldglobal, simulation, web, N_sec, void_scheme, config )

os.system( "rm Void_Velocity_All.out" )
os.system( "make compile" )
os.system( "./Void_Velocity_All.out %s %s %s %s %s %d %d"%( filename_m, filename_p, out_folder, indexes, CM, bins, Nreff ) )