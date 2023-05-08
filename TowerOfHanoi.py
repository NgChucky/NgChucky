def move(stacks, source, target):
    new_stacks = stacks
    disk = new_stacks[source].pop(0)
    new_stacks[target].insert(0,disk)
    return new_stacks

def solver(start, source, target, moves):
    if start[source] == 1:
        start[source] -= 1
        start[target] += 1
        moves.append((source, target))
        return (start, moves)
    else:
        start[source] -= 1
        target = 3 - (source+target)
        start, moves = solver(start, source, target, moves)
        start[source] += 1 
        target = 3 - (source+target)
        start, moves = solver(start, source, target, moves)
        start[target] -= 1
        source = 3 - (source+target)
        start, moves = solver(start, source, target, moves)
        start[target] += 1
        return (start, moves)

def islegal(stacks):
    all_disks = [i for i in range(num_disks)]
    order_correct = all(all(stacks[i][j] < stacks[i][j+1] for j in range(len(stacks[i])-1)) for i in range(len(stacks)))
    disks_in_state = sorted([disk for stack in stacks for disk in stack])
    disks_complete = (disks_in_state == all_disks)
    return (order_correct & disks_complete)

def iscomplete(stacks):
    all_disks = [i for i in range(num_disks)]
    return stacks[target] == all_disks

def run_solution(solver, start, source, target):
    moves = solver(start, source, target, [])[1]
    all_states = [[[],[],[]]]*(len(moves)+1)
    all_disks = [i for i in range(num_disks)]
    all_states[0][source] = all_disks
    for i, m in enumerate(moves):
        try:
            all_states[i+1] = move(all_states[i], m[0], m[1])
        except ValueError:
            all_states.append(None)
    return (all_states, moves)

def check_solution(solver, start, source, target):
    try:
        all_states, moves = run_solution(solver, start, source, target)
        all_legal = all(islegal(s) for s in all_states)
        complete = iscomplete(all_states[-1])
        return (all_legal and complete, moves)
    except ValueError:
        return False

if __name__ == '__main__':
    retry = True
    a = True
    b = True
    c = True
    d = False

    num_disks = 0
    source = int(input("Source peg: "))
    target = int(input("Target peg: "))

    while(retry):
        all_disks = [i for i in range(num_disks)]
        if a:
            try:
                num_disks = int(input("Enter the number of disks to solve for (or 0 to exit): "))
                if num_disks < 0:
                    raise ValueError()
                if not(num_disks):
                    break
                all_disks = [i for i in range(num_disks)]
            except:
                a = False
                b = False
                c = False
                d = True
        if b:
            starting_stacks = [0, 0, 0]
            starting_stacks[source] = num_disks
            correct, moves = check_solution(solver, starting_stacks, source, target)
            if correct:
                print('Moves:', moves)
                if num_disks >= 3:
                    print("Congratulations, your solution works!")
                else:
                    print("Your solution works for the {} disks. Input 8 or more to see if it works for those".format(num_disks))
            else:
                print("The 'solver' function doesn't work yet. Keep working on it!")
        if c:
            try:
                num_disks = int(input("If you want, you can input a different number this time, or input 0 to exit: "))
                if num_disks < 0:
                    raise ValueError()
                if not(num_disks):
                    break
                a = False
                b = True
                c = True
                d = False
            except:
                a = False
                b = False
                c = False
                d = True
        if d:
            try:
                num_disks = int(input("Valid inputs are WHOLE NUMBERS ONLY. Try again or input 0 to exit: "))
                if num_disks < 0:
                    raise ValueError()
                if not(num_disks):
                    break
                a = False
                b = True
                c = True
                d = False
            except:
                a = False
                b = False
                c = False
                d = True