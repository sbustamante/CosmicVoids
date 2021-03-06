#cosmicweb_volume_fraction.py
#
#This code computes the volume fraction for both web schemes for some L_th values
#Usage cosmicweb_volume_fraction.py <Vweb or Tweb> <show(0) or save(1)>
#
#by: Sebastian Bustamante

execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
simulation = "BOLSHOI/"
#Labels of graphs
labels = "BOLSHOI"
#Box lenght
Box_L = 250
#Number of sections
N_sec = 256

#Web scheme
web = sys.argv[1]

#Values to evaluate lambda_th
if web == 'Tweb':
    Lambda_opt = 0.265
if web == 'Vweb':
    Lambda_opt = 0.175
#Smooth parameter
smooth = '_s1'

#N Lambda
N_l = 100
#Lambdas Extremes
L_min = -0.3
L_max = 1
L_max += (L_max-L_min)/(1.0*N_l+1)
#Colors
colors = ["navy", "yellowgreen", "orangered", "c"]

#==================================================================================================
#			PLOTING VOLUME FRACTION OF EACH REGION
#=================================================================================================='''
plt.figure( figsize=(5.8,5) )

#Loading Density filename
delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,simulation,N_sec,smooth)
#Loading Vweb filename
eig_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,simulation,web,N_sec,smooth)

#Making counts of each region
regs = Counts( eig_filename, delta_filename, L_min, L_max, N_l )

#Fraction of Voids
plt.fill_between( regs[0], regs[5]/regs[9], color = colors[0] )
plt.plot( regs[0], regs[5]/regs[9], color = colors[0], label = "voids", linewidth=2.0 )
#Fraction of Sheets
plt.fill_between( regs[0], (regs[5]+regs[6])/regs[9], regs[5]/regs[9], color = colors[1] )
plt.plot( regs[0], (regs[5]+regs[6])/regs[9], color = colors[1], label = "sheets", linewidth=2.0 )
#Fraction of Filaments
plt.fill_between( regs[0], (regs[5]+regs[6]+regs[7])/regs[9], (regs[5]+regs[6])/regs[9], color = colors[2] )
plt.plot( regs[0], (regs[5]+regs[6]+regs[7])/regs[9], color = colors[2], label = "filaments", linewidth=2.0 )
#Fraction of Knots
plt.fill_between( regs[0], 1.0, (regs[5]+regs[6]+regs[7])/regs[9], color = colors[3] )
plt.plot( regs[0], regs[0]*0.0, color = colors[3], label = "knots", linewidth=2.0 )

plt.xlim( L_min, 1.0 )
plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
plt.title( "%s"%(web) )
plt.xlabel( "$\lambda_{th}$" )
plt.ylabel( "Volume fraction" )
#Lambda_th line

plt.text( Lambda_opt + 0.03, 0.3, '$\lambda^%s_{opt}$=%1.3f'%(web[0],Lambda_opt), fontsize = 12,\
color = "white", rotation = 90 )
plt.plot( [Lambda_opt,Lambda_opt], [0, 1.0], linestyle = '-', color = "black", linewidth = 2.5 )

#plt.subplots_adjust(  )
if sys.argv[2] == '1':
    plt.savefig( '%scosmicweb_volume_%s.pdf'%(figures_fold, web ) )
else:
    plt.show()