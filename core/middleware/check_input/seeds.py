from arguments import arguments


def get_seeds_from_cli() -> list[str]:
    seeds = []
    for seed in arguments.seed:
        print(seed)
        if seed[-1:] == ',':
            seed = seed[:-1]
        seeds.append(seed)
    seeds = list(set(seeds))
    print(f"Seeds for analyse: {' '.join(seeds)}")
    return seeds
