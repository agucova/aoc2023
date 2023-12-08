### A Pluto.jl notebook ###
# v0.19.35

using Markdown
using InteractiveUtils

# ╔═╡ eca36bb7-ee8a-4ee5-b9fd-c2cf18e3dd6c
md"## Part 1"

# ╔═╡ cbc219c1-976a-4304-b83a-d9fe703eb763
input_file = joinpath(dirname(@__DIR__), "inputs", "day6.inp")

# ╔═╡ 4569cd04-6728-4fcb-bc69-5800dd6affe4
times, records = open(input_file) do f
    times_line = readline(f)
    times = parse.(Int, 
		filter(x -> x != "", split(chopprefix(times_line, "Time:"), " "))
	)
	records_line = readline(f)
	records = parse.(Int, 
		filter(x -> x != "", split(chopprefix(records_line, "Distance:"), " "))
	)
	times, records
end

# ╔═╡ 5c1a9ccd-c68e-470b-a1fb-777a5aa952ab
races = zip(times, records)

# ╔═╡ 399197c6-955e-11ee-0cb0-5dd361efe38c
md"""Let $X(u)$ be the total distance covered by the toy boat during a race that where the button was pressed for some time $u$ with $0 \leq u \leq T$, where $T$ is the time when the race ends.

The race is divided into two segments. On $[0, u]$, we have no speed, and no distance is covered. On $(u, T]$, we a speed $u$ mm/ms. Therefore, the distance we cover over the second interval (and the entire race) is $X(u) = u \cdot (T - u)$.

Therefore, given some record $Y$, and $u \in \mathbb{N}$ we want to satisfy:

```math
u \cdot (T - u) > Y
```

We can turn this into quadratic form:

```math
-u^2 + uT - Y > 0
```
Or, equivalently:
```math
u^2 - uT + Y < 0
```

Given this formula, we can easily check for all possible combinations of $u$ through iteration.
"""

# ╔═╡ 9a8fe9e4-8d86-419c-ae19-86fba59e4667
function ways_to_win_race(time::Int, record::Int)
    return sum(Int(u^2 - u * time + record < 0) for u in 0:time-1)
end

# ╔═╡ 15fbd389-3ba2-4ff3-a6a5-39e3b99b5ec2
possible_ways = [ways_to_win_race(time, record) for (time, record) in races]

# ╔═╡ 75c35ba6-4ed5-478d-ae43-b77f79887c49
reduce(*, possible_ways)

# ╔═╡ 2d15432f-52dc-4c8a-bdb4-41f182bb63c3
md"## Part 2"

# ╔═╡ 701563c9-4385-47e6-91a6-0fb75c7c1db9
md"We load the new data:"

# ╔═╡ 63d373fc-b90f-46f3-97ac-b5ffb12b73eb
time, record = open(input_file) do f
    time_line = readline(f)
    time = parse(Int, String(filter(isdigit, (collect.(time_line)))))
	record_line = readline(f)
	record = parse(Int, String(filter(isdigit, (collect.(record_line)))))
	time, record
end

# ╔═╡ 32c77b83-dc30-4581-9035-27f44ccf3370
md"""For this, we want more efficiency than iteration. We can solve the quadratic inequation analytically.

We can see this problem as one of finding the bounds of the valid interval of $u$, by means of the roots of $X(u) = u^2 - uT + Y$. By the quadratic formula, we have:

```math
x = \frac{-b \pm \sqrt{\Delta}}{2a}
```

Where $\Delta = b^2 -4ac$, and in this case, $\Delta > 0$ (otherwise, there are no solutions).

We can't just take the difference between solutions since that could include the endpoints. What we want is to find the nearest integer upwards from the bottom root, and the nearest integer downwards from the upper root.
"""

# ╔═╡ 0460ea47-0bdc-4692-8379-5388284a94f4
function ways_to_win_race_roots(time::Int, record::Int)
	Δ = time^2 - 4 * record
	if Δ <= 0
		return 0
	end
    sqrt_Δ = sqrt(Δ)
	x1, x2 = (time - sqrt_Δ)/2, (time + sqrt_Δ)/2
	u1 = ceil(x1) == x1 ? x1 + 1 : ceil(x1)
	u2 = floor(x2) == x2 ? x2 - 1 : floor(x2)
	trunc(Int, u2 - u1) + 1
end

# ╔═╡ 442d3a4d-535b-4df9-8ec2-eac618029e9e
md"We verify that it matches our earlier results:"

# ╔═╡ 3ab8ca4a-5f44-46e8-a161-5a14c541e310
[ways_to_win_race(time, record) for (time, record) in races]

# ╔═╡ 35839f1d-b853-41ca-b14c-b3427c0da0ca
[ways_to_win_race_roots(time, record) for (time, record) in races]

# ╔═╡ 55808454-db00-47bc-9593-dfb5c5418468
ways_to_win_race_roots(time, record)

# ╔═╡ Cell order:
# ╟─eca36bb7-ee8a-4ee5-b9fd-c2cf18e3dd6c
# ╠═cbc219c1-976a-4304-b83a-d9fe703eb763
# ╠═4569cd04-6728-4fcb-bc69-5800dd6affe4
# ╠═5c1a9ccd-c68e-470b-a1fb-777a5aa952ab
# ╟─399197c6-955e-11ee-0cb0-5dd361efe38c
# ╠═9a8fe9e4-8d86-419c-ae19-86fba59e4667
# ╠═15fbd389-3ba2-4ff3-a6a5-39e3b99b5ec2
# ╠═75c35ba6-4ed5-478d-ae43-b77f79887c49
# ╟─2d15432f-52dc-4c8a-bdb4-41f182bb63c3
# ╟─701563c9-4385-47e6-91a6-0fb75c7c1db9
# ╠═63d373fc-b90f-46f3-97ac-b5ffb12b73eb
# ╟─32c77b83-dc30-4581-9035-27f44ccf3370
# ╠═0460ea47-0bdc-4692-8379-5388284a94f4
# ╟─442d3a4d-535b-4df9-8ec2-eac618029e9e
# ╠═3ab8ca4a-5f44-46e8-a161-5a14c541e310
# ╠═35839f1d-b853-41ca-b14c-b3427c0da0ca
# ╠═55808454-db00-47bc-9593-dfb5c5418468
