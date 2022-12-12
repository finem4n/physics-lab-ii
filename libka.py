# author Konrad Marciniak

def file_loader(plik):

    # 2 columns file loader, returns lists (not data frames)

    from numpy import delete
    from pandas import read_table

    df = read_table(plik,sep="\s+", skiprows=0, usecols=[0, 1])

    conv_arr = df.values

    x = delete(conv_arr, 1, axis=1)
    y = delete(conv_arr, 0, axis=1)

    x = x.ravel()
    y = y.ravel()

    return x, y

def least_squares(x, y, min, max):
    # without y uncertainity
    N = max - min + 1
    xi = 0
    yi = 0
    xiyi = 0
    xi2 = 0
    
# min inclusive, max exclusive remember
    for i in range(min,max+1):
        xi += x[i]
        yi += y[i]
        xiyi += x[i]*y[i]
        xi2 += x[i]**2
        yaxb += (y[i]-a*x[i]-b)**2

    a = (N*xiyi - xi*yi)/(N*xi2 - xi**2)
    b = (xi2*yi - xiyi*xi)/(N*xi2 - xi**2)

    ua = (N/(N-2)*yaxb/(N*xi2-xi**2))**0.5
    ub = (yaxb*xi2/(N-2)/(N*xi2-xi**2))**0.5

    chi2 = 0

    for i in range(min,max+1):
        chi2+=((y[i]-(a*x[i]+b))**2)/(a*x[i]+b)

    return a, b, ua, ub, chi2

def least_squares_non_b(x, y, min, max, uy):
    # returns a, ua, chi2
    x2u2 = 0
    xyu = 0

    for i in range(min, max+1):
        xyu += x[i]*y[i]/uy[i]**2
        x2u2 += (x[i]/uy[i])**2
    
    a = xyu/x2u2
    ua = (1/x2u2)**0.5

    chi2 = 0

    for i in range(min, max+1):
        chi2 += ((y[i]-a*x[i])/uy[i])**2

    return  a, ua, chi2

def least_squares(x, y, uy, min, max):
    #with y uncertainty
    wi = 0
    wixiyi = 0
    wixi = 0
    wiyi = 0
    wixi2 = 0


# min inclusive, max exclusive remember
    for i in range(min,max+1):
        wi += 1/uy[i]**2
        wixi += x[i]*1/uy[i]**2
        wiyi += y[i]*1/uy[i]**2
        wixiyi += x[i]*y[i]*1/uy[i]**2
        wixi2 += 1/uy[i]**2*x[i]**2

    a = (wi*wixiyi - wixi*wiyi)/(wi*wixi2 -wixi**2)
    b = (wixi2*wiyi - wixiyi*wixi)/(wi*wixi2 - wixi**2)

    ua = (wi/(wi*wixi2-wixi**2))**0.5
    ub = (wixi2/(wi*wixi2-wixi**2))**0.5

    chi2 = 0

    for i in range(min,max+1):
        chi2+=wi*(y[i]-a*x[i]-b)**2

    return a, b, ua, ub, chi2

# uncertainty type B
def typeB(dx, dxe):
    return ((dx**2)/3 + (dxe**2)/3)**0.5