% Erlang

-module(erlang).
-export([main/1]).

main(_) ->
    Numbers = [1,2,3,4,5,6,7,8,9,10],
    EvenNumbers = lists:filter(fun(N) -> N rem 2 =:= 0 end, Numbers),
    Squares = lists:map(fun(N) -> N * N end, EvenNumbers),
    Sum = lists:sum(Squares),
    io:format("Erlang: The sum is ~p~n", [Sum]).
