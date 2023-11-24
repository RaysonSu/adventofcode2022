# for type annotations on python 3.10
from __future__ import annotations

# for efficency
import multiprocessing


class State:
    def __init__(
        self: State,
        bots_built: int = 0x1,
        # the number of each bots build stored as a 32 bit integer, with each type of bot taking up 8 bits,
        # e.g.  0x01234567 would represent 0x01 geode robot, 0x23 obsidian robots, 0x45 clay robots, and 0x67 ore robots.

        resources: int = 0x0,
        # does the same trick as above, but with resource count instead of bot count.

        time: int = 32,
        # minutes remaining.

        blueprint: int = 0x0,

        # the blueprint stored as a 128 bit integer, where each recipe takes 32 bits,
        # e.g. 0x00040008 00000802 00000009 00000001 would represent a blueprint of
        # geode robot recipe: 0x00 geodes, 0x04 obsidian, 0x00 clay, 0x08 ore
        # obsidian robot recipe: 0x08 clay, 0x02 ore
        # etc.

        cheap: list[int] = [255, 255, 255, 255],
        # a list of the maximum bot costs for optimisation
        # e.g. [2, 3, 4, 255] would represent that
        # all robots execpt ore bots cost less than 2 ores
        # all robots except clay bots cost less than 3 clay
        # all robots except obsidian bots cost less than 4 obsidian
        # and that there is no cap on geode robots

        times: list[int] = 0x0
        # caches the remaining time required to build a robot
        # stores it similarly to the bots_built and resources parameter
    ) -> None:
        # assigning stuff
        self.bots_built: int = bots_built
        self.resources: int = resources
        self.time: int = time
        self.blueprint: int = blueprint
        self.cheap: list[int] = cheap
        self.build_times: int = times

    def get_actions(self: State) -> list[int]:
        # the actions we can take, e.g.
        # [0, 2] would be build an ore bot (0) and build an obsidian bot (2)
        ret: list = []

        for bot in range(4):
            # the start of bit magic!
            # the first condition checks if enough bots are built for that type of bot
            # e.g. to check for the clay bot, we want to know the number of clay bots we have
            # they are stored as these bits in the self.bots_built variable e.g. 0x????04??
            # first bot << 3 determines the start of the amount, in this case 8
            # which means that 0x????04?? >> 8 = 0x????04
            # now we bitwise and with 0xff so
            #     0x????04
            # and 0x0000ff
            #   = 0x000004 = 0x04
            # so we have 0x04 clay bots in this example
            # the second condition just checks if we can build the bot in the time we have
            if (self.bots_built >> (bot << 3) & 0xff) < self.cheap[bot] and \
                    (self.get_build_time(bot) + 1) <= self.time:
                ret.append(bot)

        try:
            # small hueristic to make it faster, where it prevents building an ore robot when you can build a geode robot.
            m_ret: int = max(ret) - 2

            ret = [i for i in ret if i >= m_ret]
            return ret
        except:  # try/except is required so that we don't run into issues with taking max of an empty list
            return []

    def get_build_time(
        self: State,
        n: int  # bot tier (0 = ore, 1 = clay, etc.)
    ) -> int:
        ret = 0  # time to build the robot

        # this extracts the correct blueprint to use for this bot
        blueprint: int = self.blueprint >> (n << 5) & 0xffffffff

        # loops over each potential resouce requirement with bit masking, see example above
        # only check for the first 3, as geodes aren't spent
        for mask in [0xff, 0xff00, 0xff0000]:

            # the rate that we gain the resouces, no bit shifting is required as we will perform a division later
            gain: int = self.bots_built & mask

            # the current amount of the resouce we have
            curr: int = self.resources & mask

            # the amount of the resouce thr blueprints require
            cost: int = blueprint & mask

            if not cost:  # if it doesn't require a resouce, then skip it
                continue

            if not gain:  # if we have no production, then we will never be able to afford it, so return 0xff
                # this will set the relavent byte to 0xff, and stores it for later
                self.build_times |= 0xff << (n << 3)
                return 255

            # performs a ceiling division, see: https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
            ret = max(ret, -((cost - curr) // -gain))

        # this overwrites the previous value
        # e.g. the clay bot will take 5 minutes
        # so we want to write 0x05 into the 2nd position
        # we start by creating a mask 0xff
        # shift it left by 8 bits (since that's where clay is stored) to get 0xff00
        # bitwise nots it so we set 0's in the correct positions to get a mask of 0xffff00ff
        # bitwise ands self.build_time with the mask to set the bits to 0
        #     0x????????
        # and 0xffff00ff
        #   = 0x????00??
        # finishes by writing the value 0x05 into the bits we've just zeroed
        #     0x????00??
        #  or 0x00000500
        #   = 0x????05??
        self.build_times &= ~(0xff << (n << 3))
        self.build_times |= ret << (n << 3)
        return ret

    def do_action(self: State, action: int) -> State:
        # uses bitmasking with the stored build times to figure out how many minutes to skip forward
        time_steps: int = 1 + (self.build_times >> (action << 3)) & 0xff

        self.time -= time_steps

        # extracts the blueprint needed
        blue: int = (self.blueprint >> (action << 5)) & 0xffffffff

        # using ints allows for gaining/losing of resouces to be done more efficently compared to a for loop
        self.resources += self.bots_built * time_steps - blue
        self.bots_built += 1 << (action << 3)

        # resets the build_times because they have changed, they will be recomputed before getting here again
        self.build_times = 0x0

        return self

    # equal to maximum possible score form this state - minimum possible score
    def extra_possible_score(self) -> int:
        return (self.time - 1) * self.time >> 1

    # assumes you do nothing for the rest of the time
    def minimum_possible_score(self) -> int:
        return (self.resources >> 24) + (self.bots_built >> 24) * self.time

    def copy(self) -> State:
        return State(self.bots_built, self.resources, self.time, self.blueprint, self.cheap, self.build_times)


def parse_inp(F: list[str]) -> list[int]:
    ret = []
    for blueprint in F:
        # generates a list with the numbers in each blueprint
        p: list[int] = [
            int(number)
            for number
            in "".join(
                char
                for char
                in blueprint
                if char.isnumeric() or char == " "
            ).split(" ")
            if number != ""]

        # calculates the blueprint value
        ret.append(
            p[1]
            + (p[2] << 32)
            + (p[3] << 64) + (p[4] << 72)
            + (p[5] << 96) + (p[6] << 112)
        )

    return ret[:3]  # only cares about the first 3 blueprints


# a crappy bfs implementation with pruning (might be dfs though)
def deal_with_blueprint(blueprint: int) -> int:
    cheap: list[int] = [max((blueprint >> 32) & 0xff, (blueprint >> 64) & 0xff, (blueprint >> 96) & 0xff),
                        (blueprint >> 72) & 0xff,
                        (blueprint >> 112) & 0xff,
                        0xff]

    # initial state
    states: list[State] = [State(blueprint=blueprint, cheap=cheap)]

    # only stores the score of the best state, because we don't care how you got that score, we only care that you've found a way to get that score
    best_min: int = 0

    while states:
        working: State = states.pop(0)

        for action in working.get_actions():
            new: State = working.copy().do_action(action)

            mscore: int = new.minimum_possible_score()
            best_min: int = max(best_min, mscore)

            bscore: int = new.extra_possible_score()
            # only append if it's (potentially) possible to beat the current best score
            if best_min <= bscore + mscore:
                states.append(new)

    return best_min


def main() -> None:
    file_location: str = "python/Advent of Code/2022/Day 19/input.txt"
    blueprints: list[int] = parse_inp(open(file_location, "r"))
    ret: int = 1

    # because each blueprint is independent of each other, we use multiprocessing for parallel computation
    with multiprocessing.Pool(len(blueprints)) as p:
        for result in p.map(deal_with_blueprint, blueprints):
            ret *= result
    print(ret)


if __name__ == "__main__":
    main()
