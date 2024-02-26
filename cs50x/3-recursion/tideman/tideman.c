#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void sort_pairs_recursive(int num);
void lock_pairs(void);
bool starts_cycle(int cycle_start, int loser);
void print_winner(void);
bool has_lost(int num);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j ++)
        {
            preferences[ranks[i]][ranks[j]] += 1;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (i != j)
            {
                if (preferences[i][j] > preferences[j][i])
                {
                    pairs[pair_count].winner = i;
                    pairs[pair_count].loser = j;
                    pair_count += 1;
                }
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    sort_pairs_recursive(0);
    return;
}

void sort_pairs_recursive(int num)
{
    int highest_margin = 0;
    int position;

    for (int i = num; i < pair_count; i++)
    {
        int difference = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
        if (!highest_margin || difference > highest_margin)
        {
            highest_margin = difference;
            position = i;
        }
    }
    if (position != num)
    {
        pair biggest_winner = pairs[position];
        pairs[position] = pairs[num];
        pairs[num] = biggest_winner;
    }
    if (num < pair_count - 1)
    {
        sort_pairs_recursive(num + 1);
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i ++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;

        if (!starts_cycle(winner, loser))
        {
            // printf("lock pair [winner][loser] [%i][%i]\n", winner, loser);
            locked[winner][loser] = true;
        }
    }
}

bool starts_cycle(int cycle_start, int loser)
{
    // printf("makes circle cycle start; %i, loser: %i\n", cycle_start, loser);
    // Check if loser has won against original winner
    if (loser == cycle_start)
    {
        return true;
    }
    for (int i = 0; i < candidate_count; i ++)
    {
        // printf("for loop [loser][i]: [%i][%i]\n", loser, i);
        // Check if loser has won. If not, return false.
        if (locked[loser][i])
        {
            // printf("loser has won against i, [loser][i]: [%i][%i]\n", loser, i);
            //  If loser has won, check
            if (starts_cycle(cycle_start, i))
            {
                // Makes a circle;
                return true;
            }
        }
    }
    return false;
}

// Print the winner of the election
void print_winner(void)
{
    // Kijken voor welk getal i nooit waar is locked[j][i]
    for (int i = 0; i < pair_count; i++)
    {
        if (!has_lost(i))
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
}

bool has_lost(int num)
{
    for (int j = 0; j < candidate_count; j++)
    {
        if (locked[j][num])
        {
            return true;
        }
    }
    return false;
}