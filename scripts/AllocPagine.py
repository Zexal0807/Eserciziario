def make_step(page, frames, fault, replaced=None):
    return {
        "page": page,
        "frames": frames.copy(),
        "fault": fault,
        "replaced": replaced
    }


def pick_tiebreak_by_oldest_arrival(frames, arrival_time, candidates):
    return min(candidates, key=lambda p: arrival_time[p])


def simulate_fifo(pages, page_size):
    frames = []
    queue_idx = 0
    steps = []

    for page in pages:
        if page in frames:
            steps.append(make_step(page, frames, False))
            continue

        replaced = None
        if len(frames) < page_size:
            frames.append(page)
        else:
            replaced = frames[queue_idx]
            frames[queue_idx] = page
            queue_idx = (queue_idx + 1) % page_size

        steps.append(make_step(page, frames, True, replaced))

    return steps


def simulate_lru(pages, page_size):
    frames = []
    last_used = {}
    steps = []

    for t, page in enumerate(pages):
        if page in frames:
            last_used[page] = t
            steps.append(make_step(page, frames, False))
            continue

        replaced = None
        if len(frames) < page_size:
            frames.append(page)
        else:
            victim = min(frames, key=lambda p: last_used[p])
            replaced = victim
            idx = frames.index(victim)
            frames[idx] = page

        last_used[page] = t
        steps.append(make_step(page, frames, True, replaced))

    return steps


def simulate_lfu(pages, page_size):
    frames = []
    freq = {}
    arrival_time = {}
    steps = []

    for t, page in enumerate(pages):
        freq[page] = freq.get(page, 0) + 1

        if page in frames:
            steps.append(make_step(page, frames, False))
            continue

        replaced = None
        if len(frames) < page_size:
            frames.append(page)
            arrival_time[page] = t
        else:
            min_freq = min(freq[p] for p in frames)
            candidates = [p for p in frames if freq[p] == min_freq]
            victim = pick_tiebreak_by_oldest_arrival(frames, arrival_time, candidates)

            replaced = victim
            idx = frames.index(victim)
            del arrival_time[victim]

            frames[idx] = page
            arrival_time[page] = t

        steps.append(make_step(page, frames, True, replaced))

    return steps


def simulate_mfu(pages, page_size):
    frames = []
    freq = {}
    arrival_time = {}
    steps = []

    for t, page in enumerate(pages):
        freq[page] = freq.get(page, 0) + 1

        if page in frames:
            steps.append(make_step(page, frames, False))
            continue

        replaced = None
        if len(frames) < page_size:
            frames.append(page)
            arrival_time[page] = t
        else:
            max_freq = max(freq[p] for p in frames)
            candidates = [p for p in frames if freq[p] == max_freq]
            victim = pick_tiebreak_by_oldest_arrival(frames, arrival_time, candidates)

            replaced = victim
            idx = frames.index(victim)
            del arrival_time[victim]

            frames[idx] = page
            arrival_time[page] = t

        steps.append(make_step(page, frames, True, replaced))

    return steps


def simulate_opt(pages, page_size):
    frames = []
    steps = []

    for i, page in enumerate(pages):
        if page in frames:
            steps.append(make_step(page, frames, False))
            continue

        replaced = None
        if len(frames) < page_size:
            frames.append(page)
        else:
            future = pages[i + 1:]

            def next_use(p):
                return future.index(p) if p in future else float("inf")

            victim = max(frames, key=next_use)
            replaced = victim
            idx = frames.index(victim)
            frames[idx] = page

        steps.append(make_step(page, frames, True, replaced))

    return steps


def eval_steps(pages, alg, page_size):
    if alg == "FIFO":
        return simulate_fifo(pages, page_size)
    if alg == "LRU":
        return simulate_lru(pages, page_size)
    if alg == "LFU":
        return simulate_lfu(pages, page_size)
    if alg == "MFU":
        return simulate_mfu(pages, page_size)
    if alg == "OPT":
        return simulate_opt(pages, page_size)
    return []

def generateLatex(params):
    p = params.split(";")

    alg, page_size, sol = p[0].split(",")
    page_size = int(page_size)

    pages = [int(x) for x in p[1].split(",")]

    res = []

    if sol == "T":
        res.append("{")
        res.append("\\vspace{0.25cm}")
        res.append("\\begin{tabular}{" + "|c" * len(pages) + "|}")
        res.append("\\hline")
        res.append(" & ".join([str(x) for x in pages]) + "\\\\")
        res.append("\\hline")
        res.append("\\end{tabular}")
        res.append("}")

    if sol == "S":
        steps = eval_steps(pages, alg, page_size)

        res.append("{")
        res.append("\\vspace{0.25cm}")
        res.append("\\textbf{" + alg + "}")
        res.append("\\vspace{0.15cm}")
        res.append("")
        res.append("\\begin{tabular}{" + "|c" * (len(pages)+1) + "|}")
        res.append("\\hline")
        res.append(" & ".join([str(x) for x in pages]) + "& \\\\")
        res.append("\\hline")
        res.append("\\hline")
        for i in range(page_size):
            res.append(" &" + " & ".join([str(x['frames'][i]) if len(x['frames']) > i else "" for x in steps]) + "\\\\")
        res.append("\\hline")
        res.append(" & ".join(["\\multicolumn{1}{c}{" + ("F" if x['fault'] else "") + "}" for x in steps]))
        res.append("\\end{tabular}")
        res.append("}")
        res.append("")

    return "\n".join(res)


def main(params):
    print(generateLatex(params))


# PAGE REPLACEMENTE
#
# ALG [FIFO,LRU,LFU,MFU,OPT],PAGE_SIZE,TESTO/SOLUZIONE (T/S);
# PAGE1,PAGE2,....PAGEn

# main("""FIFO,3,S;
# 1,2,3,5,6,3,4,5,6
# """)

import sys

# ha un parametro
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(sys.argv[1])