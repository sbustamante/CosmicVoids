#void_volume_regions_compensated.py
#
#This code calculate volume fractions for each void finder scheme and for over and subcompensated
#voids
#Usage void_volume_regions_compensated.py <normal(0) or cumulative(1)> <show(0) or save(1)>
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
#Web Scheme
webs = ['Tweb', 'Vweb', 'DLG'] 
webs = ['Tweb', 'Vweb'] 
labels = ['FA-Tweb', 'FA-Vweb', 'Density']
#Void finder scheme (FAG or FOF)
void_scheme = 'FAG'
#Schemes used for each web
schemes = [ "01","01","01" ]
#Linestyles
linestyles = ["-", "--"]


#Colors
colors = ["red", "blue", "green"]

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

fig = plt.figure( figsize=(5.8,5) )
fig.subplots_adjust( top = 0.9, right = 0.95, left = 0.15, wspace = 0.05, bottom = 0.1 )
ax1 = [fig.add_subplot(1,1,i+1) for i in xrange(1)]
ax2 = [ax1[i].twiny() for i in xrange(1)]

tick_locations = np.linspace(0,16,6)
#Function to build the second axe
def tick_function(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

i_web = 0
for web in webs:
    print simulation, web

    #DENSITY WATERSHED TRANSFORM
    if web == 'DLG':
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
	(foldglobal, simulation, "Tweb", N_sec, web, schemes[i_web] )))
    #FA WATERSHED TRANSFORM    
    else:
	void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
	(foldglobal, simulation, web, N_sec, void_scheme, schemes[i_web] )))
      
    #Loading compensated
    comp = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%s/comp_half.dat"%\
    (foldglobal, simulation, web, N_sec, void_scheme, schemes[i_web] ))

    ranger = (0.6,15)
    bins = 11
    hist1d = np.histogram( tick_function(np.log10(void_regs[1])) , bins=bins, normed=False, range=ranger )
    hist1d_o = np.histogram( tick_function(np.log10(void_regs[1][comp[:,1]==1])) , bins=bins, normed=False, range=ranger )
    hist1d_u = np.histogram( tick_function(np.log10(void_regs[1][comp[:,1]==0])) , bins=bins, normed=False, range=ranger )
    
    #Normal distribution
    if sys.argv[1] == '0':
	distro = hist1d[0]*1.0
	distro_o = hist1d_o[0]*1.0
	distro_u = hist1d_u[0]*1.0
    #Cumulative distribution
    else:
	distro = np.cumsum(hist1d[0][::-1])[::-1]
	distro = distro/(1.0*distro[0])
	
    #Normal Plot
    if sys.argv[1] == '0':	
	#Overcompensated voids
	ax1[0].plot( hist1d_o[1][:-1], distro_o/distro, lw = 1.5, linestyle = linestyles[i_web],\
	color = colors[i_web], label = "%s $C>1$"%(labels[i_web]) )
	
	#Subcompensated voids
	ax1[0].plot( hist1d_u[1][:-1], distro_u/distro, lw = 3.0, linestyle = linestyles[i_web],\
	color = colors[i_web], label = "%s $C<1$"%(labels[i_web]) )
      
    #Cumulative Plot
    else:
	ax1[0].plot( hist1d[1][:-1], distro, linewidth = 2.0, linestyle = linestyles[i_web],\
	#color = colors[i_web], label = "%s (%s-order MF)"%(labels[i_web], schemes[i_web][0]) )
	color = colors[i_web], label = "%s"%(labels[i_web]) )
      
    i_web += 1
    
#Format of plots
for i in range(1):
    #Axe 1
    ax1[i].grid()
    #ax1[i].set_xticks( np.linspace(0,16,30) )
    ax1[i].set_xticks( np.linspace(0,16,6) )
    ax1[i].set_xlim( (0,16) )
    ax1[i].set_ylim( (0,1) )
    #Cumulative distribution
    if sys.argv[1] == '1':
	#ax1[i].set_ylim( (0,1) )
	for hcut in np.linspace(0,1,9+1):
	    ax1[i].hlines( hcut, 0, 16, linestyle="--", color = "black", linewidth=1.0 )
    
    ax1[i].set_ylabel( "Fraction of voids" )
    ax1[i].set_xlabel( "Effective radius [Mpc/$h$]" )
    ax1[i].legend( loc='lower center', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )

    #Axe 2
    ax2[i].set_xlim( (0,4.2) )
    ax2[i].set_xticks( tick_locations )
    tick_label = []
    for tick in tick_locations:
	tick_label.append( "%1.1f"%(0 if tick==0 else np.log10(4*np.pi/3.*(tick)**3)) )
    ax2[i].set_xticklabels( tick_label )
    ax2[i].set_xlabel( "Comoving volume [$\log_{10}($ Mpc $h^{-1} )^{-3}$]" )

if sys.argv[2] == '1':
    plt.savefig( '%svoids_regions_volume_compensated.pdf'%(figures_fold) )
else:
    plt.show()