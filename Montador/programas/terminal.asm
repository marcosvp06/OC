inicio:
    clr r0
    out addr r0
    in data r1
    data r0 1
    out addr r0
    out data r1
    jump inicio