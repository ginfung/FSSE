from xomo import *

class xomol:
    
  def run(self, input):  
    names = ["aa", "sced", "cplx", "site", "resl", "acap", "etat", "rely", 
             "Data", "prec", "pmat", "aexp", "flex", "pcon", "tool", "time",
             "stor", "docu", "b", "plex", "pcap", "kloc", "ltex", "pr", 
             "ruse", "team", "pvol"]
    model = "flight"
    #c = Cocomo("./Problems/XOMO/Data" + "/" + model)
    c = Cocomo(input)
    out = c.xys(verbose = False,olist=True)
    return out

if __name__ == '__main__':
  xomoxo = xomol()
  bounds = {"aa" : (1,6),
            "sced" : (1.00,1.43), 
            "cplx" : (0.73,1.74),
            "site" : (0.80, 1.22),
            "resl" : (1.41,7.07),
            "acap" : (0.71,1.42),
            "etat" : (1,6),
            "rely" : (0.82,1.26),
            "Data" : (0.90,1.28),
            "prec" : (1.24,6.20),
            "pmat" : (1.56,7.80),
            "aexp" : (0.81,1.22),
            "flex" : (1.01,5.07),
            "pcon" : (0.81,1.29),
            "tool" : (0.78,1.17),
            "time" : (1.00,1.63),
            "stor" : (1.00,1.46),
            "docu" : (0.81,1.23), 
            "b" : (3,10),
            "plex" : (0.85,1.19),
            "pcap" : (0.76,1.34),
            "kloc" : (2,1000),
            "ltex" : (0.84,1.20),
            "pr" : (1,6), 
            "ruse" : (0.95,1.24), 
            "team" : (1.01,5.48), 
            "pvol" : (0.87,1.30)} 

  print xomoxo.run(bounds)