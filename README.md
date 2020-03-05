# 538-flipping

A quick solution to a [fivethirtyeight Riddler puzzle](https://fivethirtyeight.com/features/can-you-flip-your-way-to-victory/). Working through the problem by hand didn't seem to get anything concrete so why not make a computer do the dirty work?

## Usage
`./solve.py 10`
`./solve.py 100 -o results.csv`

## Solution
The winrate after 100 flips is **64.0317%**.

## Approach
To figure out the strategy, approach the problem in reverse. It's evident that after the 99th flip, if your total is greater than 2, you're guaranteed to win whichever coin you pick. If your total is 2, pick coin A to guarantee a win. Likewise, if your total is less than -1, you're guaranteed to lose regardless of the last coin flipped. If your total is exactly -1, picking coin B gives a 50% chance at a win and coin A guarantees a loss. Totals of 0 or 1 give a 50% chance of a win regardless of coin choice. That gives us:

| Running Total | Coin Choice   | Winrate   |
| -             | -             | -         |
| ...           | either        | 0%        |
| -1            | B             | 50%       |
| 0             | either        | 50%       |
| 1             | either        | 50%       |
| 2             | A             | 100%      |
| ...           | either        | 100%      |

Now let's go back another step to after the 98th flip. For each starting total, we can work through each permutation of coin choices and flip result to get a new running total for after the 99th flip. We can then reference the above chart to figure out our new winrate:

| Running Total | Coin Choice   | Winrate   |
| -             | -             | -         |
| ...           | either        | 0%        |
| -3            | B             | 25%       |
| -2            | either        | 25%       |
| -1            | B             | 50%       |
| 0             | either        | 50%       |
| 1             | either        | 50%       |
| 2             | A             | 75%       |
| 3             | A             | 100%      |
| ...           | either        | 100%      |

We can keep working backwards, but a strategy emerges: pick coin B for negative totals and pick coin A for totals of 2 or greater. It doesn't seem to matter which coin we pick for totals of 0 or 1, but we'll want to validate that later. For now, let's say our strategy is:

> Pick coin A for positive running totals, coin B otherwise

That kinda makes sense. If we're currently winning, there's no point in trying to win more (sounds like there's a lesson in there for gamers), so we play safe to minimize losses. And if we're currently losing, might as well risk more to try to get out of the hole (maybe not a great lesson for gamblers though).

So now we have a strategy. Let's work out what happens if we play accordingly.

We start at 0, so we flip coin B. Our total is now `-2` or `2`, for a 50% winrate after a single flip.  
Flip again, and possible totals are `[-4, 0, 1, 3]`. Still a 50% winrate.  
Again. `[-6, -2, -2, 2, 0, 2, 2, 4]`. Still 50%. Is all our strategizing for naught and we can't beat this game?  
4th flip. `[-8, -4, -4, 0, -4, 0, 1, 3, -2, 2, 1, 3, 1, 3, 3, 5]`. 56.25%!  

Interesting. So there's a point to this after all. If we draw out the tree of possibilities, we start to see repeats. For example, every `-2` after the 3rd flip branched to `-4` and `0` after the 4th flip. Smells like dynamic programming.

We noticed earlier that only the running total affects the result, not how we got there. As such, we don't need to keep track of every permutation, just frequency of each running total. We can visualize as:

```
                                                                                      Ending Value
Flips |  -20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1   0   1   2   3   4   5   6   7   8   9  10  11
    0 |                                                                                    1
    1 |                                                                            1   0   0   0   1
    2 |                                                                    1   0   0   0   1   1   0   1
    3 |                                                            1   0   0   0   2   0   1   0   3   0   1
    4 |                                                    1   0   0   0   3   0   1   0   2   3   1   4   0   1
    5 |                                            1   0   0   0   4   0   1   0   5   0   4   1   9   1   5   0   1
    6 |                                    1   0   0   0   5   0   1   0   9   0   5   0   6   9   6  14   1   6   0   1
    7 |                            1   0   0   0   6   0   1   0  14   0   6   0  15   0  14   6  29   7  20   1   7   0   1
    8 |                    1   0   0   0   7   0   1   0  20   0   7   0  29   0  20   0  21  29  27  49   8  27   1   8   0   1
    9 |            1   0   0   0   8   0   1   0  27   0   8   0  49   0  27   0  50   0  49  27  99  35  76   9  35   1   9   0   1
   10 |    1   0   0   0   9   0   1   0  35   0   9   0  76   0  35   0  99   0  76   0  77  99 111 175  44 111  10  44   1  10   0   1
```

That looks like a distorted Pascal's triangle. Unfortunately, unlike how every element can be calculated by combinatorics without having to fill in the rest of the triangle, no real patterns seem to show up aside from along the extreme edges. Oh, and this structure translates directly to a memoization structure!

## Results
Results for every flip up to 100 are included in the repo.

[TODO: insert chart]

The results appear to slowly converge around &#8532;. Curiously, they oscillate a bit - each odd-numbered flip has a slightly worse winrate than its previous even-numbered flip.

[TODO: math workup]

Remember that earlier, we we're entirely sure what to do with a running total of 0 or 1, as coin choice didn't seem to matter? We can tweak our script now and see that, in fact, it doesn't matter at all which coin we choose in those cases; the results come out the same.

So the actual optimal strategy is:

> If our running total is 2 or greater, pick coin A. If negative, pick coin B. If 0 or 1, pick whatever  
> (maybe flip a coin to choose which coin to fip. But then which coin do we flip to determine that???)
