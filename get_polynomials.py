from libs.special_graphs import get_vampire
from libs.chromaticpol import get_all_chromatic_polynomials

for i in range(10):
    out = get_vampire(i)

    file = open(f"polynomials/vampire{i+1}.txt", 'w')
    print(f"Finding polynomials for vampire {i+1}, graph has {len(out.edges) } edges")
    polys = get_all_chromatic_polynomials(out, NEWMODE=False)
    for poly in polys:
        file.write(str(poly)+'\n')
    file.close()

    out.save()