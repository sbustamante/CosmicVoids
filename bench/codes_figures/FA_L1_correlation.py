#FA_L1_correlation.py
#
#This code plots the correlation between the fractional anisotropy and the eigenvalue L1 of each 
#web scheme
#Usage: FA_L1_correlation.py <show(0) or save(1)>
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
#Web Scheme
webs = ['Tweb', 'Vweb']
#Colors and labels
colors = [ 'red', 'blue' ]
#Linestyles
linestyles = ["-", "--"]

#==================================================================================================
#Typical halo mass for each environment
#==================================================================================================
#Colors
plt.figure( figsize=(5.8,5) )

i_web = 0
for web in webs:
    #Loading files with quartiles
    quartiles = np.loadtxt( '%sFA_L1_%s.dat'%(data_figures_fold,web) )

    #Quartiles regions-------
    plt.fill_between( quartiles[:,0], quartiles[:,1], quartiles[:,3], color = colors[i_web], alpha = 0.2 )
    plt.plot( quartiles[:,0], quartiles[:,1], color = colors[i_web], linewidth = 1, linestyle = linestyles[i_web] )
    plt.plot( quartiles[:,0], quartiles[:,3], color = colors[i_web], linewidth = 1, linestyle = linestyles[i_web] )

    #Medians-----------------
    plt.plot( quartiles[:,0], quartiles[:,2], color = colors[i_web], linewidth = 3, label = web, \
    linestyle = linestyles[i_web] )
    
    plt.grid(1)
    plt.ylabel( 'FA', fontsize = 12 )
    plt.xlabel( '$\lambda_{1}$', fontsize = 12)
    plt.xlim( (-0.3,2) )
    plt.ylim( (0,1) )
    plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
    #Lambda_th line
    if web == 'Tweb':
	lamb_opt = 0.265
	plt.text( lamb_opt + 0.03, 0.6, '$\lambda^%s_{opt}$=%1.3f'%(web[0],lamb_opt), fontsize = 12,\
	color=colors[i_web], rotation=90 )
    elif web == 'Vweb':
	lamb_opt = 0.175
	plt.text( lamb_opt - 0.12, 0.6, '$\lambda^%s_{opt}$=%1.3f'%(web[0],lamb_opt), fontsize = 12,\
	color=colors[i_web], rotation=90 )
    plt.plot( [lamb_opt,lamb_opt], [0,1], linestyle = '-', color = colors[i_web], linewidth = 2 )
    
    i_web += 1

plt.plot( [-0.3,2], [0.95,0.95], '-', color='black', linewidth=2 )
plt.text( -0.3, 0.962, 'FA$_{th}$=0.95', fontsize = 12, color="black" )

if sys.argv[1] == '1':
    plt.savefig( '%sFA_L1.pdf'%(figures_fold) )
else:
    plt.show()