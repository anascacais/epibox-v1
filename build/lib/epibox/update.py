def update():
    global curve, data, ptr, p6

    curve.setData(data[ptr%10])
    

    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted

    ptr += 1
