import random


# The old game of Deduction with this fun compare routine.
def compare_numbers(n, g):
    cow_bull = [0, 0]
    n_list = [x for x in str(n)]
    g_list = [x for x in str(g)]
    for i in range(len(n_list)):
        if n_list[i] == g_list[i]:
            cow_bull[1] += 1
            n_list[i] = 'x'
        elif g_list[i] in n_list:
            cow_bull[0] += 1
            n_list[n_list.index(g_list[i])] = 'x'
    return cow_bull


if __name__ == '__main__':
    number = random.randint(1000, 9999)
    playing = True
    guess_count = 0
    print(f'Cheater: {number}')

    while playing:
        guess = input("Four digit number: ")
        if guess.lower == 'exit':
            break
        guess_count += 1
        cow_bull_count = compare_numbers(number, guess)
        print(f'{guess_count}) {cow_bull_count[0]} cows {cow_bull_count[1]} bulls')
        if cow_bull_count[1] == 4:
            print("Correct!")
            break
