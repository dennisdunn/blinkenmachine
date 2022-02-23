import picounicorn, utime, urandom

picounicorn.init()

while True:
    x = urandom.randint(0,15)
    y = urandom.randint(0,6)
    r = urandom.randint(0,255)
    g = urandom.randint(0,255)
    b = urandom.randint(0,255)
    print(x,y,r,g,b)
    picounicorn.set_pixel(x,y,r,g,b)
    utime.sleep(0.01)