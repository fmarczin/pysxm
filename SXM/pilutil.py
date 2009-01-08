import Image

standardpal = {
               'grey':(
                 (  0, (  0,   0,   0)), # black
                 (255, (255, 255, 255)), # white
                 ),
               'jet':(
                 (  0, (  0,   0, 131)), # dark blue
                 ( 31, (  0,   0, 255)), # blue
                 ( 95, (  0, 255, 255)), # turqoise
                 (159, (255, 255,   0)), # yellow
                 (223, (255,   0,   0)), # red
                 (255, (128,   0,   0)), # dark red
                 )
               }

def palfrompoints(points):
    pal = []
    
    for n in range(len(points)-1):
        (indi,(ri,gi,bi)) = points[n]
        (indf,(rf,gf,bf)) = points[n+1]
        nind = indf - indi
        (dr,dg,db) = (float(rf - ri)/float(nind), float(gf - gi)/float(nind), float(bf - bi)/float(nind))
        
        for i in range(nind):
            pal.extend((int(round(ri + (dr*i))), int(round(gi + (dg*i))), int(round(bi + (db*i)))))
        
    pal.extend((rf,gf,bf))
    assert len(pal) == 768
    return pal
            
def stdpal(name):
    return palfrompoints(standardpal[name])
