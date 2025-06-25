# Elixirはスクリプトのように直接実行可能
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

sum_of_squares =
  numbers
  |> Enum.filter(fn n -> rem(n, 2) == 0 end) # `numbers`を`filter`関数に渡す
  |> Enum.map(fn n -> n * n end)             # `filter`の結果を`map`関数に渡す
  |> Enum.sum()                              # `map`の結果を`sum`関数に渡す

IO.puts("Elixir: The sum is #{sum_of_squares}")