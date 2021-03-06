#void_intertia_tensor.p
#
#This code computes distributions of the eigenvalues of the blackuced intertia tensor of each void 
#region found by each void scheme. The eigenvalues were sorted such as Lambda1 < Lambda2 < Lambda3.
#Here it will be calculated non-integrated and normed distributions of Lambda1/Lambda2 and 
#Lambda1/Lambda3 in order to determinate the shape of void regions.
#Usage void_intertia_tensor.py <Vweb or Tweb> <FAG or DLG> <order MF and BR> <show(0) or save(1)>
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
#Web Scheme
web = sys.argv[1]
#Void parameters ( Nth-order median filtering,  Boolean for boundary removals )
config = sys.argv[3]
#Void finder scheme
void_scheme = sys.argv[2]
#Nbins of each histogram
Nbins = 20
Nbins2D = 10
#Minim radius for a void
rmin = 0

prop1_hist = 5
prop2_hist = 5

#==================================================================================================
#			COMPUTING EIGENVALUES AND BUILDING THE INERTIA TENSOR
#==================================================================================================

#Effective radius function
def r_eff(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

#no labels
nullfmt = NullFormatter()

#definitions for the axes
left, width = 0.1, 0.65
bottom_v, height = 0.1, 0.65
bottom_h = left_h = left+width+0.02

rect_hist2D = [left, bottom_v, width, height]
rect_histx = [left, bottom_h, 1.335*width, 0.2]
rect_histy = [left_h, bottom_v, 0.2, height]

#start with a rectangular Figure
plt.figure(1, figsize=(8,8))

axHist2D = plt.axes(rect_hist2D)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

#no labels
axHistx.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)


print simulation

#Loading intertia eigenvalues
eigen = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/eigen.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config )))
#Loading catalog of voids
catalog = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%s/void_regions.dat"%\
(foldglobal, simulation, web, N_sec, void_scheme, config )))
catalog = catalog[:,catalog[1]>=catalog[1,len(eigen[0])-1]]
#Histogram of voids
Hist_lambd  = np.transpose(np.histogram2d( eigen[0]/eigen[1], eigen[1]/eigen[2], 
bins = Nbins2D, normed = False, range = ((0,1),(0,1))  )[0][::,::-1])

#2D histogram
#map2d = axHist2D.imshow( Hist_lambd[::,::], interpolation='nearest', aspect = 'auto',
#cmap = 'binary', extent = (0,1,0,1) )	
#Scatter
reff = r_eff(np.log10(catalog[1]))
scatter = axHist2D.scatter( eigen[0,reff>rmin]/eigen[1,reff>rmin], eigen[1,reff>rmin]/eigen[2,reff>rmin], 
c = np.log10(reff[reff>rmin]), s=50, marker='.',linewidth=0.01, cmap='jet', vmin = 0.1, vmax = 1.2 )

#Create the colorbar
axc, kw = matplotlib.colorbar.make_axes( axHistx, orientation = "vertical", shrink=1., pad=.1, aspect=10 )
cb = matplotlib.colorbar.Colorbar( axc, scatter, orientation = "vertical" )
cb.set_label( "$r_{eff}$ [$h^{-1}$ Mpc]", labelpad=-70, fontsize=14 )
#Ticks
ticks = np.linspace( 0.1,1.2,10 )
cb.set_ticks( ticks )
cb.set_ticklabels( ['{0:3.1f}'.format(10**t) for t in ticks] )
#Set the colorbar
scatter.colorbar = cb

#Countorn
axHist2D.contour( Hist_lambd[::-1,::], 7, aspect = 'auto', zorder=2,
extent = (0,1,0,1),linewidths=0.5, interpolation = 'gaussian', colors="black" )

#Histogram X
histx = np.histogram( eigen[0]/eigen[1], bins=Nbins, normed=True, range=(0,1) )
axHistx.bar( histx[1][:-1], histx[0], width = 1.00/Nbins, linewidth=2.0, color="gray" )
#Histogram Y
histy = np.histogram( eigen[1]/eigen[2], bins=Nbins, normed=True, range=(0,1) )
axHisty.barh( histy[1][:-1], histy[0], height = 1.00/Nbins, linewidth=2.0, color="gray" )

#Number of anisotropic voids
N_tot = len(eigen[0])*1.0
t1t2 = eigen[0]/eigen[1]
t2t3 = eigen[1]/eigen[2]
#Number of anisotropic voids
print "Number of voids: ", N_tot
print "Anisotropic voids: ", np.sum( (t1t2<0.7)*(t2t3<0.7) )/N_tot
print "Isotropic voids: ", np.sum( (t1t2>=0.7)*(t2t3>=0.7) )/N_tot
print "Pancake voids: ", np.sum( (t1t2<0.7)*(t2t3>=0.7) )/N_tot
print "Filament voids: ", np.sum( (t1t2>=0.7)*(t2t3<0.7) )/N_tot

axHistx.set_xlim( axHist2D.get_xlim() )
axHistx.set_xticks( np.linspace( 0,1,Nbins+1 ) )
axHistx.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHistx.set_ylabel( "Normed distribution" )
yticks = np.linspace( 0, np.max(histx[0]), prop1_hist+1 )
axHistx.set_yticks( yticks )
axHistx.set_yticklabels( ['{0:1.1f}'.format(yt) for yt in yticks] )
axHistx.set_xlim( (0,1) )

axHisty.set_ylim( axHist2D.get_ylim() )
axHisty.set_yticks( np.linspace( 0,1,Nbins+1 ) )
axHisty.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHisty.set_xlabel( "Normed distribution" )
xticks = np.linspace( 0, np.max(histy[0]), prop2_hist+1 )
axHisty.set_xticks( xticks )
axHisty.set_xticklabels( ['{0:1.1f}'.format(xt) for xt in xticks], rotation=-90 )
axHisty.set_ylim( (0,1) )
    
axHist2D.set_ylim( (0,1) )
axHist2D.set_xlim( (0,1) )

axHist2D.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHist2D.set_xticks( np.linspace( 0,1,Nbins/2.+1 ) )
axHist2D.set_yticks( np.linspace( 0,1,Nbins/2.+1 ) )
axHist2D.set_xlabel( "$\\tau_1/\\tau_2$", fontsize=15 )
axHist2D.set_ylabel( "$\\tau_2/\\tau_3$", fontsize=15 )

axHist2D.hlines( 0.7, 0.0, 0.7, linestyle="--", color="black", linewidth=2.5 )
axHist2D.text( 0.35, 0.81, "Pancake\nvoids", fontweight="bold", color="black",\
fontsize=15, horizontalalignment="center" )

axHist2D.vlines( 0.7, 0.0, 0.7, linestyle="--", color="black", linewidth=2.5 )
axHist2D.text( 0.85, 0.3, "Filamentary\nvoids", fontweight="bold", color="black",\
fontsize=15, horizontalalignment="center" )

axHist2D.hlines( 0.7, 0.7, 1.0, linestyle="--", color="black", linewidth=2.5 )
axHist2D.vlines( 0.7, 0.7, 1.0, linestyle="--", color="black", linewidth=2.5 )
axHist2D.text( 0.85, 0.81, "Isotropic\nvoids", fontweight="bold", color="black",\
fontsize=15, horizontalalignment="center" )
axHist2D.text( 0.35, 0.3, "Anisotropic\nvoids", fontweight="bold", color="black",\
fontsize=15, horizontalalignment="center" )

axHist2D.text( 0.01, 0.01, "%s FA-WT"%(web), fontweight="bold", color="black", fontsize=15 )
#axHist2D.text( 0.01, 0.01, "Density-WT", fontweight="bold", color="black", fontsize=15 )

if sys.argv[4] == '1':
    plt.savefig( '%svoids_inertia_tensor_%s_%s.pdf'%(figures_fold,web,void_scheme) )
else:
    plt.show()