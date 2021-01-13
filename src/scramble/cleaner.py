""" removes unnecessary move in the scramble/solution """

def clean_moves(scramble):
    split_scramble = scramble.split()
    seq = 0

    while seq < len(split_scramble):
        try:
            if split_scramble[seq][0] == split_scramble[seq + 1][0]:
                # minus seq by 1 to cancel the +1 if we had to clean a move
                # if first move is normal
                if not is_prime(split_scramble[seq]) and not is_double(split_scramble[seq]):
                    # second move is normal
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        del split_scramble[seq + 1]
                        split_scramble[seq] += "2"

                    # second move is prime
                    elif is_prime(split_scramble[seq + 1]):
                        del split_scramble[seq], split_scramble[seq]

                    # second move is double
                    elif is_double(split_scramble[seq + 1]):
                        del split_scramble[seq + 1]
                        split_scramble[seq] += "'"

                # if first move is prime
                elif is_prime(split_scramble[seq]):
                    # second move is normal
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        del split_scramble[seq], split_scramble[seq]

                    # second move is prime
                    elif is_prime(split_scramble[seq + 1]):
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0] + "2"

                    # second move is double
                    elif is_double(split_scramble[seq + 1]):
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0]


                # if first move is double
                elif is_double(split_scramble[seq]):
                    # second move is normal
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        del split_scramble[seq]
                        split_scramble[seq] = split_scramble[seq][0] + "'"

                    # second move is prime
                    elif is_prime(split_scramble[seq + 1]):
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0]

                    # second move is double
                    elif is_double(split_scramble[seq + 1]):
                        del split_scramble[seq], split_scramble[seq]
                
                # minus seq by 1 to cancel the +1 if we had to clean a move
                seq -= 1
        except IndexError:
            break
        seq += 1

    return " ".join(split_scramble)
def is_double(move):
    try:
        if move[1] == "2":
            return True
        else:
            return False
    except IndexError:
        return False


def is_prime(move):
    try:
        if move[1] == "'":
            return True
        else:
            return False
    except IndexError:
        return False


if __name__ == "__main__":
    ''' # all possible cases
    print(clean_moves("U U D D' U U2"))
    print(clean_moves("U' U D' D' U' U2"))
    print(clean_moves("U2 U D2 D' U2 U2"))

    print("Correct output is")
    print("U2 U'")
    print("D2 U")
    print("U' D")
    '''
    print(clean_moves("B R2 B F2 L2 D D2 F2 D2 L B D U2 D2 D2 R R2 L F2 U2"))