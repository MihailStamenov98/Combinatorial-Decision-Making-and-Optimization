import matplotlib.pyplot as plt

def graph(times):
    x=range(len(times[0]))
    for time in times:
        plt.plot(x, time)
  
    plt.xlabel('instances')
    plt.ylabel('time')
    plt.title('Two lines on same graph!')
    plt.legend()
    #plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    plt.show()