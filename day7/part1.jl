using IterTools

input_file = joinpath(dirname(@__DIR__), "inputs", "day7.inp")
lines = split.(readlines(input_file))

struct Hand
    cards::Vector{Char}
    bid::Int
end

hands = [Hand(collect(hand), parse.(Int, bid)) for (hand, bid) in lines]
card_map = Dict(
    '2' => 2, '3' => 3, '4' => 4, '5' => 5, '6' => 6, '7' => 7, '8' => 8,
    '9' => 9, 'T' => 10, 'J' => 11, 'Q' => 12, 'K' => 13, 'A' => 14
)
hand_type_map = Dict(
    :five_of_a_kind => 6, :four_of_a_kind => 5, :full_house => 4,
    :three_of_a_kind => 3, :two_pair => 2, :one_pair => 1, :high_card => 0
)

function get_hand_type(hand::Hand)::Symbol
    groups = length.(collect(groupby(identity, sort(hand.cards))))
    n_unique = length(groups)
    if n_unique == 1
        return :five_of_a_kind
    elseif n_unique == 2
        if (1, 4) ⊆ groups
            return :four_of_a_kind
        else
            return :full_house
        end
    elseif n_unique == 3
        if (1, 3) ⊆ groups
            return :three_of_a_kind
        else
            return :two_pair
        end
    elseif n_unique == 4
        return :one_pair
    else
        return :high_card
    end
end

function less_than(x::Hand, y::Hand)
    # Order by hand type (primary)
    x_type = hand_type_map[get_hand_type(x)]
    y_type = hand_type_map[get_hand_type(y)]
    if x_type < y_type
        return true
    elseif x_type > y_type
        return false
    end
    # Order by successive card values (fallback)
    for (x_card, y_card) in zip(x.cards, y.cards)
        if card_map[x_card] < card_map[y_card]
            return true
        elseif card_map[x_card] > card_map[y_card]
            return false
        end
    end
    return true
end

ranks = invperm(sortperm(hands, lt=less_than))

winnings = []
for (hand, rank) in zip(hands, ranks)
    value = rank * hand.bid
    @info hand = hand rank = rank type = get_hand_type(hand) value = value
    push!(winnings, value)
end

@info "Total winnings:" sum(winnings)