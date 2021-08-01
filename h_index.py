import itertools, threading, time, sys
from scholarly import scholarly, ProxyGenerator
from fp.fp import FreeProxy

#proxy config
do_proxy = False
max_proxy_tries = 3

#input
author_name = input("Enter Researcher Name: ")

done_loading = False
def loading_animation():
    print(f"Begining h-index calculation for {author_name}. Searching the database may take a while, please be patient")
    for i in itertools.cycle(['|', '/', '-', '\\']):
        if done_loading:
            break
        print(i, end='\r')
        time.sleep(0.2)
    
t_anim = threading.Thread(target=loading_animation)
try:
    t_anim.start()
except:
    done_loading = True
    sys.exit()

print("getting proxy...")

proxy = None
proxy_tries = 0
while proxy == None:
    try:
        proxy = FreeProxy().get()[7:]
    except:
        pass
    proxy_tries += 1

    if proxy_tries >= max_proxy_tries and proxy == None:
        done_loading = True
        print("Error: Cannot resolve proxy")
        sys.exit()

pg = ProxyGenerator()
pg.SingleProxy(http=proxy)

if do_proxy:
    scholarly.use_proxy(pg)
else:
    scholarly.use_proxy(None)

print("searching G-Scholar database...")
try:
    query = scholarly.search_pubs(f"author:\"{author_name}\"")
except:
    print("Query Failed, Exit Code 1")
    done_loading = True
    sys.exit()
author_cits = [q['num_citations'] for q in query]

def calc_h_index(citations):
    cit = sorted(citations, reverse=True)
    h_idx = 0

    for i in range(len(cit)):
        if cit[i] >= i:
            h_idx = i
        else:
            return h_idx
    return 0

print("computing h-index...")
h_idx = calc_h_index(author_cits)
done_loading = True

print(f"H-index of {author_name} is {h_idx}")

if h_idx == 0:
    print("No h-index found.")